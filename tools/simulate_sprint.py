#!/usr/bin/env /usr/bin/python3
"""Apply the simulated sprint (sim/sprint-simulation.json) to the Project and derive burndown data.

- Status / Sprint fields per event (carry-over moves the Sprint), parents and epics follow their children
- Done issues are closed (state_reason=completed); events with `comment` get an issue comment
- writes sim/burndown.json and sim/burndown-sprint-01.svg / -02.svg
Usage: /usr/bin/python3 tools/simulate_sprint.py [--apply]
"""
import argparse
import json
import subprocess
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from backlog_lib import load_map  # noqa: E402
from burndown_svg import render  # noqa: E402

GH = "/opt/homebrew/bin/gh"
REPO = "duongnh-0155/sakura-product-a-backlog"
RANK = ["Blocked", "In Progress", "In Review", "Todo", "Done", "Backlog"]


def gh(args, payload=None):
    p = subprocess.run([GH] + args, input=json.dumps(payload) if payload is not None else None, text=True, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.strip()[:300])
    return p.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sim", default="sim/sprint-simulation.json")
    ap.add_argument("--plan", default="swp-report/field-plan.json")
    ap.add_argument("--scores", default="swp-report/swp-scores-reviewed.json")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    sim = json.load(open(a.sim, encoding="utf-8"))
    imap = load_map("tools/issue-map.json")
    plan = json.load(open(a.plan, encoding="utf-8"))
    raw = json.load(open(a.scores, encoding="utf-8"))["scores"]
    swp = {k: raw[str(v["number"])]["final_swp"] for k, v in imap.items()}
    status, sprint = {}, {k: v.get("Sprint") for k, v in plan.items()}
    for ev in sim["events"]:
        status[ev["key"]] = ev["status"]
        if ev.get("carry_to"):
            sprint[ev["key"]] = ev["carry_to"]
    for k, sp in sprint.items():          # next sprint = planned
        if k not in status and sp == "Sprint 03":
            status[k] = "Todo"
    kids = {}
    for k, v in imap.items():
        if v.get("parent"):
            kids.setdefault(v["parent"], []).append(k)

    def roll(k):  # parent status from children
        if k not in kids:
            return status.get(k, "Backlog")
        st = [roll(c) for c in kids[k]]
        if all(s == "Done" for s in st):
            res = "Done"
        elif any(s != "Backlog" for s in st):
            res = "In Progress" if any(s in ("Done", "In Progress", "In Review", "Blocked") for s in st) else "Todo"
        else:
            res = "Backlog"
        status[k] = res
        return res

    for k, v in imap.items():
        if v["level"] == "Epic":
            roll(k)
    changes = {k: {"Status": s} for k, s in status.items() if s != "Backlog"}
    for ev in sim["events"]:
        if ev.get("carry_to"):
            changes.setdefault(ev["key"], {})["Sprint"] = ev["carry_to"]
    json.dump(changes, open("sim/status-plan.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # burndown per sprint
    bd = {}
    for name, sp in sim["sprints"].items():
        committed = [k for k, s in sprint.items() if s == name and k not in kids and imap.get(k, {}).get("level") != "Epic"]
        committed += [ev["key"] for ev in sim["events"] if ev.get("carry_to") == name]
        committed = sorted(set(committed) | {ev["key"] for ev in sim["events"] if ev["sprint"] == name and ev["key"] not in kids})
        total = sum(swp[k] for k in committed)
        done_day = {ev["key"]: ev["day"] for ev in sim["events"] if ev["sprint"] == name and ev["status"] == "Done"}
        last = sp["days"] if sp["closed"] else sp["as_of_day"]
        remaining = [total - sum(swp[k] for k, d in done_day.items() if d <= day) for day in range(0, last + 1)]
        bd[name] = {"committed_keys": committed, "committed_swp": total, "remaining": remaining, "days": sp["days"],
                    "done_swp": total - remaining[-1], "start": sp["start"], "end": sp["end"]}
        open(f"sim/burndown-{name.lower().replace(' ', '-')}.svg", "w", encoding="utf-8").write(render(name, bd[name]))
    json.dump(bd, open("sim/burndown.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for name, b in bd.items():
        print(f"{name}: committed {b['committed_swp']} SWP ({len(b['committed_keys'])} items), done {b['done_swp']}, remaining {b['remaining']}")
    print(f"status changes: {len(changes)}")
    if not a.apply:
        print("dry-run (use --apply)")
        return
    subprocess.run([sys.executable, "tools/set_fields.py", "--plan", "sim/status-plan.json", "--apply"], check=True)
    for k, s in status.items():
        if s == "Done":
            gh(["api", f"repos/{REPO}/issues/{imap[k]['number']}", "--method", "PATCH", "--input", "-"],
               {"state": "closed", "state_reason": "completed"})
    for ev in sim["events"]:
        if ev.get("comment"):
            gh(["api", f"repos/{REPO}/issues/{imap[ev['key']]['number']}/comments", "--method", "POST", "--input", "-"],
               {"body": ev["comment"] + "\n\n_（LAB-5 のスプリント模擬。日付・進捗は架空）_"})
    print("applied")


if __name__ == "__main__":
    main()
