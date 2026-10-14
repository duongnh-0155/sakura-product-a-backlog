#!/usr/bin/env /usr/bin/python3
"""Apply human-reviewed SWP decisions (class rules + per-issue overrides) to swp-scores.json.

Writes swp-scores-reviewed.json with final_swp / review_rule / review_reason per leaf, parents re-summed.
Usage: /usr/bin/python3 tools/apply_review.py --scores swp-report/swp-scores.json \
         --decisions swp-report/review-decisions.json --out swp-report/swp-scores-reviewed.json
"""
import argparse
import json
import math

FIB = [1, 2, 3, 5, 8, 13, 21, 34]
STRONG = {"BR-INC-01", "TBL-RATE-01", "permit-vs-approval", "post-close-correction"}


def fib_ceil(x):
    return next((f for f in FIB if f >= x), FIB[-1])


def matches(v, m):
    types = m.get("type")
    types = [types] if isinstance(types, str) else types
    if types and v["type"] not in types:
        return False
    if "swp_max" in m and v["swp"] > m["swp_max"]:
        return False
    return not ("title_has" in m and m["title_has"] not in v["title"])


def apply_rule(r, v, k):
    if r["rule"] == "floor":
        return max(v["swp"], r["value"])
    if r["rule"] == "questions_x2h":
        return fib_ceil(v["metrics"]["rules"] * 2 / k)
    if r["rule"] == "qa_by_scenarios":
        tv = v["metrics"]["test_vectors"]
        s = 34 if tv >= 40 else 21 if tv >= 20 else 13
        return max(s, 21) if v.get("constraint") in STRONG else s
    raise ValueError(r["rule"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scores", required=True)
    ap.add_argument("--decisions", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    data = json.load(open(a.scores, encoding="utf-8"))
    dec = json.load(open(a.decisions, encoding="utf-8"))
    sc, k = data["scores"], dec.get("k_hint_hours_per_swp", 2.17)
    changed = 0
    for key, v in sc.items():
        if not v["is_leaf"]:
            continue
        v["final_swp"], v["review_rule"], v["review_reason"] = v["swp"], None, None
        for r in dec["class_rules"]:
            if matches(v, r["match"]):
                v["final_swp"], v["review_rule"], v["review_reason"] = apply_rule(r, v, k), r["id"], r["reason"]
                break
        if key in dec.get("overrides", {}):
            o = dec["overrides"][key]
            v["final_swp"], v["review_rule"], v["review_reason"] = o["final_swp"], "override", o["reason"]
        changed += v["final_swp"] != v["swp"]

    def total(key):
        v = sc[key]
        if v["is_leaf"]:
            return v["final_swp"]
        v["final_swp"] = sum(total(c) for c in v["children"])
        return v["final_swp"]

    roots = [key for key, v in sc.items() if not v.get("parent")]
    grand = sum(total(r) for r in roots)
    data["review"] = {"status": dec.get("status"), "changed_leaves": changed, "total_before": sum(sc[r]["swp"] for r in roots),
                      "total_after": grand}
    json.dump(data, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"changed leaves={changed} total SWP {data['review']['total_before']} -> {grand}")


if __name__ == "__main__":
    main()
