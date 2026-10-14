# Product A — 水産物卸売市場 業務支援システム バックログ（LAB-5）

**受講者コード:** nguyen.hong.duong ・ **課題:** Product A（架空の RFP「株式会社 桜水産市場」）

## 概要

- **分解元:** LAB-4 提出版の詳細設計（`specs/`、ブランチ `ver/lab4`、コミット `901af59`、2026-10-09 提出）。
- **PREMISE.md:** LAB-4 から**差分あり**。分解中に見つけた仕様の食い違い 25 件の修正・追加、仮定 71 件、方向の確定 9 件（LAB-4 へのレビューコメントは未受領）。
- **規模:** Epic **16**（LAB-4 の feature 13 ＋ 共通基盤・データ移行・インフラ）、Issue 264、Sub-issue 125。SWP 合計 4,411、見積 9,194 時間。
- **模擬したスプリント:** Sprint 01（2026-11-09〜11-20）を完了として、Sprint 02（11-23〜12-04）を 12-02 時点の進行中として Project に反映した。日付と進捗は架空。

## リンク

| 対象 | URL・パス |
|---|---|
| リポジトリ | <https://github.com/duongnh-0155/sakura-product-a-backlog> |
| GitHub Project | <https://github.com/users/duongnh-0155/projects/1> |
| SWP 採点レポート（HTML） | [swp-report/swp-report.html](swp-report/swp-report.html) |

リポジトリ・Project・Issue は、ログインしていない状態（cookie なしの HTTP 取得）で表示できることを 2026-10-14 に確認した。

## リポジトリ構成

| ファイル・フォルダ | 内容 |
|---|---|
| `README.md` | 本書 |
| `PREMISE.md` | LAB-4 提出版との差分（仕様の修正・追加、仮定、方向の確定） |
| `task-breakdown.md` | 分解の原則、仕様 → Issue の対応、固有制約の項目、仕様の穴・矛盾 |
| `estimate.md` | SWP サンプルのレビュー、時間への換算方法、epic 別合計、LAB-1 との比較 |
| `progress-report.md` | Sprint 01〜02 の進捗報告（状態、バーンダウン、遅延リスクと対応） |
| `AI-report.md` | AI の使い方、AI 出力のレビュー、振り返り |
| `swp-report/` | 採点スキルの出力（HTML レポート、採点 JSON、レビュー判断、取得した Project データ、計画 JSON） |
| `skills/swp-scoring/` | 自作の SWP 採点スキル（Scope × Complexity、校正、HTML 出力、Point 欄への書込み） |
| `tools/` | バックログの登録・紐付け・欄の設定、レビュー適用、時間換算とスプリント計画、模擬、文書の表生成のスクリプト |
| `sim/` | スプリント模擬のシナリオ、バーンダウン（SVG・JSON）、模擬後の Project 集計 |
| `.gitignore` | Python のキャッシュ等を除外 |

## 仕様 → Epic

| 仕様（LAB-4 のファイル・ID、または PREMISE の行） | Project の Epic（#番号 — 名前） | 備考（固有制約） |
|---|---|---|
| specs/identity-and-participants/（SCR-001〜011、IAM_DB・PARTY_DB） | #117 — E1 認証・参加者 | 許可≠承認（BR-PERM-01）14 Issue。外部アカウントのパスワード経路は確認中 |
| specs/lot-and-item-master/（SCR-012〜018） | #230 — E2 ロット・品目 | 業務日（ロット受付は OPEN の業務日のみ） |
| specs/negotiated-trade/（SCR-019〜023） | #251 — E3 相対取引 | 許可≠承認（確定時点の資格判定）、締め後訂正（取消・復元）。1 取引 ≤ 20 明細、ロット分割 1〜4 者 |
| specs/auction-result/（SCR-024〜026） | #22 — E4 せり | セッション確定で取引を生成。ロック順を修正（PREMISE C-04） |
| specs/delivery/（SCR-027〜032・067） | #84 — E5 引渡し | **完納奨励金**: 完納確定（SCR-029・DLV_CONFIRM_COMPLETION）を単独 Issue 化。分割 ≤ 5 回 |
| specs/offline-continuity/（SCR-033・034） | #291 — E6 オフライン | LAB-1 の削減候補 1 位。業務日・冪等キュー |
| specs/settlement-and-correction/（SCR-035〜042・066） | #352 — E7 照合・締め・訂正 | 業務日（OPEN 1 件・締め解除）、締め後訂正（reverse/delta・50 万円以上 2 段階承認）、税関数（BR-INC-01 と共用） |
| specs/incentive-and-rule-version/（SCR-043〜047） | #166 — E8 奨励金・料率版 | **完納奨励金**（110/100・円未満切り捨て・次期差額・DS-INC-EDGE-01）と料率版（年 4 回・起票承認分離） |
| specs/reporting-and-print/（SCR-048〜058） | #315 — E9 帳票・印刷 | 奨励金帳票 RPT-07 は BR-INC-01。PDF は作らない（PREMISE C-22） |
| specs/accounting-integration/（SCR-059） | #4 — E10 会計連携 | 会計出力済 = .ok 受領。締め後訂正は追加バッチ |
| specs/notification/（SCR-060〜062） | #278 — E11 通知 |  |
| specs/audit-trail/（SCR-063・064） | #42 — E12 監査 | 監査 4 要素はトリガー（LAB-4 ADR-003） |
| specs/operations-monitoring/（SCR-065） | #305 — E13 運用監視 | 日次バッチの枠組みを本 epic に集約（PREMISE C-19） |
| specs/_common/、COMMON_DB、ADR-001・003・005〜007 | #54 — E14 共通基盤 | 業務日・rule_config の版解決。全 epic の前提 |
| architecture/data-migration.md、ADR-013 | #70 — E15 データ移行 | rule_config 初期版の発効日を変更（PREMISE C-11・C-12） |
| architecture/deployment.md・nfr.md・integrations.md、ADR-009・014 | #212 — E16 インフラ・非機能 | 国内リージョンのみ（国外複製なし） |
| PREMISE.md §2 A-71、§3 | —（全 epic） — — | 確認 Issue（各 epic の `確認事項`）に実装 Issue を依存させない |
