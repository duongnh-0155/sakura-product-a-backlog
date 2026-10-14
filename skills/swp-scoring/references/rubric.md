# SWP 採点ルーブリック（Scope × Complexity）

SWP（Story Weight Point）は **Scope（広さ）1–5 × Complexity（難しさ）1–5** の積を
フィボナッチ数列 **1, 2, 3, 5, 8, 13, 21, 34** に切り上げた値。
子を持つアイテム（Epic、sub-issue を持つ Issue）は **子の SWP 合計**で、直接採点しない。

## 入力：Issue 本文の metrics 行

```
<!-- swp-metrics: screens=1 apis=2 tables=2 states=4 rules=3 integrations=1 test_vectors=6 -->
```

| キー | 数えるもの（スペックから数える。推測で盛らない） |
|---|---|
| screens | 触る画面（SCR）の数。部分 UI のみなら 0 でもよい |
| apis | 実装・呼び出しに関わる API の本数 |
| tables | 作成・変更・参照で設計上触れるテーブル数 |
| states | 扱う状態・遷移の数（例：下書き→申請→承認→差戻し = 4） |
| rules | 複雑な業務ルール・バリデーションの数（単純必須チェックは数えない） |
| integrations | 外部連携の数（SFTP、メール、Entra、PWA 同期、プリンタ…） |
| test_vectors | TECH / SPEC に書かれたテストベクトル・境界ケースの数 |

欠落時は **Scope=Complexity=1（SWP 1）で仮採点し警告**。本文に行を追記して再採点する。

## Scope（広さ）

`raw = screens×2 + apis×1 + tables×1.5 + integrations×2`

| Scope | raw | 目安（アンカー） | 例 |
|---|---|---|---|
| 1 | ≤ 2 | 画面 1 枚の静的 UI、API 1〜2 本のみ、テーブル 0〜1、連携なし | 「SCR-xxx 静的 UI・項目定義」sub-issue、顧客確認 issue（clarify）、`rule_config` の 1 行追加 |
| 2 | ≤ 4 | 画面 1 枚 + API 1〜2 本、または API 2〜3 本 + テーブル 1 | 一覧画面 1 枚と参照 API 2 本、参照系 API 群 |
| 3 | ≤ 7 | 画面 1 枚 + API 2〜3 本 + テーブル 1〜2、または API 4〜5 本 + テーブル 2、連携 1 本を含む小さな塊 | 登録＋詳細の画面 1 枚と API 3 本、メール送信 1 本 |
| 4 | ≤ 11 | 画面 2 枚 or API 6〜8 本 + テーブル 2〜3、または連携 1 本 + 画面 + API | リソース単位の API 群（6〜7 本）、DB migration（テーブル 4〜5） |
| 5 | > 11 | 画面 3 枚以上、API 6 本超、テーブル 6 本超、連携 2 本以上 | 大型 migration（partition・trigger 付き）、PWA オフライン同期一式 |

## Complexity（難しさ）

`raw = states×1 + rules×1.5 + integrations×2 + test_vectors×0.5 + 2（制約 ≠ none）+ 1（type が tech / migration）`

| Complexity | raw | 目安（アンカー） | 例 |
|---|---|---|---|
| 1 | ≤ 2 | 状態 0〜2、ルールなし、テストベクトル 0〜2 | 静的 UI、固定表示の帳票レイアウト、簡単な必須チェック |
| 2 | ≤ 5 | 状態 2〜3 + ルール 1〜2、テストベクトル 3〜4 | ログイン画面（成功／失敗／ロック）、必須＋形式＋相関チェック |
| 3 | ≤ 9 | 状態 3〜4 + ルール 2〜3 + テストベクトル 4〜6、または制約 1 つ付きの登録 API | 申請→承認→差戻しの遷移、業務日チェック付き登録 API |
| 4 | ≤ 14 | 状態 4〜5 + ルール 3〜4 + テストベクトル 6〜10 + 制約 + tech | 料率版の切替（TBL-RATE-01）、締め後訂正の reverse/delta |
| 5 | > 14 | 業務ロジック（tech）+ ルール 5 以上 + 境界テスト 10 件以上 + 制約 | 完納奨励金計算 FUNC（BR-INC-01、DS-INC-EDGE-01、テストベクトル 12 件） |

### 制約（constraint）の扱い

`constraint:*` ラベル／Project の Constraint 欄／YAML の `constraint` のいずれかが
`none`・`なし` 以外なら **+2**。対象：BR-INC-01、TBL-RATE-01、permit-vs-approval（許可≠承認）、
business-day（業務日・締め）、post-close-correction（締め後訂正）。
理由：これらは仕様の読み違えが起きやすく、レビューと境界テストが必ず増えるため。

### type の扱い

`type:tech`（業務ロジック + テストベクトル）と `type:migration` は **+1**。
データ整合・ロールバック・境界条件の検証が通常の fe / be より重いため。

## 積 → SWP

| 積 | 1 | 2 | 3 | 4 | 5–6 | 7–8 | 9–12 | 13–15 | 16–20 | 21–25 |
|---|---|---|---|---|---|---|---|---|---|---|
| SWP | 1 | 2 | 3 | 5 | 5–8 | 8 | 13 | 21 | 21 | 34 |

（切り上げなので 4→5、6→8、9→13、15→21、25→34）

## 人手レビューの観点

- 同じ Scope / Complexity の issue 同士で体感の重さが揃っているか（相対評価）。
- metrics の数え方が issue 間で一貫しているか（API を数え落としていないか等）。
- 制約付きなのに `constraint: none` になっていないか（+2 の漏れ）。
- 親の SWP が子の合計になっているか。sub-issue を切った Issue 自身の metrics は使われない。
- 変更する場合は `swp-scores.json` の該当キーに `final_swp` と `reason` を書く。変更しない場合も理由を残す。

## 校正後の境界（本バックログ、2026-10-14）

`references/calibration.json` に保存。341 葉の raw 分位点から算出。

| 軸 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Scope raw | ≤ 3 | ≤ 7.5 | ≤ 12.5 | ≤ 19 | > 19 |
| Complexity raw | ≤ 12.5 | ≤ 18 | ≤ 23 | ≤ 29 | > 29 |

上の「目安（アンカー）」表は既定境界での説明。校正後は同じ段階でも raw の幅が広い。
既知の弱点: インフラ・顧客確認の Issue は metrics が小さく SWP 1 になりやすい（サンプルレビューで補正）。

