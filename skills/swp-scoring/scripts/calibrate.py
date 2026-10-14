"""Quantile calibration of bucket thresholds (decision D-15).

Weights stay fixed; only the 4 upper bounds per axis move so that the leaves of
this backlog spread over levels 1..5 at the 20/40/60/80th percentiles of raw.
"""
from __future__ import annotations

from typing import Dict, List

from score import complexity_raw, normalize_metrics, parse_metrics, scope_raw

QUANTILES = (0.2, 0.4, 0.6, 0.8)


def _quantile(sorted_vals: List[float], q: float) -> float:
    if not sorted_vals:
        return 0.0
    pos = (len(sorted_vals) - 1) * q
    lo, hi = int(pos), min(int(pos) + 1, len(sorted_vals) - 1)
    return sorted_vals[lo] + (sorted_vals[hi] - sorted_vals[lo]) * (pos - lo)


def _strictly_increasing(vals: List[float]) -> List[float]:
    out: List[float] = []
    for v in vals:
        v = round(v * 2) / 2  # 0.5 刻み
        out.append(v if not out or v > out[-1] else out[-1] + 0.5)
    return out


def leaf_raws(items: List[dict]) -> Dict[str, List[float]]:
    parents = {it.get("parent") for it in items if it.get("parent")}
    parents |= {it["key"] for it in items if it.get("children")}
    s_vals, c_vals = [], []
    for it in items:
        if it["key"] in parents:
            continue
        m = normalize_metrics(it.get("metrics")) or parse_metrics(it.get("body"))
        if m is None:
            continue
        s_vals.append(scope_raw(m))
        c_vals.append(complexity_raw(m, it.get("constraint"), it.get("type")))
    return {"scope": sorted(s_vals), "complexity": sorted(c_vals)}


def calibrate(items: List[dict]) -> dict:
    raws = leaf_raws(items)
    out = {"method": "quantile 20/40/60/80 of leaf raw scores (D-15)", "n_leaves": len(raws["scope"])}
    for axis in ("scope", "complexity"):
        out[axis] = _strictly_increasing([_quantile(raws[axis], q) for q in QUANTILES])
    return out
