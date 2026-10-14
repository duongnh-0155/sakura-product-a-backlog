#!/usr/bin/env /usr/bin/python3
"""Set Project fields for issues from a JSON plan.

Plan format: {"DLV-01": {"Point": 8, "Hours": 24, "Sprint": "Sprint 01", "Status": "Done", "担当": "FE-1"}, ...}
Keys are backlog keys (tools/issue-map.json) or "#123" issue numbers.
Usage: /usr/bin/python3 tools/set_fields.py --plan plan.json [--apply]   (default: dry-run)
"""
import argparse
import json
import subprocess
import sys
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from backlog_lib import load_map  # noqa: E402

GH = "/opt/homebrew/bin/gh"


def graphql(query, variables, retries=5):
    for attempt in range(retries):  # retry transient network / rate-limit errors
        proc = subprocess.run([GH, "api", "graphql", "--input", "-"],
                              input=json.dumps({"query": query, "variables": variables}), text=True, capture_output=True)
        if proc.returncode == 0:
            return json.loads(proc.stdout)
        err = proc.stderr.lower()
        if attempt < retries - 1 and any(t in err for t in ("reset", "timed out", "timeout", "eof", "50", "secondary")):
            time.sleep(10 * (attempt + 1))
            continue
        raise RuntimeError(proc.stderr.strip()[:400])


def load_fields(path):
    with open(path, encoding="utf-8") as fh:
        proj = json.load(fh)
    fields = {}
    for f in proj["fields"]["nodes"]:
        if not f:
            continue
        entry = {"id": f["id"], "type": f["dataType"], "options": {o["name"]: o["id"] for o in f.get("options", [])}}
        if f["dataType"] == "ITERATION":
            entry["options"] = {it["title"]: it["id"] for it in f["configuration"]["iterations"]}
        fields[f["name"]] = entry
    return proj["id"], fields


def value_literal(field, value):
    if field["type"] == "NUMBER":
        return "{number:%s}" % float(value)
    if field["type"] == "SINGLE_SELECT":
        return '{singleSelectOptionId:"%s"}' % field["options"][value]
    if field["type"] == "ITERATION":
        return '{iterationId:"%s"}' % field["options"][value]
    if field["type"] == "TEXT":
        return '{text:%s}' % json.dumps(str(value), ensure_ascii=False)
    raise ValueError(field["type"])


def resolve_item_id(key, imap):
    if key in imap:
        return imap[key]["item_id"], imap[key]["number"]
    if key.startswith("#"):
        for rec in imap.values():
            if rec["number"] == int(key[1:]):
                return rec["item_id"], rec["number"]
    raise KeyError(key)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--map", default="tools/issue-map.json")
    ap.add_argument("--fields", default="tools/project-fields.json")
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()
    with open(args.plan, encoding="utf-8") as fh:
        plan = json.load(fh)
    imap = load_map(args.map)
    project_id, fields = load_fields(args.fields)
    n = 0
    for key, values in plan.items():
        item_id, number = resolve_item_id(key, imap)
        muts = []
        for i, (fname, val) in enumerate(values.items()):
            if val is None:
                continue
            fld = fields[fname]
            muts.append('f%d: updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$it,fieldId:"%s",value:%s}){projectV2Item{id}}'
                        % (i, fld["id"], value_literal(fld, val)))
        if not muts:
            continue
        print(f"{'APPLY' if args.apply else 'dry'} #{number:4} {key:10} {values}")
        if args.apply:
            graphql("mutation($p:ID!,$it:ID!){" + " ".join(muts) + "}", {"p": project_id, "it": item_id})
            time.sleep(0.25)
        n += 1
    print(f"items: {n} ({'applied' if args.apply else 'dry-run'})")


if __name__ == "__main__":
    main()
