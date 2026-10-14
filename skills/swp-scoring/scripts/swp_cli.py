#!/usr/bin/env /usr/bin/python3
"""SWP scoring CLI.

  swp_cli.py fetch [--owner duongnh-0155] [--number 1] [--out items.json] [--from-yaml DIR]
  swp_cli.py calibrate --in items.json [--out references/calibration.json]
  swp_cli.py score --in items.json --out-dir DIR [--sample 30] [--seed 42] [--calibration FILE|none]
  swp_cli.py write-points --scores reviewed.json --items items.json [--fields tools/project-fields.json] [--apply]

`fetch`/`score` are read-only. `write-points` is dry-run unless --apply is given.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from report_html import render_report  # noqa: E402
from score import active_thresholds, score_items, select_samples, set_thresholds  # noqa: E402

DEFAULT_CALIBRATION = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references", "calibration.json")

DEFAULT_OWNER, DEFAULT_NUMBER = "duongnh-0155", 1


def _load(path: str) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _dump(obj, path: str) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, ensure_ascii=False, indent=2)


def cmd_fetch(a: argparse.Namespace) -> int:
    if a.from_yaml:
        from backlog_yaml import load_backlog_dir
        data = load_backlog_dir(a.from_yaml)
    else:
        from fetch_project import fetch_project
        data = fetch_project(a.owner, a.number, a.gh)
    _dump(data, a.out)
    print("fetched %d items (%s) -> %s" % (len(data["items"]), data["source"], a.out))
    return 0


def cmd_calibrate(a: argparse.Namespace) -> int:
    from calibrate import calibrate
    cal = calibrate(_load(a.infile)["items"])
    _dump(cal, a.out)
    print("calibrated on %d leaves: scope=%s complexity=%s -> %s" % (cal["n_leaves"], cal["scope"], cal["complexity"], a.out))
    return 0


def cmd_score(a: argparse.Namespace) -> int:
    if a.calibration != "none" and os.path.exists(a.calibration):
        cal = _load(a.calibration)
        set_thresholds(cal.get("scope"), cal.get("complexity"))
        print("thresholds from %s: %s" % (os.path.basename(a.calibration), active_thresholds()))
    data = _load(a.infile)
    items = data["items"]
    scores = score_items(items)
    samples = select_samples(scores, n=a.sample, seed=a.seed)
    os.makedirs(a.out_dir, exist_ok=True)
    src = data.get("source_path") or ("%s/projects/%s" % (data.get("project", {}).get("owner"), data.get("project", {}).get("number")))
    html_path = os.path.join(a.out_dir, "swp-report.html")
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(render_report(scores, samples, {"source_label": src, "seed": a.seed, "extra_random": 5,
                                                 "thresholds": active_thresholds()}))
    sidecar = {k: {f: v[f] for f in ("number", "title", "level", "scope", "complexity", "product", "swp", "is_leaf",
                                       "children", "parent", "epic", "constraint", "type", "metrics", "missing", "item_id")}
               for k, v in scores.items()}
    for k in samples:
        sidecar[k]["sample"] = True
    _dump({"seed": a.seed, "samples": samples, "scores": sidecar}, os.path.join(a.out_dir, "swp-scores.json"))
    roots = [s for s in scores.values() if not s["parent"]]
    missing = [s["key"] for s in scores.values() if s["missing"]]
    print("items=%d leaves=%d total_swp=%d samples=%d missing_metrics=%d" % (
        len(scores), sum(1 for s in scores.values() if s["is_leaf"]), sum(r["swp"] for r in roots), len(samples), len(missing)))
    if missing:
        print("WARN missing swp-metrics:", ", ".join(missing))
    print("report:", html_path)
    return 0


def cmd_write_points(a: argparse.Namespace) -> int:
    from write_points import apply_writes, load_field_ids, plan_writes
    reviewed = _load(a.scores)
    scores = reviewed.get("scores", reviewed)
    items_by_key = {it["key"]: it for it in _load(a.items)["items"]} if a.items else {}
    ids = load_field_ids(a.fields)
    rows = plan_writes(scores, items_by_key)
    to_write = [r for r in rows if r["status"] == "write"]
    print("%-10s %-8s %-8s %s" % ("key", "before", "value", "status"))
    for r in rows:
        print("%-10s %-8s %-8s %s" % (r["key"], r.get("before", ""), r.get("value", ""), r["status"]))
    print("planned writes: %d / %d items" % (len(to_write), len(rows)))
    if not a.apply:
        print("DRY-RUN: nothing written. Re-run with --apply after human review.")
        return 0
    done = apply_writes(rows, ids, a.gh)
    errors = [r for r in done if r["status"].startswith("error")]
    print("written: %d, errors: %d" % (len(done) - len(errors), len(errors)))
    for r in errors:
        print("  ", r["key"], r["status"])
    return 1 if errors else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="SWP scoring for GitHub Project backlog")
    ap.add_argument("--gh", default="/opt/homebrew/bin/gh")
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch", help="fetch Project items (or --from-yaml for local dry-run)")
    f.add_argument("--owner", default=DEFAULT_OWNER)
    f.add_argument("--number", type=int, default=DEFAULT_NUMBER)
    f.add_argument("--out", default="items.json")
    f.add_argument("--from-yaml", dest="from_yaml", default=None, help="directory of backlog YAML files")
    f.set_defaults(func=cmd_fetch)
    s = sub.add_parser("score", help="score items and render HTML + JSON (no writes to GitHub)")
    s.add_argument("--in", dest="infile", required=True)
    s.add_argument("--out-dir", dest="out_dir", required=True)
    s.add_argument("--sample", type=int, default=30)
    s.add_argument("--seed", type=int, default=42)
    s.add_argument("--calibration", default=DEFAULT_CALIBRATION, help="calibration.json, or 'none' for fixed D-13 thresholds")
    s.set_defaults(func=cmd_score)
    c = sub.add_parser("calibrate", help="derive bucket thresholds from leaf raw-score quantiles (D-15)")
    c.add_argument("--in", dest="infile", required=True)
    c.add_argument("--out", default=DEFAULT_CALIBRATION)
    c.set_defaults(func=cmd_calibrate)
    w = sub.add_parser("write-points", help="write reviewed SWP to the Point field (dry-run unless --apply)")
    w.add_argument("--scores", required=True, help="swp-scores.json edited by a human (final_swp per key)")
    w.add_argument("--items", default=None, help="items.json from fetch (for item ids / current Point)")
    w.add_argument("--fields", default="tools/project-fields.json")
    w.add_argument("--apply", action="store_true")
    w.set_defaults(func=cmd_write_points)
    a = ap.parse_args(argv)
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
