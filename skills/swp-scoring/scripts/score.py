"""SWP (Story Weight Point) scoring — pure functions, importable.

Rubric (fixed):
  Scope raw      = screens*2 + apis*1 + tables*1.5 + integrations*2
  Complexity raw = states*1 + rules*1.5 + integrations*2 + test_vectors*0.5
                   + 2 (constraint != none) + 1 (type in tech/migration)
  scope bucket:      raw<=2 ->1, <=4 ->2, <=7 ->3, <=11 ->4, >11 ->5
  complexity bucket: raw<=2 ->1, <=5 ->2, <=9 ->3, <=14 ->4, >14 ->5   (D-13, 2026-10-11)
  leaf SWP = ceil-to-Fibonacci(scope * complexity); parent SWP = sum(children)
"""
from __future__ import annotations

import random
import re
from typing import Dict, List, Optional

FIB = [1, 2, 3, 5, 8, 13, 21, 34]
METRIC_KEYS = ("screens", "apis", "tables", "states", "rules", "integrations", "test_vectors")
NONE_CONSTRAINTS = {"", "none", "なし", "null", "-"}
COMPLEX_TYPES = {"tech", "migration"}
METRICS_RE = re.compile(r"<!--\s*swp-metrics:\s*(.*?)\s*-->", re.S)


def fib_ceil(x: float) -> int:
    """Smallest Fibonacci value >= x (clamped to FIB[-1])."""
    for f in FIB:
        if f >= x:
            return f
    return FIB[-1]


SCOPE_THRESHOLDS = (2, 4, 7, 11)
COMPLEXITY_THRESHOLDS = (2, 5, 9, 14)


def bucket(raw: float, thresholds=SCOPE_THRESHOLDS) -> int:
    """Map a raw score to 1..5 using 4 inclusive upper bounds."""
    for level, upper in enumerate(thresholds, start=1):
        if raw <= upper:
            return level
    return 5


_ACTIVE = {"scope": SCOPE_THRESHOLDS, "complexity": COMPLEXITY_THRESHOLDS}


def set_thresholds(scope=None, complexity=None) -> None:
    """Override bucket thresholds (from references/calibration.json, D-15)."""
    if scope:
        _ACTIVE["scope"] = tuple(scope)
    if complexity:
        _ACTIVE["complexity"] = tuple(complexity)


def active_thresholds() -> Dict[str, tuple]:
    return dict(_ACTIVE)


def scope_bucket(raw: float) -> int:
    return bucket(raw, _ACTIVE["scope"])


def complexity_bucket(raw: float) -> int:
    return bucket(raw, _ACTIVE["complexity"])


def parse_metrics(body: Optional[str]) -> Optional[Dict[str, int]]:
    """Read `<!-- swp-metrics: screens=1 apis=2 ... -->` from an issue body."""
    if not body:
        return None
    m = METRICS_RE.search(body)
    if not m:
        return None
    out = {k: 0 for k in METRIC_KEYS}
    for pair in re.findall(r"([a-z_]+)\s*=\s*(-?\d+)", m.group(1)):
        if pair[0] in out:
            out[pair[0]] = int(pair[1])
    return out


def normalize_metrics(raw: Optional[dict]) -> Optional[Dict[str, int]]:
    if not isinstance(raw, dict):
        return None
    out = {}
    for k in METRIC_KEYS:
        try:
            out[k] = int(raw.get(k, 0) or 0)
        except (TypeError, ValueError):
            out[k] = 0
    return out


def is_constrained(constraint: Optional[str]) -> bool:
    return (constraint or "").strip().lower() not in NONE_CONSTRAINTS


def scope_raw(m: Dict[str, int]) -> float:
    return m["screens"] * 2 + m["apis"] * 1 + m["tables"] * 1.5 + m["integrations"] * 2


def complexity_raw(m: Dict[str, int], constraint: Optional[str], type_: Optional[str]) -> float:
    raw = m["states"] * 1 + m["rules"] * 1.5 + m["integrations"] * 2 + m["test_vectors"] * 0.5
    if is_constrained(constraint):
        raw += 2
    if (type_ or "").strip().lower() in COMPLEX_TYPES:
        raw += 1
    return raw


def score_leaf(item: dict) -> dict:
    """Score one leaf item. item: {metrics?, body?, constraint?, type?}."""
    metrics = normalize_metrics(item.get("metrics")) or parse_metrics(item.get("body"))
    warnings: List[str] = []
    if metrics is None:
        metrics = {k: 0 for k in METRIC_KEYS}
        warnings.append("swp-metrics 行が無い（Scope=Complexity=1 で仮採点）")
        s_raw, c_raw, scope, cx, missing = 0.0, 0.0, 1, 1, True
    else:
        s_raw = scope_raw(metrics)
        c_raw = complexity_raw(metrics, item.get("constraint"), item.get("type"))
        scope, cx, missing = scope_bucket(s_raw), complexity_bucket(c_raw), False
    product = scope * cx
    return {
        "scope": scope, "complexity": cx, "scope_raw": s_raw, "complexity_raw": c_raw,
        "product": product, "swp": fib_ceil(product), "metrics": metrics,
        "missing": missing, "warnings": warnings,
    }


def _root_of(key: str, parent_of: Dict[str, Optional[str]]) -> str:
    seen = set()
    while parent_of.get(key) and key not in seen:
        seen.add(key)
        key = parent_of[key]
    return key


def score_items(items: List[dict]) -> Dict[str, dict]:
    """Score a flat item list (each has key, parent, children). Parents = sum of children."""
    by_key = {it["key"]: it for it in items}
    children: Dict[str, List[str]] = {k: [] for k in by_key}
    parent_of: Dict[str, Optional[str]] = {}
    for it in items:
        kids = [c for c in (it.get("children") or []) if c in by_key and c != it["key"]]
        children[it["key"]].extend(k for k in kids if k not in children[it["key"]])
        for c in kids:
            parent_of.setdefault(c, it["key"])
    for it in items:  # parent pointers not mirrored by children lists
        p = it.get("parent")
        if p in by_key and p != it["key"] and it["key"] not in children[p]:
            children[p].append(it["key"])
            parent_of.setdefault(it["key"], p)
    scores: Dict[str, dict] = {}

    def visit(key: str, stack: tuple) -> dict:
        if key in scores:
            return scores[key]
        it, kids = by_key[key], [c for c in children[key] if c not in stack]
        if kids:
            kid_scores = [visit(c, stack + (key,)) for c in kids]
            res = {"scope": None, "complexity": None, "product": None,
                   "swp": sum(k["swp"] for k in kid_scores), "metrics": None,
                   "missing": False, "warnings": [], "scope_raw": None, "complexity_raw": None}
        else:
            res = score_leaf(it)
        res.update({"key": key, "number": it.get("number"), "title": it.get("title", ""),
                    "level": it.get("level"), "type": it.get("type"),
                    "constraint": it.get("constraint") or "none", "is_leaf": not kids,
                    "children": kids, "parent": parent_of.get(key),
                    "epic": _root_of(key, parent_of), "item_id": it.get("item_id")})
        scores[key] = res
        return res

    for k in by_key:
        visit(k, ())
    return scores


def select_samples(scores: Dict[str, dict], n: int = 30, seed: int = 42, extra_random: int = 5) -> List[str]:
    """Deterministic review sample: per-epic max/min leaf, constrained leaves (<=2/epic), + random."""
    leaves = sorted((s for s in scores.values() if s["is_leaf"]), key=lambda s: s["key"])
    by_epic: Dict[str, List[dict]] = {}
    for s in leaves:
        by_epic.setdefault(s["epic"], []).append(s)
    picked: List[str] = []

    def add(key: str) -> None:
        if key not in picked:
            picked.append(key)

    for epic in sorted(by_epic):
        group = by_epic[epic]
        add(max(group, key=lambda s: (s["swp"], s["key"]))["key"])
        add(min(group, key=lambda s: (s["swp"], s["key"]))["key"])
        for s in [g for g in group if is_constrained(g["constraint"])][:2]:
            add(s["key"])
    rng = random.Random(seed)
    pool = [s["key"] for s in leaves if s["key"] not in picked]
    for key in rng.sample(pool, min(extra_random, len(pool))):
        add(key)
    return picked[:n]
