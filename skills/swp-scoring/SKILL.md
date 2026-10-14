---
name: swp-scoring
description: GitHub Project v2（または push 前のローカル backlog YAML）の Epic / Issue / Sub-issue に Story Weight Point（SWP = Scope × Complexity → フィボナッチ切り上げ、親は子の合計）を付け、日本語 HTML レポートと JSON を出力し、人手レビュー用サンプル issue を選ぶ。レポートのみ生成し Project には書かない。レビュー後の反映は別コマンド write-points（既定 dry-run）。
triggers:
  - "SWP を採点"
  - "SWP チェック"
  - "ストーリーポイントを付けて"
  - "chấm SWP"
  - "chấm điểm backlog"
  - "score backlog points"
  - "swp report"
---

# swp-scoring — SWP 採点スキル

## 何をするか

1. **fetch** — GitHub Project v2（owner `duongnh-0155`、project #1）の全アイテムを `gh api graphql` で取得（100 件/ページで全件）。
   Issue ごとに number / title / body / labels / state / parent / subIssues / フィールド値
   （Point, Hours, Level, Priority, Constraint, 担当, Status, Sprint）を `items.json` に保存。
   `--from-yaml DIR` を付けると GitHub に触らず、ローカルの backlog YAML（epic → issues → sub_issues）から同じ形式を作る（push 前の dry-run 用）。
2. **score** — `items.json` を採点して `swp-report.html`（日本語、CSS インライン、CDN なし）と `swp-scores.json` を出力。
   レビュー用サンプル issue を決定的（seed）に選ぶ。**GitHub には一切書かない。**
3. **write-points** — 人がレビュー・修正した `swp-scores.json` を Project の `Point` 欄へ反映する。
   **既定は dry-run**。`--apply` を付けたときだけ `updateProjectV2ItemFieldValue` を実行する。
   field ID / project ID は `tools/project-fields.json` から読む（ハードコードしない）。

## 採点ルール（確定版）

- 入力は Issue 本文の `<!-- swp-metrics: screens= apis= tables= states= rules= integrations= test_vectors= -->`
  （YAML からは `metrics` ブロック）。行が無い葉は **missing** として Scope=Complexity=1 で仮採点し警告。
- Scope raw = screens×2 + apis×1 + tables×1.5 + integrations×2 → raw ≤2:1 / ≤4:2 / ≤7:3 / ≤11:4 / >11:5
- Complexity raw = states×1 + rules×1.5 + integrations×2 + test_vectors×0.5
  + 2（constraint ≠ none/なし）+ 1（type が tech / migration）→ raw ≤2:1 / ≤5:2 / ≤9:3 / ≤14:4 / >14:5
  （上記は既定値。`calibrate` を実行すると `references/calibration.json` の境界が優先される — 下記「校正」）
  - constraint は `constraint:*` ラベル → Project の Constraint 欄 → YAML `constraint` の順で解決
  - type は `type:*` ラベル → YAML `type`
- 葉の SWP = Scope × Complexity を **フィボナッチ [1,2,3,5,8,13,21,34] に切り上げ**
- 子を持つアイテム（Epic、sub-issue を持つ Issue）の SWP = **子の SWP 合計**（直接採点しない）。
  親子は GitHub の `parent` / `subIssues`、YAML では入れ子から取る。
- サンプル選定（seed 既定 42、既定上限 30）：各エピックの SWP 最大・最小の葉 ＋ constraint ≠ none の葉（エピックごと最大 2）
  ＋ 乱択 5 件、重複除去。
- 段階ごとの目安とアンカー例は `references/rubric.md`。

## 実行方法

**必ず `/usr/bin/python3` を使う**（PyYAML 入り。Homebrew の python には yaml が無い）。依存は標準ライブラリ + PyYAML のみ。
`gh` は `/opt/homebrew/bin/gh`（`gh auth login -s project,repo,read:org` 済みであること）。

```bash
cd <repo root>
S=skills/swp-scoring/scripts

# (a) GitHub Project から取得
/usr/bin/python3 $S/swp_cli.py fetch --owner duongnh-0155 --number 1 --out swp-report/items.json
# (a') ローカル YAML で dry-run（push 前チェック）
/usr/bin/python3 $S/swp_cli.py fetch --from-yaml ../plans/<plan>/backlog --out /tmp/items.json

# (b) 採点 → HTML + JSON（GitHub には書かない）
/usr/bin/python3 $S/swp_cli.py score --in swp-report/items.json --out-dir swp-report --sample 30 --seed 42

# (c) 人手レビュー：swp-report.html §4 を見て swp-scores.json の該当キーに final_swp / reason を追記

# (d) 反映（既定 dry-run。--apply で実書き込み）
/usr/bin/python3 $S/swp_cli.py write-points --scores swp-report/swp-scores.json --items swp-report/items.json --fields tools/project-fields.json
/usr/bin/python3 $S/swp_cli.py write-points --scores swp-report/swp-scores.json --items swp-report/items.json --fields tools/project-fields.json --apply

# テスト
/usr/bin/python3 -m unittest discover -s $S -p 'test_*.py' -v
```

## 入出力

| ファイル | 内容 |
|---|---|
| `items.json` | `{source, project|source_path, items:[{key, number, item_id, title, body, labels, state, level, type, constraint, parent, children, fields, metrics}]}` |
| `swp-report.html` | 1 概要 / 2 エピック別（エピック・Issue 数・SWP 合計）/ 3 全アイテム（番号・タイトル・Level・Scope・Complexity・積・SWP・親・制約・根拠 metrics）/ 4 レビュー用サンプル（確定 SWP・理由は空欄）/ 5 採点方法 |
| `swp-scores.json` | `{seed, samples:[key…], scores:{key:{scope, complexity, product, swp, is_leaf, children, parent, epic, metrics, missing, item_id, sample?}}}`。人は `final_swp`, `reason` を追加する |

## 制限・注意

- **score は報告のみ。Project の Point は書かない。** 書くのは人のレビュー後に `write-points --apply` を明示したときだけ（課題の「AI Agent が確定 SWP を書く」工程）。
- `write-points` は `final_swp` > `reviewed_swp` > `swp` の優先で値を取り、現在の Point と同じなら skip。
- GitHub 側で `Level` 欄が未設定なら、`epic` ラベル / parent / subIssues から Level を推定する。
- DraftIssue・Pull Request は採点対象外（スキップ）。
- 公開リポジトリ前提：スクリプトにトークン・環境 URL・個人情報を書かない。認証は `gh` に任せる。
- Python 3.9 互換（macOS 標準）で書く。1 ファイル 200 行未満。

## ファイル構成

```
skills/swp-scoring/
├── SKILL.md
├── references/rubric.md          # Scope / Complexity のアンカー表
└── scripts/
    ├── swp_cli.py                # fetch / score / write-points
    ├── fetch_project.py          # gh api graphql（読み取りのみ）
    ├── backlog_yaml.py           # ローカル YAML → items.json
    ├── score.py                  # 採点の純関数（import 可）
    ├── report_html.py            # 日本語 HTML レンダリング
    ├── write_points.py           # Point 欄の更新（dry-run 既定）
    └── test_score.py             # unittest
```

## 校正（calibrate、D-15）

重みは固定のまま、段階の境界 4 つを「このバックログの葉の raw の 20/40/60/80 パーセンタイル」に合わせる。
メトリクスの数え方が担当者ごとに広め・狭めにぶれても、相対順位で 1〜5 に散らすための措置。

```bash
/usr/bin/python3 skills/swp-scoring/scripts/swp_cli.py calibrate --in swp-report/items.json   # references/calibration.json を更新
/usr/bin/python3 skills/swp-scoring/scripts/swp_cli.py score --in swp-report/items.json --out-dir swp-report   # 校正値を自動適用
```

`--calibration none` で既定境界に戻せる。校正は「重み付け自体の妥当性」は保証しない。
画面・API・テーブルで測れない作業（インフラ構築、顧客確認）は低く出やすいので、レビュー用サンプルで必ず確認する。

