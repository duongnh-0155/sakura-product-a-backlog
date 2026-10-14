"""Write reviewed SWP into the Project's `Point` field (updateProjectV2ItemFieldValue).

Dry-run by default; nothing is sent unless apply=True. The field/project IDs come from
tools/project-fields.json (output of `gh api graphql` field listing), never hard-coded.
"""
from __future__ import annotations

import json
from typing import Dict, List, Optional

from fetch_project import GH_BIN, gh_graphql

MUTATION = """
mutation($project: ID!, $item: ID!, $field: ID!, $value: Float!) {
  updateProjectV2ItemFieldValue(input: {projectId: $project, itemId: $item, fieldId: $field, value: {number: $value}}) {
    projectV2Item { id }
  }
}
"""


def load_field_ids(path: str, field_name: str = "Point") -> Dict[str, str]:
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    nodes = (data.get("fields") or {}).get("nodes", [])
    field = next((n for n in nodes if n.get("name") == field_name), None)
    if not field or not data.get("id"):
        raise ValueError("field '%s' or project id not found in %s" % (field_name, path))
    return {"project_id": data["id"], "field_id": field["id"]}


def final_swp(entry: dict) -> Optional[float]:
    """Reviewed value wins: final_swp > reviewed_swp > swp."""
    for k in ("final_swp", "reviewed_swp", "swp"):
        if entry.get(k) is not None:
            return float(entry[k])
    return None


def reaggregate(scores: Dict[str, dict]) -> Dict[str, dict]:
    """Parents are always the sum of their children; recompute after human edits to leaf final_swp."""
    def eff(key: str, stack: tuple) -> float:
        e = scores[key]
        kids = [c for c in (e.get("children") or []) if c in scores and c not in stack]
        if kids:
            e["final_swp"] = sum(eff(c, stack + (key,)) for c in kids)
        return final_swp(e) or 0.0
    for k in scores:
        eff(k, ())
    return scores


def plan_writes(scores: Dict[str, dict], items_by_key: Dict[str, dict], current: Optional[Dict[str, object]] = None) -> List[dict]:
    """Build the write list: one row per item with a project item id. Skips unchanged values."""
    rows: List[dict] = []
    reaggregate(scores)
    for key, entry in sorted(scores.items()):
        item = items_by_key.get(key) or {}
        item_id = entry.get("item_id") or item.get("item_id")
        value = final_swp(entry)
        if item_id is None or value is None:
            rows.append({"key": key, "item_id": item_id, "value": value, "status": "skip:no-item-id-or-value"})
            continue
        before = (item.get("fields") or {}).get("Point") if current is None else current.get(key)
        status = "unchanged" if before is not None and float(before) == value else "write"
        rows.append({"key": key, "title": entry.get("title") or item.get("title", ""), "item_id": item_id,
                     "before": before, "value": value, "status": status})
    return rows


def apply_writes(rows: List[dict], ids: Dict[str, str], gh_bin: str = GH_BIN) -> List[dict]:
    done: List[dict] = []
    for r in rows:
        if r["status"] != "write":
            continue
        try:
            gh_graphql(MUTATION, {"project": ids["project_id"], "item": r["item_id"], "field": ids["field_id"],
                                  "value": int(r["value"]) if float(r["value"]).is_integer() else r["value"]}, gh_bin)  # gh -F types ints only
            r["status"] = "written"
        except RuntimeError as exc:  # keep going, report at the end
            r["status"] = "error: %s" % exc
        done.append(r)
    return done
