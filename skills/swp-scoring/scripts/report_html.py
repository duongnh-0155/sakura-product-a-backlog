"""Render the Japanese SWP report as a self-contained HTML string (inline CSS, no CDN)."""
from __future__ import annotations

import html
from datetime import datetime
from typing import Dict, List

CSS = """
body{font-family:-apple-system,"Hiragino Sans","Noto Sans JP",sans-serif;margin:24px;color:#222;font-size:14px}
h1{font-size:22px;border-bottom:2px solid #345;padding-bottom:6px}h2{font-size:17px;margin-top:32px;border-left:5px solid #345;padding-left:8px}
table{border-collapse:collapse;width:100%;margin:8px 0 16px}th,td{border:1px solid #ccd;padding:4px 6px;vertical-align:top}
th{background:#eef1f6;text-align:left;white-space:nowrap}td.n{text-align:right;white-space:nowrap}
tr.epic td{background:#f6f3e8;font-weight:600}tr.miss td{background:#fdecec}tr.sample td{background:#eef9ee}
.kpi{display:inline-block;border:1px solid #ccd;border-radius:6px;padding:8px 14px;margin:4px 8px 4px 0;background:#fafbfd}
.kpi b{display:block;font-size:20px}.warn{color:#a00}.blank{min-width:90px;height:22px;background:#fff}
code{background:#f3f3f3;padding:1px 4px;border-radius:3px}small{color:#666}
"""
LEVEL_ORDER = {"Epic": 0, "Issue": 1, "Sub-issue": 2}


def _e(v) -> str:
    return html.escape("" if v is None else str(v))


def _metrics_str(m) -> str:
    if not m:
        return "—"
    return " ".join("%s=%s" % (k[:3] if k != "test_vectors" else "tv", v) for k, v in m.items())


def _tree_order(scores: Dict[str, dict]) -> List[dict]:
    """Depth-first order: epic, its issues, their sub-issues; orphans last."""
    out: List[dict] = []
    roots = sorted((s for s in scores.values() if not s["parent"]), key=lambda s: (LEVEL_ORDER.get(s["level"], 9), s["key"]))

    def walk(s: dict) -> None:
        out.append(s)
        for c in sorted(s["children"], key=lambda k: scores[k]["key"]):
            walk(scores[c])
    for r in roots:
        walk(r)
    return out


def _row(s: dict, sample: set) -> str:
    cls = " ".join(c for c in ["epic" if s["level"] == "Epic" else "", "miss" if s["missing"] else "",
                               "sample" if s["key"] in sample else ""] if c)
    num = s["number"] if s["number"] is not None else s["key"]
    prod = "" if s["product"] is None else s["product"]
    basis = _metrics_str(s["metrics"]) if s["is_leaf"] else "子 %d 件の合計" % len(s["children"])
    if s["warnings"]:
        basis += ' <span class="warn">⚠ %s</span>' % _e("; ".join(s["warnings"]))
    return "<tr class='%s'><td>%s</td><td>%s</td><td>%s</td><td class='n'>%s</td><td class='n'>%s</td><td class='n'>%s</td><td class='n'><b>%s</b></td><td>%s</td><td>%s</td><td><small>%s</small></td></tr>" % (
        cls, _e(num), _e(s["title"]), _e(s["level"]), _e(s["scope"] or ""), _e(s["complexity"] or ""), _e(prod),
        s["swp"], _e(s["parent"] or ""), _e(s["constraint"]), basis)


def _bounds(th) -> str:
    th = list(th or [])
    parts = ["raw≤%g:%d" % (v, i + 1) for i, v in enumerate(th)]
    return " / ".join(parts + ["&gt;%g:5" % th[-1]]) if th else ""


def render_report(scores: Dict[str, dict], samples: List[str], meta: dict) -> str:
    ordered = _tree_order(scores)
    leaves = [s for s in ordered if s["is_leaf"]]
    epics = [s for s in ordered if not s["parent"]]
    total = sum(s["swp"] for s in epics)
    missing = [s for s in leaves if s["missing"]]
    sample = set(samples)
    p: List[str] = ["<!doctype html><html lang='ja'><head><meta charset='utf-8'><title>SWP 採点レポート</title><style>%s</style></head><body>" % CSS]
    p.append("<h1>SWP（Story Weight Point）採点レポート</h1>")
    p.append("<p><small>生成: %s ／ ソース: %s ／ seed=%s</small></p>" % (
        _e(datetime.now().strftime("%Y-%m-%d %H:%M")), _e(meta.get("source_label", "")), _e(meta.get("seed"))))
    p.append("<h2>1. 概要</h2>")
    for label, val in [("エピック数", len(epics)), ("アイテム総数", len(ordered)), ("葉（直接採点）", len(leaves)),
                       ("SWP 合計", total), ("metrics 欠落", len(missing)), ("レビュー対象サンプル", len(samples))]:
        p.append("<span class='kpi'>%s<b>%s</b></span>" % (label, val))
    if missing:
        p.append("<p class='warn'>⚠ %d 件の葉に <code>swp-metrics</code> 行が無く、Scope=Complexity=1 で仮採点しています。本文に metrics を追記して再採点してください。</p>" % len(missing))
    p.append("<p>本レポートは <b>採点結果の提示のみ</b>を行い、Project の Point 欄は更新しません。人手レビュー後に別コマンド（write-points --apply）で反映します。</p>")
    p.append("<h2>2. エピック別集計</h2><table><tr><th>エピック</th><th>Issue 数</th><th>Sub-issue 数</th><th>葉の数</th><th>SWP 合計</th></tr>")
    for ep in epics:
        sub = [s for s in ordered if s["epic"] == ep["key"] and s["key"] != ep["key"]]
        n_iss = sum(1 for s in sub if s["level"] == "Issue")
        n_sub = sum(1 for s in sub if s["level"] == "Sub-issue")
        n_leaf = sum(1 for s in sub if s["is_leaf"])
        p.append("<tr><td>%s %s</td><td class='n'>%d</td><td class='n'>%d</td><td class='n'>%d</td><td class='n'><b>%d</b></td></tr>" % (
            _e(ep["number"] if ep["number"] is not None else ep["key"]), _e(ep["title"]), n_iss, n_sub, n_leaf, ep["swp"]))
    p.append("<tr><th>合計</th><th></th><th></th><th class='n'>%d</th><th class='n'>%d</th></tr></table>" % (len(leaves), total))
    p.append("<h2>3. 全アイテム一覧</h2><p><small>緑＝レビュー用サンプル、赤＝metrics 欠落。親（Epic / sub-issue を持つ Issue）は子の SWP 合計。</small></p>")
    p.append("<table><tr><th>番号</th><th>タイトル</th><th>Level</th><th>Scope</th><th>Complexity</th><th>積</th><th>SWP</th><th>親</th><th>制約</th><th>根拠 metrics</th></tr>")
    p.extend(_row(s, sample) for s in ordered)
    p.append("</table>")
    p.append("<h2>4. レビュー用サンプル（人手確認）</h2><p>各エピックの最大・最小 SWP の葉、制約付きの葉（エピックごと最大 2 件）、ランダム %d 件（seed=%s）。"
             "<b>確定 SWP</b> と <b>理由</b> を記入し、変更しない場合も「据え置き」と理由を書く。</p>" % (meta.get("extra_random", 5), _e(meta.get("seed"))))
    p.append("<table><tr><th>番号</th><th>タイトル</th><th>Scope</th><th>Complexity</th><th>SWP（採点）</th><th>制約</th><th>根拠 metrics</th><th>確定 SWP</th><th>理由</th></tr>")
    for k in samples:
        s = scores[k]
        p.append("<tr><td>%s</td><td>%s</td><td class='n'>%s</td><td class='n'>%s</td><td class='n'><b>%s</b></td><td>%s</td><td><small>%s</small></td><td><div class='blank'></div></td><td><div class='blank'></div></td></tr>" % (
            _e(s["number"] if s["number"] is not None else s["key"]), _e(s["title"]), s["scope"], s["complexity"], s["swp"], _e(s["constraint"]), _metrics_str(s["metrics"])))
    p.append("</table>")
    p.append("<h2>5. 採点方法</h2><ol>"
             "<li>各 Issue 本文の <code>&lt;!-- swp-metrics: screens= apis= tables= states= rules= integrations= test_vectors= --&gt;</code> を読む。</li>"
             "<li>Scope raw = screens×2 + apis×1 + tables×1.5 + integrations×2 → %s</li>"
             "<li>Complexity raw = states×1 + rules×1.5 + integrations×2 + test_vectors×0.5 + 2（制約≠none）+ 1（type が tech / migration）→ %s</li>"
             "<li>段階の境界は本バックログの葉の raw の 20/40/60/80 パーセンタイルで校正（D-15、<code>references/calibration.json</code>）。重みは固定。</li>"
             "<li>葉の SWP = Scope×Complexity をフィボナッチ（1,2,3,5,8,13,21,34）へ切り上げ。</li>"
             "<li>子を持つアイテム（Epic、sub-issue を持つ Issue）は子の SWP 合計。直接採点しない。</li>"
             "<li>metrics 行が無い葉は Scope=Complexity=1（SWP 1）で仮採点し警告を付ける。</li>"
             "<li>詳細な段階の目安は <code>skills/swp-scoring/references/rubric.md</code> を参照。</li></ol>"
             % (_bounds(meta.get("thresholds", {}).get("scope")), _bounds(meta.get("thresholds", {}).get("complexity"))))
    p.append("</body></html>")
    return "\n".join(p)
