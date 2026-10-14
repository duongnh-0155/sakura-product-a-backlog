#!/usr/bin/env /usr/bin/python3
"""Hours (SWP × k) and sprint assignment for the reviewed backlog (decisions D-07, D-08).

k is calibrated on the LAB-1 epics that were broken down to task level (L3):
  k = sum(LAB-1 dev MD of anchor modules) × 8 / sum(LAB-5 SWP of the matching epics)
Sprint assignment is greedy: leaves sorted by (phase, priority, topological order), each placed in the
earliest sprint >= phase start and >= every dependency's sprint where the owner role has capacity left.
Usage: /usr/bin/python3 tools/plan_hours_sprints.py --scores swp-report/swp-scores-reviewed.json --dir BACKLOG \
         --lab1 LAB1_SUMMARY.json --out plan.json
"""
import argparse
import json
import math
import os
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from backlog_lib import iter_items, load_backlog  # noqa: E402

ANCHOR = {"M03": "EPIC-TRD", "M05B": "EPIC-OFF", "M06": "EPIC-STL", "M07": "EPIC-INC", "M09": "EPIC-ACC", "M12": "EPIC-MIG"}
PHASE_START = {1: 1, 2: 4, 3: 9}                 # sprint number where a phase may start
PRI = {"Critical": 0, "High": 1, "Medium": 2}
CAPACITY_H = 60                                  # 10 days × 8 h × focus 0.75 per person per sprint
ROSTER = {"FE-1": 1, "FE-2": 1, "BE-1": 1, "BE-2": 1, "BE-3": 1, "QA-1": 1, "QA-2": 1, "QA-AUTO": 1,
          "DESIGN": 1, "INFRA": 1, "PM": 1, "BrSE": 1}
POOLS = {"FE": ["FE-1", "FE-2"], "BE": ["BE-1", "BE-2", "BE-3"], "QA": ["QA-1", "QA-2"]}
RAMP = {1: 0.5, 2: 0.75}                         # onboarding sprints (LAB-1 M1 = 4.1 FTE)
N_SPRINTS = 30                                   # D-19: allow overrun beyond Sprint 18 (go-live)


def calibrate_k(scores, lab1):
    md = {c["code"]: c["dev_md"] for c in lab1["categories"]}
    hours = sum(md[m] for m in ANCHOR) * 8
    swp = sum(final_swp(scores[e]) for e in ANCHOR.values())   # reviewed SWP (D-18)
    return hours / swp, hours, swp


def final_swp(s):
    return s.get("final_swp", s["swp"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scores", required=True)
    ap.add_argument("--dir", required=True)
    ap.add_argument("--lab1", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--map", default="tools/issue-map.json")
    a = ap.parse_args()
    raw = json.load(open(a.scores, encoding="utf-8"))["scores"]
    imap = json.load(open(a.map, encoding="utf-8")) if os.path.exists(a.map) else {}
    by_num = {str(v["number"]): k for k, v in imap.items()}
    scores = {by_num.get(n, n): v for n, v in raw.items()}   # GitHub scores are keyed by issue number
    lab1 = json.load(open(a.lab1, encoding="utf-8"))
    feats = load_backlog(a.dir)
    meta, order = {}, []
    for f in feats:
        for level, item, parent in iter_items(f):
            par = meta.get(parent, {})
            meta[item["key"]] = {"level": level, "parent": parent, "owner": item.get("owner") or par.get("owner"),
                                 "phase": item.get("phase") or par.get("phase") or 2,
                                 "priority": item.get("priority") or par.get("priority") or "High",
                                 "deps": list(item.get("depends_on") or []) + list(par.get("deps", []))}
            order.append(item["key"])
    k, k_hours, k_swp = calibrate_k(scores, lab1)
    leaves = [x for x in order if scores[x]["is_leaf"] and meta[x]["level"] != "Epic"]
    hours = {x: math.ceil(final_swp(scores[x]) * k) for x in leaves}
    # dependency on a parent means "all its leaves"
    kids = {}
    for x in order:
        p = meta[x]["parent"]
        if p:
            kids.setdefault(p, []).append(x)

    def leaf_set(x):
        return [x] if x in hours else [y for c in kids.get(x, []) for y in leaf_set(c)]

    key = {x: (meta[x]["phase"], PRI.get(meta[x]["priority"], 1), order.index(x)) for x in leaves}
    deps = {x: {y for d in meta[x]["deps"] if d in meta for y in leaf_set(d) if y != x and y in hours} for x in leaves}
    indeg = {x: len(deps[x]) for x in leaves}
    users = {x: [] for x in leaves}
    for x in leaves:
        for y in deps[x]:
            users[y].append(x)
    used = {(o, s): 0.0 for o in ROSTER for s in range(1, N_SPRINTS + 1)}
    sprint, done, assignee = {}, set(), {}
    while len(done) < len(leaves):
        ready = [x for x in leaves if x not in done and indeg[x] == 0]
        if not ready:  # cycle: break it at the highest-priority remaining leaf
            ready = [min((x for x in leaves if x not in done), key=key.get)]
        x = min(ready, key=key.get)
        s = max([PHASE_START[meta[x]["phase"]]] + [sprint[y] for y in deps[x] if y in sprint])
        role = meta[x]["owner"] if meta[x]["owner"] in ROSTER else "PM"
        pool = next((v for v in POOLS.values() if role in v), [role])
        remaining, last, s0 = float(hours[x]), s, s
        while remaining > 0:   # whole item goes to the pool member with capacity earliest
            free = [(o, CAPACITY_H * RAMP.get(s, 1.0) - used[(o, s)]) for o in pool]
            o, cap = max(free, key=lambda t: t[1])
            if cap > 0 or s == N_SPRINTS:
                take = remaining if s == N_SPRINTS else min(cap, remaining)
                used[(o, s)] += take
                remaining -= take
                last = s
                assignee.setdefault(x, o)
            if remaining > 0:
                s = min(s + 1, N_SPRINTS)
        sprint[x] = last
        done.add(x)
        for u in users[x]:
            indeg[u] -= 1
    plan = {}
    for x in order:
        ls = leaf_set(x)
        h = sum(hours[y] for y in ls)
        sp = max(sprint[y] for y in ls) if ls and meta[x]["level"] != "Epic" else None
        plan[x] = {"Point": final_swp(scores[x]), "Hours": h, "Sprint": f"Sprint {sp:02d}" if sp else None}
        if x in assignee:
            plan[x]["担当"] = assignee[x]
    load = {s: {o: round(used[(o, s)]) for o in ROSTER if used[(o, s)]} for s in range(1, N_SPRINTS + 1)}
    json.dump({"k": k, "k_basis": {"lab1_hours": k_hours, "lab5_swp": k_swp, "anchor": ANCHOR},
               "plan": plan, "load": load}, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"k={k:.3f} h/SWP (LAB-1 {k_hours} h / LAB-5 {k_swp} SWP); leaves={len(leaves)} total_h={sum(hours.values())}")
    print("last sprint used:", max(sprint.values()))
    for sp in range(1, max(sprint.values()) + 1):
        print(f"  S{sp:02d} load={sum(load[sp].values()):5}h", load[sp])


if __name__ == "__main__":
    main()
