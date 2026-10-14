#!/usr/bin/env /usr/bin/python3
"""Generate the table parts of task-breakdown.md / PREMISE.md from backlog YAML + issue map.

Writes markdown fragments into OUT_DIR; the hand-written parts of each document include them.
Usage: /usr/bin/python3 tools/gen_docs.py --dir BACKLOG --out OUT_DIR [--map tools/issue-map.json]
"""
import argparse
import json
import os
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from backlog_lib import load_backlog, load_map  # noqa: E402

KEY_RE = re.compile(r"\b([A-Z]{2,4}-(?:\d{2}(?:-[a-z])?|Q))\b")
CON_JA = {"BR-INC-01": "BR-INC-01 完納奨励金", "TBL-RATE-01": "TBL-RATE-01 料率版", "permit-vs-approval": "許可≠承認（BR-PERM-01）",
          "post-close-correction": "締め後訂正（reverse/delta・2 段階承認）", "business-day": "業務日・締め（OPEN 1 件・休市日・締め解除）"}
HANDLING_JA = {"design-change": "設計修正", "assumption": "仮定", "clarify-issue": "確認 Issue", "open": "保留"}


def cell(text, limit=None):
    t = re.sub(r"\s*\n\s*", " ", str(text or "")).replace("|", "／").strip()
    return t if not limit or len(t) <= limit else t[: limit - 1] + "…"


class Linker:
    def __init__(self, imap, aliases):
        self.imap, self.aliases = imap, aliases

    def num(self, key):
        k = key if key in self.imap else self.aliases.get(key, key)
        return f"#{self.imap[k]['number']}" if k in self.imap else None

    def ref(self, key):
        n = self.num(key)
        return f"{n} `{key}`" if n else f"`{key}`"

    def text(self, s):
        return KEY_RE.sub(lambda m: (self.num(m.group(1)) or m.group(1)) + ("" if self.num(m.group(1)) is None else f"（{m.group(1)}）"), str(s or ""))


def section(body, name):
    m = re.search(r"## " + name + r"[^\n]*\n(.*?)(?=\n## |\Z)", body or "", re.S)
    return m.group(1).strip() if m else ""


def spec_to_issue(feats, L):
    rows = ["| Spec（LAB-4 文書 ID） | Epic | Issue（sub-issue） | タスク化しなかった部分と理由 |", "|---|---|---|---|"]
    for f in feats:
        epic = f"{L.num(f['epic']['key']) or ''} {f['epic']['title'].replace('[Epic] ', '')}"
        for i in f["issues"]:
            subs = ", ".join(L.num(s["key"]) or s["key"] for s in i.get("sub_issues") or [])
            iss = f"{L.ref(i['key'])} {cell(i['title'], 50)}" + (f"（{subs}）" if subs else "")
            rows.append(f"| {cell(', '.join(i.get('specs') or []) or '—', 90)} | {cell(epic, 40)} | {iss} | — |")
        for nb in f.get("not_broken") or []:
            rows.append(f"| {cell(nb.get('spec'), 90)} | {cell(epic, 40)} | — | {cell(L.text(nb.get('why')), 160)} |")
    return "\n".join(rows)


def constraint_table(feats, L):
    rows = ["| 制約 | Issue | 分離した理由（Issue 本文 §備考 より） |", "|---|---|---|"]
    for con, label in CON_JA.items():
        for f in feats:
            for i in f["issues"]:
                if i.get("constraint") != con:
                    continue
                if i["type"] == "clarify":
                    keys = re.findall(r"\*\*([A-Z]{2,4}-\d{2}|GAP-[A-Z]+-\d{2})\*\*[^\n]*制約 " + re.escape(con), i["body"])
                    why = f"確認項目 {', '.join(keys)} が {label} の前提（回答で金額・資格・締めの扱いが変わる）。項目単位で回答を追跡するため確認 Issue 内でも制約ラベルを付ける。"
                    rows.append(f"| {label} | {L.ref(i['key'])} {cell(i['title'], 46)} | {cell(L.text(why), 220)} |")
                    continue
                why = section(i["body"], "備考")
                why = next((ln for ln in why.splitlines() if con.split("-")[0] in ln or "理由" in ln or "分離" in ln or "単独" in ln), why.splitlines()[0] if why else "")
                rows.append(f"| {label} | {L.ref(i['key'])} {cell(i['title'], 46)} | {cell(L.text(why), 220)} |")
    return "\n".join(rows)


def gaps_table(feats, L, premise_rows):
    rows = ["| ID | Spec | 穴・矛盾 | 処理 |", "|---|---|---|---|"]
    for f in feats:
        for g in f.get("gaps") or []:
            h = g.get("handling")
            if h in ("design-change", "assumption"):
                how = f"{HANDLING_JA[h]} → PREMISE.md {premise_rows[g['id']]}"
            elif h == "clarify-issue":
                how = f"確認 Issue 起票 {cell(L.text(g.get('ref')), 120)}"
            else:
                how = f"保留: {cell(L.text(g.get('ref')), 150)}"
            rows.append(f"| {g['id']} | {cell(g.get('spec'), 70)} | {cell(L.text(g.get('gap')), 200)} | {how} |")
    return "\n".join(rows)


def premise_tables(feats, L):
    dc = ["| # | Spec（文書） | 区分 | 前 → 後 | 理由（出典） | 影響 Issue |", "|---|---|---|---|---|---|"]
    asm = ["| # | 仮定 | Spec・RFP で開いている箇所 | Issue・見積への影響 |", "|---|---|---|---|"]
    index, n_dc, n_as = {}, 0, 0
    for f in feats:
        for g in f.get("gaps") or []:
            if g.get("handling") == "design-change":
                n_dc += 1
                rid = f"C-{n_dc:02d}"
                dc.append(f"| {rid} | {cell(g.get('spec'), 60)} | 修正 | 前: {cell(L.text(g.get('gap')), 150)}<br>後: {cell(L.text(g.get('ref')), 150)} "
                          f"| break 時に発見した穴（{g['id']}） | {cell(L.text(g.get('impact')), 120)} |")
                index[g["id"]] = rid
            elif g.get("handling") == "assumption":
                n_as += 1
                rid = f"A-{n_as:02d}"
                asm.append(f"| {rid} | {cell(L.text(g.get('ref')), 170)} | {cell(g.get('spec'), 50)}: {cell(L.text(g.get('gap')), 130)} "
                           f"| {cell(L.text(g.get('impact')), 120)} |")
                index[g["id"]] = rid
    return "\n".join(dc), "\n".join(asm), index


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--map", default="tools/issue-map.json")
    a = ap.parse_args()
    feats = load_backlog(a.dir)
    aliases = json.load(open(os.path.join(a.dir, "_aliases.json"), encoding="utf-8"))
    L = Linker(load_map(a.map), aliases)
    os.makedirs(a.out, exist_ok=True)
    dc, asm, index = premise_tables(feats, L)
    parts = {"spec-to-issue.md": spec_to_issue(feats, L), "constraints.md": constraint_table(feats, L),
             "gaps.md": gaps_table(feats, L, index), "premise-changes.md": dc, "premise-assumptions.md": asm}
    for name, text in parts.items():
        with open(os.path.join(a.out, name), "w", encoding="utf-8") as fh:
            fh.write(text + "\n")
        print(f"{name}: {text.count(chr(10)) - 1} rows")


if __name__ == "__main__":
    main()
