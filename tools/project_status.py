#!/usr/bin/env /usr/bin/python3
"""Status / sprint / release-burndown tables computed from a fresh Project fetch (items.json).

SWP is summed over leaves only (parents are sums of children) to avoid double counting.
Usage: /usr/bin/python3 tools/project_status.py --items sim/items-after-sprint.json --out sim/status.json
"""
import argparse
import collections
import json

ORDER = ["Done", "In Review", "In Progress", "Blocked", "Todo", "Backlog"]


def num(v):
    try:
        return float(v or 0)
    except (TypeError, ValueError):
        return 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    items = json.load(open(a.items, encoding="utf-8"))["items"]
    leaves = [i for i in items if not i.get("children") and i["level"] != "Epic"]
    by_status = collections.defaultdict(lambda: {"items": 0, "leaves": 0, "swp": 0.0, "hours": 0.0})
    for i in items:
        if i["level"] == "Epic":
            continue
        st = i["fields"].get("Status") or "Backlog"
        by_status[st]["items"] += 1
        if not i.get("children"):
            by_status[st]["leaves"] += 1
            by_status[st]["swp"] += num(i["fields"].get("Point"))
            by_status[st]["hours"] += num(i["fields"].get("Hours"))
    sprints = collections.defaultdict(lambda: collections.Counter())
    for i in leaves:
        sp = i["fields"].get("Sprint") or "—"
        st = i["fields"].get("Status") or "Backlog"
        sprints[sp][st] += num(i["fields"].get("Point"))
        sprints[sp]["_n"] += 1
    total = sum(num(i["fields"].get("Point")) for i in leaves)
    planned, remaining = [], total
    for sp in sorted(k for k in sprints if k.startswith("Sprint")):
        remaining -= sum(v for k, v in sprints[sp].items() if not k.startswith("_"))
        planned.append({"sprint": sp, "planned_remaining": round(remaining)})
    done = by_status["Done"]["swp"]
    epics = {i["number"]: (i["fields"].get("Status") or "Backlog") for i in items if i["level"] == "Epic"}
    out = {"total_leaf_swp": total, "done_swp": done, "by_status": {s: by_status[s] for s in ORDER if s in by_status},
           "sprints": {k: dict(v) for k, v in sorted(sprints.items())}, "release_plan": planned, "epics": epics,
           "closed_issues": sum(1 for i in items if i.get("state") == "CLOSED")}
    json.dump(out, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for s, v in out["by_status"].items():
        print(f"{s:12} items={v['items']:3} leaves={v['leaves']:3} swp={v['swp']:6.0f} h={v['hours']:6.0f}")
    print("total leaf SWP", total, "done", done, "closed issues", out["closed_issues"])
    for sp in ("Sprint 01", "Sprint 02", "Sprint 03"):
        print(sp, dict(out["sprints"].get(sp, {})))
    print("epic status", collections.Counter(epics.values()))


if __name__ == "__main__":
    main()
