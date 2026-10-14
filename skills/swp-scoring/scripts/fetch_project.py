"""Fetch GitHub Project v2 items via `gh api graphql` and normalize to the flat item schema.

Read-only. Requires `gh auth login -s project,repo,read:org`. No token is stored here.
"""
from __future__ import annotations

import json
import subprocess
from typing import Dict, List, Optional

GH_BIN = "/opt/homebrew/bin/gh"
PAGE_SIZE = 100
TRACKED_FIELDS = ("Point", "Hours", "Level", "Priority", "Constraint", "担当", "Status", "Sprint")

QUERY = """
query($owner: String!, $number: Int!, $cursor: String) {
  user(login: $owner) {
    projectV2(number: $number) {
      id title
      items(first: %d, after: $cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          id
          content {
            __typename
            ... on Issue {
              number title body state url
              repository { nameWithOwner }
              labels(first: 40) { nodes { name } }
              parent { number }
              subIssues(first: 50) { nodes { number } }
            }
          }
          fieldValues(first: 30) {
            nodes {
              __typename
              ... on ProjectV2ItemFieldNumberValue { number field { ... on ProjectV2FieldCommon { name } } }
              ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2FieldCommon { name } } }
              ... on ProjectV2ItemFieldIterationValue { title field { ... on ProjectV2FieldCommon { name } } }
              ... on ProjectV2ItemFieldTextValue { text field { ... on ProjectV2FieldCommon { name } } }
            }
          }
        }
      }
    }
  }
}
""" % PAGE_SIZE


def gh_graphql(query: str, variables: Dict[str, object], gh_bin: str = GH_BIN) -> dict:
    cmd = [gh_bin, "api", "graphql", "-H", "GraphQL-Features: sub_issues", "-f", "query=%s" % query]
    for k, v in variables.items():
        if v is None:
            continue
        cmd += ["-F" if isinstance(v, (int, float)) else "-f", "%s=%s" % (k, v)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError("gh api graphql failed: %s" % proc.stderr.strip())
    data = json.loads(proc.stdout)
    if data.get("errors"):
        raise RuntimeError("GraphQL errors: %s" % json.dumps(data["errors"], ensure_ascii=False))
    return data["data"]


def _field_values(nodes: List[dict]) -> Dict[str, object]:
    out: Dict[str, object] = {}
    for n in nodes or []:
        name = ((n.get("field") or {}).get("name"))
        if not name:
            continue
        out[name] = n.get("number", n.get("name", n.get("title", n.get("text"))))
    return out


def _label_value(labels: List[str], prefix: str) -> Optional[str]:
    for l in labels:
        if l.startswith(prefix):
            return l[len(prefix):]
    return None


def normalize_item(node: dict) -> Optional[dict]:
    content = node.get("content") or {}
    if content.get("__typename") != "Issue":
        return None  # DraftIssue / PR are not scored
    labels = [l["name"] for l in (content.get("labels") or {}).get("nodes", [])]
    fields = {k: v for k, v in _field_values((node.get("fieldValues") or {}).get("nodes", [])).items()
              if k in TRACKED_FIELDS}
    parent = (content.get("parent") or {}).get("number")
    children = [str(c["number"]) for c in (content.get("subIssues") or {}).get("nodes", [])]
    level = fields.get("Level") or ("Epic" if "epic" in labels else ("Sub-issue" if parent and not children else "Issue"))
    constraint = _label_value(labels, "constraint:") or fields.get("Constraint") or "none"
    return {
        "key": str(content["number"]), "number": content["number"], "item_id": node["id"],
        "title": content.get("title", ""), "body": content.get("body") or "", "url": content.get("url"),
        "repository": (content.get("repository") or {}).get("nameWithOwner"),
        "labels": labels, "state": content.get("state"), "level": level,
        "type": _label_value(labels, "type:"), "constraint": constraint,
        "parent": str(parent) if parent else None, "children": children, "fields": fields,
        "metrics": None,  # parsed from body by score.py
        "feature": _label_value(labels, "feature:"),
    }


def fetch_project(owner: str, number: int, gh_bin: str = GH_BIN) -> Dict[str, object]:
    cursor: Optional[str] = None
    items: List[dict] = []
    project_id = title = None
    while True:
        data = gh_graphql(QUERY, {"owner": owner, "number": number, "cursor": cursor}, gh_bin)
        proj = data["user"]["projectV2"]
        project_id, title = proj["id"], proj["title"]
        for node in proj["items"]["nodes"]:
            it = normalize_item(node)
            if it:
                items.append(it)
        page = proj["items"]["pageInfo"]
        if not page["hasNextPage"]:
            break
        cursor = page["endCursor"]
    return {"source": "github", "project": {"owner": owner, "number": number, "id": project_id, "title": title},
            "items": items}
