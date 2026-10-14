#!/usr/bin/env /usr/bin/python3
"""Create GitHub issues (epic -> issue -> sub-issue) from backlog YAML.

Resume-safe: key -> {number,id,node_id} is kept in tools/issue-map.json.
Usage: /usr/bin/python3 tools/push_backlog.py --dir backlog --repo OWNER/REPO [--only feature] [--dry-run]
"""
import argparse
import json
import subprocess
import sys
import time

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from backlog_lib import iter_items, labels_for, load_backlog, load_map, render_body, save_map  # noqa: E402

GH = "/opt/homebrew/bin/gh"


def gh_api(args, payload=None, retries=3):
    cmd = [GH, "api"] + args
    for attempt in range(retries):
        proc = subprocess.run(cmd, input=json.dumps(payload) if payload is not None else None,
                              text=True, capture_output=True)
        if proc.returncode == 0:
            return json.loads(proc.stdout) if proc.stdout.strip() else {}
        err = proc.stderr.strip()
        if "rate limit" in err.lower() or "abuse" in err.lower() or "secondary" in err.lower():
            wait = 60 * (attempt + 1)
            print(f"  rate limited, sleeping {wait}s", file=sys.stderr)
            time.sleep(wait)
            continue
        raise RuntimeError(err[:500])
    raise RuntimeError("gh api failed after retries")


def create_issue(repo, title, body, labels):
    data = gh_api([f"repos/{repo}/issues", "--method", "POST", "--input", "-"],
                  {"title": title, "body": body, "labels": labels})
    return {"number": data["number"], "id": data["id"], "node_id": data["node_id"], "url": data["html_url"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="backlog")
    ap.add_argument("--repo", required=True)
    ap.add_argument("--map", default="tools/issue-map.json")
    ap.add_argument("--only", help="feature name filter")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--sleep", type=float, default=1.2)
    args = ap.parse_args()

    feats = load_backlog(args.dir)
    issue_map = load_map(args.map)
    created = skipped = 0
    for feat in feats:
        if args.only and feat["feature"] != args.only:
            continue
        parent_items = {}
        for level, item, parent_key in iter_items(feat):
            parent_items[item["key"]] = item
            if item["key"] in issue_map:
                skipped += 1
                continue
            parent = parent_items.get(parent_key) if parent_key else None
            body = render_body(level, item, feat, parent_key)
            labels = labels_for(level, item, feat, parent)
            if args.dry_run:
                print(f"[dry] {level:9} {item['key']:10} {item['title']}  labels={labels}")
                continue
            info = create_issue(args.repo, item["title"], body, labels)
            info.update({"level": level, "feature": feat["feature"], "parent": parent_key})
            issue_map[item["key"]] = info
            save_map(args.map, issue_map)
            created += 1
            print(f"#{info['number']:4} {level:9} {item['key']:10} {item['title']}")
            time.sleep(args.sleep)
    print(f"created={created} skipped(existing)={skipped}")


if __name__ == "__main__":
    main()
