#!/usr/bin/env /usr/bin/python3
"""Validate backlog YAML files against the break-task brief before pushing.

Usage: /usr/bin/python3 tools/validate_backlog.py --dir backlog [--strict]
"""
import argparse
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from backlog_lib import CONSTRAINT_OPTION, METRIC_KEYS, iter_items, iter_keys, load_backlog  # noqa: E402

ROSTER = {"FE-1", "FE-2", "BE-1", "BE-2", "BE-3", "QA-1", "QA-2", "QA-AUTO", "DESIGN", "INFRA", "PM", "BrSE"}
TYPES = {"fe", "be", "db", "tech", "qa", "infra", "migration", "clarify"}
PRIORITIES = {"Critical", "High", "Medium"}
HANDLING = {"design-change", "assumption", "clarify-issue", "open"}
BODY_HEADINGS = ("## 概要", "## 完了の定義")


def check(feats):
    errors, warns = [], []
    all_keys = set()
    for f in feats:
        all_keys.update(iter_keys(f))
    for f in feats:
        fn = f["_file"]
        epic = f["epic"]
        if not epic.get("title", "").startswith("[Epic]"):
            warns.append(f"{fn}: epic title should start with [Epic]")
        for level, item, parent_key in iter_items(f):
            k = item.get("key", "?")
            tag = f"{fn}:{k}"
            for req in ("key", "title", "body"):
                if not item.get(req):
                    errors.append(f"{tag}: missing {req}")
            if level != "Epic":
                typ = item.get("type")
                if level == "Issue" and typ not in TYPES:
                    errors.append(f"{tag}: bad type {typ!r}")
                if level == "Issue" and item.get("priority") not in PRIORITIES:
                    errors.append(f"{tag}: bad priority {item.get('priority')!r}")
                con = item.get("constraint", "none" if level == "Sub-issue" else None)
                if level == "Issue" and con not in CONSTRAINT_OPTION:
                    errors.append(f"{tag}: bad constraint {con!r}")
                if item.get("owner") and item["owner"] not in ROSTER:
                    errors.append(f"{tag}: owner {item['owner']!r} not in roster")
                if level == "Issue" and not item.get("owner"):
                    errors.append(f"{tag}: missing owner")
                m = item.get("metrics")
                if not isinstance(m, dict):
                    errors.append(f"{tag}: missing metrics")
                else:
                    bad = [x for x in m if x not in METRIC_KEYS]
                    if bad:
                        errors.append(f"{tag}: unknown metric keys {bad}")
                    if sum(int(m.get(x, 0) or 0) for x in METRIC_KEYS) == 0:
                        warns.append(f"{tag}: all metrics are 0")
                if level == "Issue" and not item.get("specs"):
                    warns.append(f"{tag}: no specs listed")
                for dep in item.get("depends_on", []) or []:
                    if dep not in all_keys:
                        warns.append(f"{tag}: depends_on {dep} not found (cross-feature or missing)")
                body = item.get("body", "")
                if level == "Issue" and "完了の定義" not in body:
                    errors.append(f"{tag}: body lacks 完了の定義")
                if "\t" in body:
                    errors.append(f"{tag}: tab character in body")
                if level == "Issue" and item.get("sub_issues"):
                    for s in item["sub_issues"]:
                        if s.get("sub_issues"):
                            errors.append(f"{tag}: sub-issue {s.get('key')} has children")
        for g in f.get("gaps", []) or []:
            if g.get("handling") not in HANDLING:
                errors.append(f"{fn}:{g.get('id')}: bad handling {g.get('handling')!r}")
            if g.get("handling") == "clarify-issue" and not any(str(g.get("ref", "")).startswith(k) for k in all_keys):
                warns.append(f"{fn}:{g.get('id')}: clarify ref {g.get('ref')!r} is not an issue key")
    return errors, warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="backlog")
    ap.add_argument("--strict", action="store_true", help="warnings count as errors")
    args = ap.parse_args()
    feats = load_backlog(args.dir)
    errors, warns = check(feats)
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    n_i = sum(len(f.get("issues", [])) for f in feats)
    n_s = sum(len(i.get("sub_issues") or []) for f in feats for i in f.get("issues", []))
    n_g = sum(len(f.get("gaps") or []) for f in feats)
    print(f"files={len(feats)} issues={n_i} sub_issues={n_s} gaps={n_g} errors={len(errors)} warnings={len(warns)}")
    sys.exit(1 if errors or (args.strict and warns) else 0)


if __name__ == "__main__":
    main()
