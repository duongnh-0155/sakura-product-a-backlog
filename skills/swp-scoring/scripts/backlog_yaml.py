"""Load local backlog YAML files (epic -> issues -> sub_issues) into the flat item schema.

Used for dry-run scoring before anything is pushed to GitHub.
Schema reference: plans/.../break-task-brief.md §Schema YAML.
Run with /usr/bin/python3 (has PyYAML).
"""
from __future__ import annotations

import glob
import os
from typing import Dict, List, Optional

import yaml


def _norm_constraint(value: Optional[str]) -> str:
    v = (value or "none").strip()
    return v if v else "none"


def _mk_item(node: dict, level: str, parent: Optional[str], feature: str) -> dict:
    return {
        "key": str(node.get("key")),
        "number": None,
        "item_id": None,
        "title": node.get("title", ""),
        "body": node.get("body", "") or "",
        "labels": [l for l in [
            "epic" if level == "Epic" else None,
            "feature:%s" % feature if feature else None,
            "type:%s" % node["type"] if node.get("type") else None,
            "constraint:%s" % _norm_constraint(node.get("constraint")),
            "priority:%s" % node["priority"] if node.get("priority") else None,
        ] if l],
        "state": "OPEN",
        "level": level,
        "type": node.get("type"),
        "constraint": _norm_constraint(node.get("constraint")),
        "parent": parent,
        "children": [],
        "fields": {
            "Level": level,
            "Priority": node.get("priority"),
            "Constraint": _norm_constraint(node.get("constraint")),
            "担当": node.get("owner"),
            "Status": "Backlog",
        },
        "metrics": node.get("metrics"),
        "feature": feature,
    }


def load_backlog_file(path: str) -> List[dict]:
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
    feature = str(data.get("feature") or os.path.splitext(os.path.basename(path))[0])
    items: List[dict] = []
    epic = data.get("epic") or {}
    epic_key = str(epic.get("key") or "EPIC-%s" % feature.upper())
    epic_item = _mk_item({**epic, "key": epic_key}, "Epic", None, feature)
    items.append(epic_item)
    for issue in data.get("issues") or []:
        iss = _mk_item(issue, "Issue", epic_key, feature)
        epic_item["children"].append(iss["key"])
        items.append(iss)
        for sub in issue.get("sub_issues") or []:
            s = _mk_item(sub, "Sub-issue", iss["key"], feature)
            s["type"] = s["type"] or iss["type"]
            # sub-issue inherits the parent's constraint unless it sets its own
            if "constraint" not in sub:
                s["constraint"] = iss["constraint"]
                s["fields"]["Constraint"] = iss["constraint"]
            iss["children"].append(s["key"])
            items.append(s)
    return items


def load_backlog_dir(directory: str) -> Dict[str, object]:
    files = sorted(glob.glob(os.path.join(directory, "*.yaml")) + glob.glob(os.path.join(directory, "*.yml")))
    items: List[dict] = []
    seen: Dict[str, str] = {}
    for f in files:
        for it in load_backlog_file(f):
            if it["key"] in seen:
                raise ValueError("duplicate key %s in %s and %s" % (it["key"], seen[it["key"]], f))
            seen[it["key"]] = f
            items.append(it)
    return {"source": "yaml", "source_path": os.path.abspath(directory), "files": [os.path.basename(f) for f in files], "items": items}
