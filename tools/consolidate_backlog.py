#!/usr/bin/env /usr/bin/python3
"""Consolidate raw agent backlog into the version pushed to GitHub (decisions D-14, D-16, D-17).

- keep sub-issues only for type `tech` or strong constraints; fold others into a checklist
- merge all `clarify` issues of a feature into one `{PFX}-Q` issue (checklist, old keys kept)
- alias folded/merged keys in depends_on and gap refs; drop deps from work issues to clarify
Usage: /usr/bin/python3 tools/consolidate_backlog.py SRC_DIR DST_DIR
"""
import copy
import glob
import json
import os
import re
import sys

import yaml

STRONG = {"BR-INC-01", "TBL-RATE-01", "permit-vs-approval", "post-close-correction"}
CON_RANK = ["BR-INC-01", "TBL-RATE-01", "permit-vs-approval", "post-close-correction", "business-day", "none"]
PRI_RANK = ["Critical", "High", "Medium"]
TO_CLARIFY = {"GAP-ACC-02": "ACC", "GAP-RPT-06": "RPT"}   # D-16
KEY_RE = re.compile(r"\b([A-Z]{2,3}-\d{2}(?:-[a-z])?)\b")


class Dumper(yaml.SafeDumper):
    pass


Dumper.add_representer(str, lambda d, s: d.represent_scalar("tag:yaml.org,2002:str", s, style="|" if "\n" in s else None))


def first_section(body, heading):
    m = re.search(r"## " + heading + r"[^\n]*\n(.*?)(?=\n## |\Z)", body or "", re.S)
    return m.group(1).strip() if m else ""


def keep_subs(iss):
    return iss["type"] == "tech" or iss.get("constraint", "none") in STRONG


def fold(iss, alias):
    lines = ["## 作業分解（チェックリスト）", ""]
    for s in iss.get("sub_issues") or []:
        alias[s["key"]] = iss["key"]
        lines.append(f"- [ ] **{s['key']}** {s['title']}")
        for dod in re.findall(r"- \[ \] (.+)", first_section(s.get("body"), "完了の定義")):
            lines.append(f"  - {dod}")
    iss["body"] = iss["body"].rstrip() + "\n\n" + "\n".join(lines) + "\n"
    iss["sub_issues"] = []


def merge_clarify(feat, items, prefix, extra):
    key = f"{prefix}-Q"
    con = min((i.get("constraint", "none") for i in items), key=CON_RANK.index, default="none")
    pri = min((i["priority"] for i in items), key=PRI_RANK.index, default="High")
    lines = ["## 概要", "", f"`{feat['feature']}` の顧客・設計確認事項 {len(items) + len(extra)} 件をまとめた Issue。"
             "各項目は回答受領後にチェックし、反映先 Issue と PREMISE.md を更新する。", "", "## 確認項目", ""]
    specs, deps = [], []
    for i in items:
        lines.append(f"- [ ] **{i['key']}** {i['title']}（{i['priority']}・制約 {i.get('constraint', 'none')}）")
        summary = first_section(i.get("body"), "概要").splitlines()
        if summary:
            lines.append(f"  - {summary[0][:200]}")
        specs += [s for s in i.get("specs") or [] if s not in specs]
        deps += [d for d in i.get("depends_on") or [] if d not in deps]
    for gid, text in extra:
        lines.append(f"- [ ] **{gid}** {text[:200]}（設計上の矛盾のうち業務判断が必要なもの・D-16）")
    lines += ["", "## 完了の定義（DoD）", "", "- [ ] 全項目について発注者または設計責任者の回答を記録した",
              "- [ ] 回答を PREMISE.md・関連 Issue・テストケースに反映した",
              "- [ ] 回答待ちで着手した Issue は仮定を Issue 本文に明記し、回答後に差分を確認した",
              "", "## 備考", "", "元の確認 Issue のキーを項目名に残している（D-14）。実装 Issue は本 Issue に依存させない（D-17）。"]
    m = {k: 0 for k in ("screens", "apis", "tables", "states", "rules", "integrations", "test_vectors")}
    m["rules"] = len(items) + len(extra)
    return {"key": key, "title": f"確認事項（{feat['feature']}）— {len(items) + len(extra)} 件", "type": "clarify",
            "priority": pri, "constraint": con, "owner": "BrSE", "phase": 1, "specs": specs[:12],
            "depends_on": [], "metrics": m, "body": "\n".join(lines) + "\n", "sub_issues": [], "_deps_raw": deps}


def remap(text, alias):
    return KEY_RE.sub(lambda mm: alias.get(mm.group(1), mm.group(1)), text) if isinstance(text, str) else text


def main(src, dst):
    os.makedirs(dst, exist_ok=True)
    feats = [yaml.safe_load(open(p, encoding="utf-8")) | {"_file": os.path.basename(p)} for p in sorted(glob.glob(f"{src}/*.yaml"))]
    alias, clarify_keys = {}, set()
    for f in feats:
        prefix = f["epic"]["key"].split("-", 1)[1]
        cl = [i for i in f["issues"] if i["type"] == "clarify"]
        extra = [(g["id"], g["gap"]) for g in f.get("gaps") or [] if TO_CLARIFY.get(g["id"]) == prefix]
        work = [i for i in f["issues"] if i["type"] != "clarify"]
        for i in work:
            if i.get("sub_issues") and not keep_subs(i):
                fold(i, alias)
        if cl or extra:
            merged = merge_clarify(f, cl, prefix, extra)
            for i in cl:
                alias[i["key"]] = merged["key"]
            clarify_keys.add(merged["key"])
            work.append(merged)
            for g in f.get("gaps") or []:
                if g["id"] in TO_CLARIFY:
                    g["handling"], g["ref"] = "clarify-issue", f"{merged['key']}（{g['id']} を確認項目に追加、D-16）"
        f["issues"] = work
    for f in feats:
        for i in f["issues"]:
            for node in [i] + list(i.get("sub_issues") or []):
                deps = [alias.get(d, d) for d in node.get("depends_on") or []]
                if node.get("type", i["type"]) != "clarify":
                    deps = [d for d in deps if d not in clarify_keys]          # D-17
                node["depends_on"] = [d for j, d in enumerate(deps) if d not in deps[:j] and d != node["key"]]
            i.pop("_deps_raw", None)
        for g in f.get("gaps") or []:
            g["ref"] = remap(g.get("ref"), alias)
        out = {k: v for k, v in f.items() if not k.startswith("_")}
        with open(os.path.join(dst, f["_file"]), "w", encoding="utf-8") as fh:
            yaml.dump(out, fh, Dumper=Dumper, allow_unicode=True, sort_keys=False, width=1000)
    with open(os.path.join(dst, "_aliases.json"), "w", encoding="utf-8") as fh:
        json.dump(alias, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(f"aliases={len(alias)} clarify_issues={len(clarify_keys)}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
