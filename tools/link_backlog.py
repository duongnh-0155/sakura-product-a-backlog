#!/usr/bin/env /usr/bin/python3
"""Second pass after push_backlog.py: link sub-issues, add items to the Project,
set Level / Priority / Constraint / 担当 / Status fields, rewrite {{DEP:KEY}} -> #number.

Usage: /usr/bin/python3 tools/link_backlog.py --dir backlog --repo OWNER/REPO --step sub|project|fields|deps|all
"""
import argparse
import json
import re
import subprocess
import sys
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from backlog_lib import CONSTRAINT_OPTION, DEP_RE, iter_items, load_backlog, load_map, save_map  # noqa: E402

GH = "/opt/homebrew/bin/gh"


TRANSIENT = ("timed out", "timeout", "connection reset", "eof", "502", "503", "504", "secondary rate", "abuse")


def gh(args, payload=None, retries=5):
    """Run gh; retry transient network / rate-limit errors with backoff."""
    for attempt in range(retries):
        proc = subprocess.run([GH] + args, input=json.dumps(payload) if payload is not None else None,
                              text=True, capture_output=True)
        if proc.returncode == 0:
            return json.loads(proc.stdout) if proc.stdout.strip() else {}
        err = proc.stderr.strip()
        if attempt < retries - 1 and any(t in err.lower() for t in TRANSIENT):
            time.sleep(10 * (attempt + 1))
            continue
        raise RuntimeError(err[:400])


def graphql(query, variables):
    return gh(["api", "graphql", "--input", "-"], {"query": query, "variables": variables})


def load_fields(path):
    with open(path, encoding="utf-8") as fh:
        proj = json.load(fh)
    fields = {}
    for f in proj["fields"]["nodes"]:
        if not f:
            continue
        fields[f["name"]] = {"id": f["id"], "options": {o["name"]: o["id"] for o in f.get("options", [])}}
    return proj["id"], fields


def step_sub(repo, feats, imap):
    done = 0
    for feat in feats:
        for level, item, parent_key in iter_items(feat):
            if not parent_key or imap[item["key"]].get("linked"):
                continue
            parent = imap[parent_key]["number"]
            try:
                gh(["api", f"repos/{repo}/issues/{parent}/sub_issues", "--method", "POST", "--input", "-"],
                   {"sub_issue_id": imap[item["key"]]["id"]})
            except RuntimeError as exc:
                if not any(t in str(exc).lower() for t in ("already", "duplicate", "only have one parent")):
                    raise
            imap[item["key"]]["linked"] = True
            done += 1
            time.sleep(0.4)
    print(f"sub-issue links: {done}")


def existing_items(project_id):
    """content node id -> project item id for items already in the project."""
    q = ("query($p:ID!,$a:String){node(id:$p){... on ProjectV2{items(first:100,after:$a){pageInfo{hasNextPage endCursor}"
         "nodes{id content{... on Issue{id}}}}}}}")
    out, after = {}, None
    while True:
        page = graphql(q, {"p": project_id, "a": after})["data"]["node"]["items"]
        out.update({n["content"]["id"]: n["id"] for n in page["nodes"] if n.get("content")})
        if not page["pageInfo"]["hasNextPage"]:
            return out
        after = page["pageInfo"]["endCursor"]


def step_project(project_id, feats, imap):
    q = "mutation($p:ID!,$c:ID!){addProjectV2ItemById(input:{projectId:$p,contentId:$c}){item{id}}}"
    have = existing_items(project_id)
    for rec in imap.values():
        if not rec.get("item_id") and rec["node_id"] in have:
            rec["item_id"] = have[rec["node_id"]]
    done = 0
    for feat in feats:
        for level, item, _ in iter_items(feat):
            rec = imap[item["key"]]
            if rec.get("item_id"):
                continue
            try:
                rec["item_id"] = graphql(q, {"p": project_id, "c": rec["node_id"]})["data"]["addProjectV2ItemById"]["item"]["id"]
            except RuntimeError as exc:  # GitHub's built-in workflow auto-adds sub-issues of items in the project
                if "already exists" not in str(exc):
                    raise
                for _ in range(5):  # the listing lags behind the auto-add
                    time.sleep(3)
                    have.update(existing_items(project_id))
                    if rec["node_id"] in have:
                        rec["item_id"] = have[rec["node_id"]]
                        break
                else:
                    print(f"  skip {rec['number']}: auto-added but not listed yet (re-run later)")
                    continue
            done += 1
            time.sleep(0.3)
    print(f"project items added: {done}")


def step_fields(project_id, fields, feats, imap):
    tmpl = ('f{i}: updateProjectV2ItemFieldValue(input:{{projectId:$p,itemId:$it,fieldId:"{fid}",'
            'value:{{singleSelectOptionId:"{oid}"}}}}){{projectV2Item{{id}}}}')
    done = 0
    for feat in feats:
        parents = {}
        for level, item, parent_key in iter_items(feat):
            parents[item["key"]] = item
            rec = imap[item["key"]]
            if rec.get("fields_set") or not rec.get("item_id"):
                continue
            par = parents.get(parent_key, {}) if parent_key else {}
            pri = item.get("priority") or par.get("priority") or feat["epic"].get("priority") or "Medium"
            con = CONSTRAINT_OPTION[item.get("constraint") or par.get("constraint") or "none"]
            own = item.get("owner") or par.get("owner") or "PM"
            wanted = [("Level", level), ("Priority", pri), ("Constraint", con), ("担当", own), ("Status", "Backlog")]
            muts = []
            for i, (fname, oname) in enumerate(wanted):
                fld = fields[fname]
                oid = fld["options"].get(oname)
                if not oid:
                    raise KeyError(f"option {oname!r} not in field {fname}")
                muts.append(tmpl.format(i=i, fid=fld["id"], oid=oid))
            graphql("mutation($p:ID!,$it:ID!){" + " ".join(muts) + "}", {"p": project_id, "it": rec["item_id"]})
            rec["fields_set"] = True
            done += 1
            time.sleep(0.3)
    print(f"field sets: {done}")


def step_deps(repo, feats, imap):
    done = 0
    for feat in feats:
        for level, item, _ in iter_items(feat):
            rec = imap[item["key"]]
            if rec.get("deps_done"):
                continue
            body = gh(["api", f"repos/{repo}/issues/{rec['number']}", "--jq", "{body:.body}"])["body"] or ""
            if "{{DEP:" in body:
                new = DEP_RE.sub(lambda m: f"#{imap[m.group(1)]['number']}" if m.group(1) in imap else f"`{m.group(1)}`", body)
                gh(["api", f"repos/{repo}/issues/{rec['number']}", "--method", "PATCH", "--input", "-"], {"body": new})
                time.sleep(0.6)
            rec["deps_done"] = True
            done += 1
    print(f"dependency rewrites: {done}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="backlog")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--map", default="tools/issue-map.json")
    ap.add_argument("--fields", default="tools/project-fields.json")
    ap.add_argument("--step", default="all", choices=["sub", "project", "fields", "deps", "all"])
    args = ap.parse_args()
    feats = load_backlog(args.dir)
    imap = load_map(args.map)
    project_id, fields = load_fields(args.fields)
    try:
        if args.step in ("sub", "all"):
            step_sub(args.repo, feats, imap)
        if args.step in ("project", "all"):
            step_project(project_id, feats, imap)
        if args.step in ("fields", "all"):
            step_fields(project_id, fields, feats, imap)
        if args.step in ("deps", "all"):
            step_deps(args.repo, feats, imap)
    finally:
        save_map(args.map, imap)


if __name__ == "__main__":
    main()
