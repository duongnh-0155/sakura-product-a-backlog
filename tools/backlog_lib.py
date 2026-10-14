#!/usr/bin/env /usr/bin/python3
"""Shared helpers: load backlog YAML files, render issue bodies and labels.

Run with /usr/bin/python3 (has PyYAML)."""
import glob
import json
import os
import re
import sys

import yaml

CONSTRAINT_OPTION = {
    "BR-INC-01": "BR-INC-01 完納奨励金",
    "TBL-RATE-01": "TBL-RATE-01 料率版",
    "permit-vs-approval": "許可≠承認",
    "business-day": "業務日・締め",
    "post-close-correction": "締め後訂正",
    "none": "なし",
}
METRIC_KEYS = ["screens", "apis", "tables", "states", "rules", "integrations", "test_vectors"]
METRIC_LABELS = {
    "screens": "画面数", "apis": "API 数", "tables": "テーブル数", "states": "状態・遷移数",
    "rules": "業務ルール数", "integrations": "外部連携数", "test_vectors": "テストベクトル数",
}
DEP_RE = re.compile(r"\{\{DEP:([A-Za-z0-9\-]+)\}\}")


def load_backlog(dir_path):
    """Return list of feature dicts, sorted by file name, with keys validated."""
    feats = []
    seen = set()
    for path in sorted(glob.glob(os.path.join(dir_path, "[!_]*.yaml"))):
        with open(path, encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        data["_file"] = os.path.basename(path)
        for key in iter_keys(data):
            if key in seen:
                raise ValueError(f"duplicate key {key} in {path}")
            seen.add(key)
        feats.append(data)
    return feats


def iter_keys(feat):
    yield feat["epic"]["key"]
    for iss in feat.get("issues", []):
        yield iss["key"]
        for sub in iss.get("sub_issues", []) or []:
            yield sub["key"]


def iter_items(feat):
    """Yield (level, item, parent_key) for epic, issues, sub-issues."""
    epic = feat["epic"]
    yield "Epic", epic, None
    for iss in feat.get("issues", []):
        yield "Issue", iss, epic["key"]
        for sub in iss.get("sub_issues", []) or []:
            yield "Sub-issue", sub, iss["key"]


def metrics_line(metrics):
    m = {k: int((metrics or {}).get(k, 0) or 0) for k in METRIC_KEYS}
    return "<!-- swp-metrics: " + " ".join(f"{k}={m[k]}" for k in METRIC_KEYS) + " -->"


def metrics_table(metrics):
    m = {k: int((metrics or {}).get(k, 0) or 0) for k in METRIC_KEYS}
    rows = "\n".join(f"| {METRIC_LABELS[k]} | {m[k]} |" for k in METRIC_KEYS)
    return "## 規模指標（SWP 算定の根拠）\n\n| 指標 | 値 |\n|---|---|\n" + rows


def render_body(level, item, feat, parent_key=None):
    """Compose the GitHub issue body. Dependencies stay as {{DEP:KEY}} placeholders."""
    parts = [item.get("body", "").rstrip()]
    meta = []
    if item.get("specs"):
        meta.append("- 対象スペック: " + ", ".join(f"`{s}`" for s in item["specs"]))
    if item.get("pf"):
        meta.append(f"- 業務フロー: {item['pf']}")
    if item.get("phase"):
        meta.append(f"- フェーズ: {item['phase']}")
    if item.get("depends_on"):
        meta.append("- 依存: " + ", ".join("{{DEP:%s}}" % d for d in item["depends_on"]))
    if parent_key:
        meta.append("- 親: {{DEP:%s}}" % parent_key)
    if meta:
        parts.append("## メタ情報\n\n" + "\n".join(meta))
    if level != "Epic":
        parts.append(metrics_table(item.get("metrics")))
        parts.append(metrics_line(item.get("metrics")))
    parts.append(f"<!-- backlog-key: {item['key']} | feature: {feat['feature']} | level: {level} -->")
    return "\n\n".join(p for p in parts if p)


def labels_for(level, item, feat, parent=None):
    labels = {f"feature:{feat['feature']}"}
    if level == "Epic":
        labels.add("epic")
    typ = item.get("type") or (parent or {}).get("type")
    if typ:
        labels.add(f"type:{typ}")
    pri = item.get("priority") or (parent or {}).get("priority")
    if pri:
        labels.add(f"priority:{str(pri).lower()}")
    con = item.get("constraint") or (parent or {}).get("constraint") or "none"
    if con != "none":
        labels.add(f"constraint:{con}")
    return sorted(labels)


def load_map(path):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    return {}


def save_map(path, data):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1, sort_keys=True)
    os.replace(tmp, path)


def summary(feats):
    n_e = n_i = n_s = 0
    for f in feats:
        n_e += 1
        for iss in f.get("issues", []):
            n_i += 1
            n_s += len(iss.get("sub_issues", []) or [])
    return n_e, n_i, n_s


if __name__ == "__main__":
    feats = load_backlog(sys.argv[1] if len(sys.argv) > 1 else "backlog")
    e, i, s = summary(feats)
    print(f"features={e} issues={i} sub_issues={s} total={e + i + s}")
    for f in feats:
        print(f"  {f['feature']:28} issues={len(f.get('issues', [])):3} subs={sum(len(x.get('sub_issues') or []) for x in f.get('issues', [])):3}")
