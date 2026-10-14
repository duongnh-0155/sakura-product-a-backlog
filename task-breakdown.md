# タスク分解（task-breakdown）

対象: LAB-4 提出版 `specs/`（`901af59`）＋ [PREMISE.md](PREMISE.md) の差分。
GitHub Project: <https://github.com/users/duongnh-0155/projects/1> — Epic 16 件・Issue 264 件・Sub-issue 125 件（計 405 件）。

## 1. 分解の原則

### 1.1 粒度 — どこまで分けて止めるか

| 階層 | 単位 | 止める条件 |
|---|---|---|
| Epic | LAB-4 の feature 1 つ（13）＋横断 3（共通基盤・データ移行・インフラ／非機能） | feature README が SPEC・TECH・API・DB の唯一の結合点なので、そのまま 1 Epic にする |
| Issue | 画面仕様 1 件 → 画面 Issue／API 設計をリソース単位で 3〜6 本 → API Issue／DB 設計 1 件 → マイグレーション Issue／技術設計 1 件 → 業務ロジック Issue／feature ごとの受入テスト／feature ごとの確認事項 1 件 | 1 人が 1〜5 日で終わり、完了の定義を第三者が確認できる大きさ |
| Sub-issue | Issue の中の独立して検証できる段（実装／テストベクトル、静的 UI／状態・バリデーション／結合） | 下記「Sub-issue にする条件」を満たすときだけ。Sub-issue の下は作らない |

**Sub-issue にする条件（決定 D-14）:** 技術設計（TECH）を実装する Issue、または「完納奨励金・料率版・許可≠承認・締め後訂正」の制約を持つ Issue。理由は、金額・資格に直結するためテストベクトルを実装と別担当（QA-AUTO）で追い、完了を別々に判定したいから。それ以外の Issue の段は本文の「作業分解（チェックリスト）」に残し、GitHub 上の件数を抑えた（agent が出した 637 件 → 405 件）。

**API をまとめる単位:** 1 API = 1 Issue にはしない（200 Issue になり追えない）。同じリソース（例: 訂正依頼の起票系 4 本）を 1 Issue にする。例外は完納確定 API（DLV_CONFIRM_COMPLETION）で、BR-INC-01 の境界として単独にした。

### 1.2 完了の定義（DoD）

各 Issue 本文の「完了の定義」に個別の条件を書いた。共通の最低条件は次のとおり。

- 対象 SPEC・TECH・API・DB の記載と実装を突き合わせ、差異があれば PREMISE.md に行を追加した
- 単体テスト（TECH はテストベクトル全件）と lint・型検査が CI で通る
- 画面 Issue は受入条件のシナリオを staging で確認し、権限（ロール別表示）を確認した
- DB Issue は `forbid_delete()`・監査トリガー・年度パーティションの有無を確認した
- レビュー 1 名の承認。制約付き Issue は QA-AUTO のテストベクトル結果を添付

### 1.3 Project 上での Epic → Issue → Sub-issue の使い方

- 親子は GitHub の sub-issue 機能で結び、Project の `Parent issue`・`Sub-issues progress` 列で進捗を見る。
- `Level` 欄（Epic／Issue／Sub-issue）で階層をフィルタする。Board ビューは Issue と Sub-issue だけを表示。
- `Point` は SWP（子を持つ Issue・Epic は子の合計）、`Hours` は見積時間、`Sprint` は 2 週間の Iteration、`担当` は仮の担当ロール（実在の個人ではない）。
- 制約はラベル `constraint:*` と `Constraint` 欄の両方に付け、「制約別」ビューで一覧できる。
- 依存は Issue 本文「メタ情報 → 依存」に #番号で書いた。確認 Issue（`確認事項（feature）`）には実装 Issue を依存させていない（D-17）。

## 2. 仕様 → Issue

LAB-4 の文書 ID（`specs/` の frontmatter `id`、API は `api_id`）から Issue への対応。1 行 = 1 Issue（括弧内は sub-issue の番号）。
Issue にしなかった仕様（107 行）は「タスク化しなかった部分と理由」に書いた。主な理由は、別 feature の Issue に含めた、範囲外（LAB-4 PREMISE）、運用側の作業で開発 Issue ではない、の 3 つ。

| Spec（LAB-4 文書 ID） | Epic | Issue（sub-issue） | タスク化しなかった部分と理由 |
|---|---|---|---|
| SPEC-ACCOUNTING_DB-001, SPEC-BIZDAY_DB-001, SPEC-SETTLEMENT_DB-001, SPEC-COMMON_DB-001, A… | #4 E10 会計連携（accounting-integration） | #5 `ACC-01` DB マイグレーション ACCOUNTING_DB（acc_export_batch・acc_ac… | — |
| SPEC-TECH-ACC_EXPORT_ACK, SPEC-ACCOUNTING_DB-001, SPEC-REPORT_DB-001, SPEC-BIZDAY_DB-001,… | #4 E10 会計連携（accounting-integration） | #6 `ACC-02` 業務ロジック ACC_EXPORT_ACK（DAILY 出力・SFTP 送信・ACK 回収・再出力…（#7, #8, #9, #10, #11, #12） | — |
| SPEC-TECH-ACC_EXPORT_ACK, SPEC-ACCOUNTING_DB-001, SPEC-SETTLEMENT_DB-001, ADR-004, ADR-01… | #4 E10 会計連携（accounting-integration） | #13 `ACC-03` 業務ロジック ACC_EXPORT_ACK §4.6（締め後訂正の SUPPLEMENT 追加バッ…（#14, #15） | — |
| SPEC-ACC-001, SPEC-RPT-005, ACC_LIST_EXPORT_BATCHES, ACC_GET_EXPORT_BATCH, ACC_GET_CONNEC… | #4 E10 会計連携（accounting-integration） | #16 `ACC-04` API 会計出力バッチ照会（ACC_LIST_EXPORT_BATCHES, ACC_GET_EX… | — |
| SPEC-ACC-001, ACC_RESEND_EXPORT_BATCH, ACC_CREATE_EXPORT_BATCH, ACC_CONFIRM_MANUAL_ACK, S… | #4 E10 会計連携（accounting-integration） | #17 `ACC-05` API 会計連携操作（ACC_RESEND_EXPORT_BATCH, ACC_CREATE_EX… | — |
| SPEC-ACC-001, ACC_LIST_EXPORT_BATCHES, ACC_GET_EXPORT_BATCH, ACC_GET_CONNECTION_STATUS, A… | #4 E10 会計連携（accounting-integration） | #18 `ACC-06` 画面 SCR-059 会計連携状況 | — |
| SPEC-ACC-001 | #4 E10 会計連携（accounting-integration） | #19 `ACC-08` 受入テスト accounting-integration（SCR-059 E2E 13 シナリオ・… | — |
| SPEC-TECH-ACC_EXPORT_ACK, PF-08, SPEC-ACC-001, ADR-014 | #4 E10 会計連携（accounting-integration） | #20 `ACC-09` 会計 IF 結合テスト（/test/ 検証・実結合 2 回・PF-08 全遷移・11:00 枠） | — |
| SPEC-ACCOUNTING_DB-001, SPEC-TECH-ACC_EXPORT_ACK, SPEC-RPT-005, SPEC-ACC-001, ADR-012 | #4 E10 会計連携（accounting-integration） | #21 `ACC-Q` 確認事項（accounting-integration）— 5 件 | — |
| SCR-052 RPT-06 会計照合用出力（送信内容の照会・原本表示） | #4 E10 会計連携（accounting-integration） | — | reporting-and-print の画面・API（#321（RPT-06） issue）。本 feature は `ACC_GET_EXPORT_FILE`・`ACC_LIST_EXPORT_BATCHES` を提供するのみ。 |
| `.ng` 原因の照合データ修正（締め解除・訂正依頼） | #4 E10 会計連携（accounting-integration） | — | settlement-and-correction（SCR-037〜040、PF-01／PF-06）。 |
| エクスポートエラー通知の送達・再送 | #4 E10 会計連携（accounting-integration） | — | notification（#280（NTF-02）／#281（NTF-03））。本 feature は `notify(ACC_EXPORT_ERROR)` を呼ぶだけ。 |
| 会計からの入金実績の取込 | #4 E10 会計連携（accounting-integration） | — | 対象外（IF-#5（ACC-01） は出力のみ、AS-089）。入金は incentive-and-rule-version の SCR-047 で手入力。 |
| SSH 鍵の発行・許可リスト登録 | #4 E10 会計連携（accounting-integration） | — | 発注者情報システム部門の作業。本 feature は受領手順（#222（INF-10） runbook）のみ。 |
| AUCTION_DB, TRADE_DB, PF-10, ADR-001, ADR-006, ADR-013 | #22 E4 せり（auction-result） | #23 `AUC-01` DB migration AUCTION_DB（auction_session / auction… | — |
| AUC_AUCTION_SESSION_CLOSE, AUC_CONFIRM_AUCTION_SESSION_API, SPEC-AUC-001, AUCTION_DB, TRA… | #22 E4 せり（auction-result） | #24 `AUC-02` 業務ロジック AUC_AUCTION_SESSION_CLOSE（せりセッション確定と取引生成・A…（#25, #26） | — |
| AUC_CREATE_AUCTION_SESSION_API, AUC_LIST_AUCTION_SESSIONS_API, AUC_GET_AUCTION_SESSION_AP… | #22 E4 せり（auction-result） | #27 `AUC-03` API せりセッション（AUC_CREATE_AUCTION_SESSION, AUC_LIST_… | — |
| AUC_CREATE_AUCTION_RESULT_API, AUC_UPDATE_AUCTION_RESULT_API, AUC_LIST_AUCTION_RESULT_HIS… | #22 E4 せり（auction-result） | #28 `AUC-04` API せり結果行（AUC_CREATE_AUCTION_RESULT, AUC_UPDATE_A…（#29, #30） | — |
| SPEC-AUC-001, AUC_GET_AUCTION_SESSION_API, AUC_LIST_AUCTION_LOT_CANDIDATES_API, AUC_LIST_… | #22 E4 せり（auction-result） | #31 `AUC-05` 画面 SCR-024 せり結果連続入力（#32, #33, #34） | — |
| SPEC-AUC-010, AUC_LIST_AUCTION_SESSIONS_API, AUC_CREATE_AUCTION_SESSION_API, STL_GET_OPEN… | #22 E4 せり（auction-result） | #35 `AUC-06` 画面 SCR-025 せりセッション一覧 | — |
| SPEC-AUC-011, AUC_GET_AUCTION_SESSION_API, AUC_LIST_AUCTION_RESULT_HISTORY_API, AUC_UPDAT… | #22 E4 せり（auction-result） | #36 `AUC-07` 画面 SCR-026 せり結果照会（#37, #38） | — |
| SPEC-AUC-001, SPEC-AUC-010, SPEC-AUC-011 | #22 E4 せり（auction-result） | #39 `AUC-08` 受入テスト auction-result（SCR-024〜026 E2E） | — |
| AUC_AUCTION_SESSION_CLOSE, AUCTION_DB, TRADE_DB, SPEC-AUC-001, SPEC-AUC-011, PF-04, PF-05 | #22 E4 せり（auction-result） | #40 `AUC-09` 受入テスト（特殊）せり確定→取引生成の結合（全体 ROLLBACK・maker≠checker・落… | — |
| SPEC-AUC-001, AUCTION_DB, AUC_AUCTION_SESSION_CLOSE, SPEC-AUC-011, SPEC-AUC-010, PF-10 | #22 E4 せり（auction-result） | #41 `AUC-Q` 確認事項（auction-result）— 3 件 | — |
| SCR-024 / 025 の STL_GET_OPEN_BUSINESS_DAY、業務日オープン SCR-066・締め SCR-036 | #22 E4 せり（auction-result） | — | settlement-and-correction の責務。 |
| SCR-026 ㉙ 訂正依頼 SCR-037 と 2 段階承認（50 万円）・SCR-040 締め解除申請 | #22 E4 せり（auction-result） | — | settlement-and-correction（PF-06、STL_CORRECTION_APPROVAL / STL_BUSINESS_DAY_UNLOCK）。本 feature は導線とモード表示のみ。 |
| 生成取引の一覧・詳細・引渡し・精算・奨励金 | #22 E4 せり（auction-result） | — | negotiated-trade / delivery / settlement / incentive の経路に乗る（AS-051）。#40（AUC-09） で結合のみ検証。 |
| `party.short_code` の登録・資格の管理（SCR-008）、`assert_party_eligible_as_buyer()` | #22 E4 せり（auction-result） | — | identity-and-participants。 |
| 手やり・符丁・手書き票の OCR／AI 認識、写真取込、CSV 一括取込 | #22 E4 せり（auction-result） | — | 範囲外（SCOPE-OUT-02、REQ-002 Q12）。提案もしない。 |
| オフライン入力キュー | #22 E4 せり（auction-result） | — | 対象外（fail closed、REQ-002 Q28）。E-OFF-002 の表示のみ各画面 issue に含む。 |
| RPT-14 せり件数・せり結果票の帳票 | #22 E4 せり（auction-result） | — | reporting-and-print。 |
| SPEC-TECH-AUD_AUDIT_WRITE, SPEC-COMMON_DB-001, ADR-003, ADR-007, ADR-013 | #42 E12 監査（audit-trail） | #43 `AUD-01` 業務ロジック AUD_AUDIT_WRITE（監査書込み・実行主体コンテキスト必須・不変性）（#44, #45） | — |
| SPEC-AUDIT_DB-001, SPEC-COMMON_DB-001, ADR-013 | #42 E12 監査（audit-trail） | #46 `AUD-02` DB マイグレーション AUDIT_DB（v_audit_search・audit_search_… | — |
| SPEC-AUD-001, SPEC-AUD-002, SPEC-AUDIT_DB-001, AUD_LIST_AUDIT_LOGS, AUD_GET_AUDIT_LOG, AU… | #42 E12 監査（audit-trail） | #47 `AUD-03` API 監査検索・詳細・変更履歴（AUD_LIST_AUDIT_LOGS, AUD_GET_AUD… | — |
| SPEC-AUD-001, AUD_CREATE_ARCHIVE_SEARCH, RPT_GET_REPORT_RUN, SPEC-REPORT_DB-001, ADR-013 | #42 E12 監査（audit-trail） | #48 `AUD-04` API cold 期間の非同期監査検索（AUD_CREATE_ARCHIVE_SEARCH）と検索… | — |
| SPEC-AUD-001, AUD_LIST_AUDIT_LOGS, AUD_CREATE_ARCHIVE_SEARCH, RPT_GET_REPORT_RUN, IAM_LIS… | #42 E12 監査（audit-trail） | #49 `AUD-05` 画面 SCR-063 監査検索 | — |
| SPEC-AUD-002, AUD_GET_AUDIT_LOG, AUD_LIST_AUDIT_LOGS | #42 E12 監査（audit-trail） | #50 `AUD-06` 画面 SCR-064 監査詳細 | — |
| SPEC-AUD-001, SPEC-AUD-002 | #42 E12 監査（audit-trail） | #51 `AUD-07` 受入テスト audit-trail（SCR-063／064 E2E・性能・権限） | — |
| SPEC-TECH-AUD_AUDIT_WRITE, SPEC-COMMON_DB-001, ADR-003 | #42 E12 監査（audit-trail） | #52 `AUD-08` 監査トリガー網羅・不変性テスト（全業務表・OBJ-03 測定クエリ） | — |
| SPEC-AUD-001, SPEC-AUDIT_DB-001, SPEC-AUD-002 | #42 E12 監査（audit-trail） | #53 `AUD-Q` 確認事項（audit-trail）— 3 件 | — |
| COMMON_DB §4.1 audit_log（表・PK・索引 1〜5・トリガー本体の DDL） | #42 E12 監査（audit-trail） | — | 横断 DB のため cross-cutting epic（#55（XC-01）, #56（XC-02））で起票。本 feature は関数の拡張とビューのみ。 |
| SCR-063 の候補 API（IAM_LIST_PARTY_CANDIDATES・IAM_LIST_USER_CANDIDATES） | #42 E12 監査（audit-trail） | — | identity-and-participants の API。本 feature は呼び出すだけ。 |
| SCR-063 A7・SCR-064 A6 のアクセスログ基盤（7 年保持、AS-019） | #42 E12 監査（audit-trail） | — | ログ基盤は infra-nfr epic。本 feature は出力呼出しのみ（#47（AUD-03） に含む）。 |
| AUD_AUDIT_WRITE §4.3 No.3 7 年満了後の物理削除 | #42 E12 監査（audit-trail） | — | アプリ外の runbook（発注者 IT の専用 DB ロール、P5 D60）。システム開発の範囲外。 |
| SCR-063 対象外: login_attempt・APPI 開示請求 | #42 E12 監査（audit-trail） | — | SPEC で対象外と明記。login_attempt は operations-monitoring の領域。 |
| COMMON_DB, ADR-003, ADR-005, ADR-006, ADR-013, data-model-overview | #54 E14 共通基盤（cross-cutting） | #55 `XC-01` DB 共通テーブル COMMON_DB（audit_log・rule_config・market_… | — |
| COMMON_DB, ADR-007, ADR-013, data-model-overview, deployment | #54 E14 共通基盤（cross-cutting） | #56 `XC-02` DB 共通トリガー基盤 forbid_delete()・年度パーティション枠組み・DB ロール 5… | — |
| api-conventions, error-codes, ADR-001 | #54 E14 共通基盤（cross-cutting） | #57 `XC-03` API エラー封筒・E-code 変換層（成功/失敗 envelope・trace_id・DB H… | — |
| api-conventions, ADR-007, ADR-010, nfr, integrations | #54 E14 共通基盤（cross-cutting） | #58 `XC-04` 認証ミドルウェア・サーバーセッション基盤（__Host-sid Cookie・ElastiCach… | — |
| api-conventions, api-list, ADR-007 | #54 E14 共通基盤（cross-cutting） | #59 `XC-05` RBAC 判定層（role_permission scope=API/ACTION・has_act… | — |
| ADR-003, ADR-006, api-conventions, COMMON_DB | #54 E14 共通基盤（cross-cutting） | #60 `XC-06` 監査コンテキスト・トランザクション基盤 withAudit()（set_audit_context… | — |
| log-convention, api-conventions, nfr | #54 E14 共通基盤（cross-cutting） | #61 `XC-07` 構造化ログ・trace_id 伝播・ログ規約（log-convention・禁止項目・CloudW… | — |
| ADR-005, ADR-006, ADR-013, api-conventions, COMMON_DB | #54 E14 共通基盤（cross-cutting） | #62 `XC-08` 業務日・会計年度・hot/cold 判定の共通ユーティリティ（rule_value 呼出し・営業日… | — |
| api-conventions, COMMON_DB, ADR-008, ADR-011, ADR-013 | #54 E14 共通基盤（cross-cutting） | #63 `XC-09` 共通 API 基盤: ページング・ソート・絞込・楽観ロック・Idempotency-Key・データ… | — |
| nfr, error-codes, glossary, screen-id-map | #54 E14 共通基盤（cross-cutting） | #64 `XC-10` デザインシステム・UI キット（WCAG 2.1 A・タップ 44px・コントラスト 4.5:1/… | — |
| api-conventions, error-codes, screen-id-map, ADR-011 | #54 E14 共通基盤（cross-cutting） | #65 `XC-11` FE アプリ基盤（App shell・8 ロール別ナビゲーション・API クライアント封筒処理・セ… | — |
| deployment, nfr, ADR-007 | #54 E14 共通基盤（cross-cutting） | #66 `XC-12` CI ゲート骨格（gate: tsc/lint/trace/check:sql/build・tes… | — |
| deployment, api-conventions, ADR-006, ADR-010 | #54 E14 共通基盤（cross-cutting） | #67 `XC-13` E2E テスト基盤（Playwright・ロール別ログインフィクスチャ・業務日 OPEN/CLOS… | — |
| ADR-001, ADR-003, ADR-006, ADR-007, api-conventions, error-codes, nfr | #54 E14 共通基盤（cross-cutting） | #68 `XC-17` 受入テスト cross-cutting（制約・監査・権限の侵入シナリオと API 共通規約の契約テ… | — |
| log-convention, nfr, integrations, api-conventions, COMMON_DB, ADR-005, ADR-013 | #54 E14 共通基盤（cross-cutting） | #69 `XC-Q` 確認事項（cross-cutting）— 3 件 | — |
| api-list.md §2 の公開 API 4 本（IAM_CREATE_OIDC_*・IAM_CREATE_EXTERNAL_SESSION・OPS_GET_MAINTENA… | #54 E14 共通基盤（cross-cutting） | — | 契約を所有する feature（identity-and-participants・operations-monitoring）の BE issue で実装。#58（XC-04） は allowlist と検証ミドルウェアのみ提供。 |
| COMMON_DB §4.5 税関数の呼び出し側（DELIVERY_DB・SETTLEMENT_DB・INCENTIVE_PART2_DB） | #54 E14 共通基盤（cross-cutting） | — | 関数定義は #55（XC-01-e）、呼び出しと BR-#167（INC-01） の計算は各 feature（delivery・settlement・incentive）の issue。 |
| ADR-013 の年度パーティション 11 表のうち audit_log 以外の 10 表の DDL | #54 E14 共通基盤（cross-cutting） | — | 各 feature の DB issue が #56（XC-02-c） のテンプレートと `assert_partition_fiscal_year()` を使って定義する。 |
| glossary.md §1 用語一覧・§3 許可と承認の比較 | #54 E14 共通基盤（cross-cutting） | — | 実装物は §2 の enum↔ラベル対照（#64（XC-10-b））のみ。用語定義そのものはタスク化対象外。 |
| screen-id-map.md | #54 E14 共通基盤（cross-cutting） | — | 優先度と feature 割当の参照のみ。#65（XC-11-a） のナビ生成の入力として使う。 |
| COMMON_DB §5 Q3（correction_threshold_basis、AS-039） | #54 E14 共通基盤（cross-cutting） | — | settlement-and-correction feature の clarify で扱う（post-close-correction 制約）。 |
| ARCH-DATA_MIGRATION, drift-vs-lab1 | #70 E15 データ移行（data-migration） | #71 `MIG-01` 移行プロファイリング（1〜2 か月目）: インベントリ正本化・Q26 汚れ R-1〜R-8 の実測… | — |
| ARCH-DATA_MIGRATION, ADR-007, COMMON_DB, IAM_DB | #70 E15 データ移行（data-migration） | #72 `MIG-02` 移行専用スキーマ migration.*（reject・party_code_map・item_c… | — |
| ARCH-DATA_MIGRATION, ADR-002, PARTY_DB, LOT_DB, TRADE_DB, DELIVERY_DB, SETTLEMENT_DB | #70 E15 データ移行（data-migration） | #73 `MIG-03` 列単位マッピング定義 mapping/v1,v2,v3/*.csv（テンプレート 3 世代・App… | — |
| ARCH-DATA_MIGRATION, ADR-003, ADR-006, ADR-013, COMMON_DB, deployment | #70 E15 データ移行（data-migration） | #74 `MIG-04` 移行ツール共通基盤（Fargate 一回限りタスク・読込・規則エンジン R-1〜R-8・rejec… | — |
| ARCH-DATA_MIGRATION, ADR-002, PARTY_DB, LOT_DB, COMMON_DB | #70 E15 データ移行（data-migration） | #75 `MIG-05` Wave 1 ロード: party・party_status_history・item_maste…（#76, #77, #78） | — |
| ARCH-DATA_MIGRATION, ADR-006, ADR-008, BIZDAY_DB, LOT_DB, TRADE_DB, DELIVERY_DB, SETTLEME… | #70 E15 データ移行（data-migration） | #79 `MIG-06` Wave 2 ロード: FY2026 business_day（全日 CLOSED）・lot・lo… | — |
| ARCH-DATA_MIGRATION, ADR-013, SETTLEMENT_DB, TRADE_DB | #70 E15 データ移行（data-migration） | #80 `MIG-07` Wave 3 ロード: FY2022〜25 全明細（3 世代）・FY2021 相対明細＋せり日次合… | — |
| ARCH-DATA_MIGRATION, ARCH-NFR | #70 E15 データ移行（data-migration） | #81 `MIG-08` 照合・受入（MIG-03）: 件数・金額・整合性照合 SQL の自動化、照合表（ACC-04 証跡… | — |
| ARCH-DATA_MIGRATION, ARCH-DEPLOYMENT, ADR-004, ADR-007 | #70 E15 データ移行（data-migration） | #82 `MIG-09` 切替・ロールバック手順（MIG-04 / 10-04）: freeze 前日 10:00・スナップ… | — |
| ARCH-DATA_MIGRATION, COMMON_DB, ASSUMPTIONS | #70 E15 データ移行（data-migration） | #83 `MIG-Q` 確認事項（data-migration）— 2 件 | — |
| data-migration.md §9 SCR-035／SCR-055 の「集計レベル」バッジ、SCR-063 の `reason LIKE 'migration:%'` 抽出 | #70 E15 データ移行（data-migration） | — | 画面側の実装は settlement／reporting／audit-trail feature の SPEC issue。本 epic はデータ側（`settlement_monthly_legacy`・`audit_log` の actor_role／reason）を保証する。 |
| data-migration.md §5 R-7 の `assert_trade_confirm_eligibility` 緩和分岐 | #70 E15 データ移行（data-migration） | — | トリガー本体は TRADE_DB（negotiated-trade feature）の DB issue。#72（MIG-02） で要求事項（`current_user = 'producta_migration'` 判定）を連絡する。 |
| data-migration.md §3 体制表・go/no-go 判定者 | #70 E15 データ移行（data-migration） | — | 役割割当は PM の体制文書で扱い、タスクにはしない。#82（MIG-09） の手順書に承認欄として反映。 |
| ADR-014 FY_PARTITION_CREATE（次年度パーティションの年次作成） | #70 E15 データ移行（data-migration） | — | 年次バッチは reporting feature（batch_job_run）と #216（INF-04） のスケジュール。移行用の過去年度一括作成だけ #56（XC-02-c）。 |
| DELIVERY_DB, SPEC-TECH-DLV_DELIVERY_RECORD, SPEC-TECH-DLV_DELIVERY_EXCEPTION_RECALC, ADR-… | #84 E5 引渡し（delivery） | #85 `DLV-01` DB マイグレーション DELIVERY_DB（delivery・delivery_excepti… | — |
| SPEC-TECH-DLV_DELIVERY_RECORD, DLV_CREATE_DELIVERY_API, DLV_UPDATE_DELIVERY_API, DELIVERY… | #84 E5 引渡し（delivery） | #86 `DLV-02` 業務ロジック DLV_DELIVERY_RECORD（分割 5 回・累計上限・未完了 1 回・都度…（#87, #88, #89） | — |
| SPEC-TECH-DLV_DELIVERY_COMPLETION_CONFIRM, DLV_CONFIRM_COMPLETION_API, DELIVERY_DB, TRADE… | #84 E5 引渡し（delivery） | #90 `DLV-03` 業務ロジック DLV_DELIVERY_COMPLETION_CONFIRM（完納確定 confi…（#91, #92） | — |
| SPEC-TECH-DLV_DELIVERY_EXCEPTION_RECALC, DLV_CREATE_DELIVERY_EXCEPTION_API, DLV_CONFIRM_D… | #84 E5 引渡し（delivery） | #93 `DLV-04` 業務ロジック DLV_DELIVERY_EXCEPTION_RECALC（例外起票・締め前自動再計…（#94, #95, #96） | — |
| SPEC-DLV-001, DLV_LIST_DELIVERIES_API, DLV_UPDATE_DELIVERY_API, STL_LIST_BUSINESS_DAYS_AP… | #84 E5 引渡し（delivery） | #97 `DLV-05` 画面 SCR-027 引渡しボード | — |
| SPEC-DLV-002, DLV_LIST_DELIVERABLE_TRADES_API, DLV_GET_DELIVERY_API, DLV_CREATE_DELIVERY_… | #84 E5 引渡し（delivery） | #98 `DLV-06` 画面 SCR-028 引渡し記録入力 | — |
| SPEC-DLV-003, DLV_GET_DELIVERY_API, DLV_CONFIRM_COMPLETION_API, AUD_LIST_ENTITY_AUDIT_LOG… | #84 E5 引渡し（delivery） | #99 `DLV-07` 画面 SCR-029 引渡し詳細（完納確定）（#100, #101, #102） | — |
| SPEC-DLV-010, DLV_GET_DELIVERY_EXCEPTION_CONTEXT_API, DLV_CREATE_DELIVERY_EXCEPTION_API, … | #84 E5 引渡し（delivery） | #103 `DLV-08` 画面 SCR-030 引渡し例外入力 | — |
| SPEC-DLV-011, DLV_LIST_STALE_DELIVERIES_API, STL_LIST_BUSINESS_DAYS_API, IAM_LIST_PARTY_C… | #84 E5 引渡し（delivery） | #104 `DLV-09` 画面 SCR-031 滞留引渡し一覧 | — |
| SPEC-DLV-012, DLV_GET_SETTLEMENT_TRACE_API, DLV_CREATE_ARCHIVE_SEARCH_API, ACC_GET_EXPORT… | #84 E5 引渡し（delivery） | #105 `DLV-10` 画面 SCR-032 引渡し⇔精算追跡 | — |
| SPEC-DLV-004, DLV_LIST_QUICK_LOOKUP_API, RPT_CREATE_PRINT_JOB_API, RPT_UPDATE_PRINT_JOB_A… | #84 E5 引渡し（delivery） | #106 `DLV-11` 画面 SCR-067 窓口クイック照会（1 操作印刷） | — |
| DLV_LIST_DELIVERIES_API, DLV_LIST_DELIVERABLE_TRADES_API, DLV_GET_DELIVERY_API, DLV_CREAT… | #84 E5 引渡し（delivery） | #107 `DLV-12` API 引渡し記録・ボード（DLV_LIST_DELIVERIES, DLV_LIST_DELIV… | — |
| DLV_CONFIRM_COMPLETION_API, SPEC-TECH-DLV_DELIVERY_COMPLETION_CONFIRM, PF-07 | #84 E5 引渡し（delivery） | #108 `DLV-13` API 完納確定（DLV_CONFIRM_COMPLETION） | — |
| DLV_GET_DELIVERY_EXCEPTION_CONTEXT_API, DLV_CREATE_DELIVERY_EXCEPTION_API, DLV_LIST_DELIV… | #84 E5 引渡し（delivery） | #109 `DLV-14` API 引渡し例外（DLV_GET_DELIVERY_EXCEPTION_CONTEXT, DLV… | — |
| DLV_CREATE_DELIVERY_EXCEPTION_ATTACHMENT_API, DLV_GET_DELIVERY_EXCEPTION_ATTACHMENT_API, … | #84 E5 引渡し（delivery） | #110 `DLV-15` API 引渡し例外の証跡添付（DLV_CREATE_DELIVERY_EXCEPTION_ATTA… | — |
| DLV_LIST_STALE_DELIVERIES_API, DLV_LIST_QUICK_LOOKUP_API, DLV_GET_SETTLEMENT_TRACE_API, D… | #84 E5 引渡し（delivery） | #111 `DLV-16` API 照会系（DLV_LIST_STALE_DELIVERIES, DLV_LIST_QUICK… | — |
| SPEC-DLV-001, SPEC-DLV-002, SPEC-DLV-003, SPEC-DLV-010, SPEC-DLV-011, SPEC-DLV-012, SPEC-… | #84 E5 引渡し（delivery） | #112 `DLV-17` 受入テスト delivery（SCR-027〜032・067 の受入条件 E2E） | — |
| SPEC-TECH-DLV_DELIVERY_COMPLETION_CONFIRM, SPEC-TECH-DLV_DELIVERY_EXCEPTION_RECALC, SPEC-… | #84 E5 引渡し（delivery） | #113 `DLV-18` 受入テスト BR-INC-01 完納状態の横断（完納→奨励金対象・6 回目算入・完納後の例外/訂正） | — |
| SPEC-TECH-DLV_DELIVERY_RECORD, OFF_CREATE_SYNC_RECEIPT_API, OFFLINE_DB, PF-09, ADR-011 | #84 E5 引渡し（delivery） | #114 `DLV-19` 連携 引渡しのオフライン業務キー・同期契約（{trade.code}#{seq} / #{stat… | — |
| SPEC-TECH-DLV_DELIVERY_RECORD, DELIVERY_DB, SETTLEMENT_DB, ADR-008 | #84 E5 引渡し（delivery） | #115 `DLV-20` 受入テスト 分割引渡し × 精算の金額整合（按分・端数寄せ・再計算後） | — |
| SPEC-DLV-002, DELIVERY_DB, SPEC-DLV-003, SPEC-TECH-DLV_DELIVERY_COMPLETION_CONFIRM, PF-06… | #84 E5 引渡し（delivery） | #116 `DLV-Q` 確認事項（delivery）— 6 件 | — |
| SCR-027 / 028 / 029 / 030 の受渡伝票印刷リンク（SCR-058 への遷移） | #84 E5 引渡し（delivery） | — | 版面・プリンタ選択は reporting-and-print（RPT）の範囲。delivery 側はリンク表示のみで #100（DLV-07-a） / #98（DLV-06-a） に含める。 |
| SCR-028 / SCR-030 の締め解除モードの入口（SCR-040）と STL_UNLOCK_MODE_WRITE の判定 | #84 E5 引渡し（delivery） | — | settlement-and-correction（#354（STL-02））が所有。delivery 側は GUC を渡し DB 判定を受けるだけ（#86（DLV-02） / #93（DLV-04） に含む）。 |
| SCR-030 ⑲ 訂正依頼へ進む → SCR-037 の起票内容・2 段階承認 | #84 E5 引渡し（delivery） | — | PF-06 は settlement-and-correction の範囲。delivery は例外 ID の引継ぎのみ（#103（DLV-08-c））。 |
| SCR-032 の会計 batch 再送・手動 ACK（SCR-059） | #84 E5 引渡し（delivery） | — | accounting-integration の範囲。SCR-032 は状態表示のみ。 |
| COMMON_DB §4.5 `settlement_tax_from_gross()` / `br_inc01_incentive_with_tax()` と STL_SETT… | #84 E5 引渡し（delivery） | — | cross-cutting（COMMON_DB）と settlement-and-correction が所有。delivery は呼び出すだけ（#88（DLV-02-b））。 |
| OFF_CREATE_SYNC_RECEIPT の受領・冪等・競合作成（PF-09 §4 遷移 2〜5） | #84 E5 引渡し（delivery） | — | offline-continuity（#293（OFF-02））が所有。delivery は業務キーと payload 契約（#114（DLV-19））だけを担う。 |
| 各 SPEC の 画面項目定義（項目ごとの型・桁・バリデーション詳細） | #84 E5 引渡し（delivery） | — | brief の指示により件数のみ計上（SCR-027: 17、028: 21、029: 23、030: 27、031: 21、032: 23、067: 13）。実装時に各 FE sub-issue (a) が参照。 |
| IAM_DB, COMMON_DB, ADR-007, ADR-010 | #117 E1 認証・参加者（identity-and-participant… | #118 `IAM-01` DB migration IAM_DB（app_user・external_account・log… | — |
| PARTY_DB, COMMON_DB, PF-02, ADR-002 | #117 E1 認証・参加者（identity-and-participant… | #119 `IAM-02` DB migration PARTY_DB（party・party_status_history・…（#120, #121） | — |
| SPEC-IAM-001, IAM_CREATE_OIDC_AUTHORIZATION_API, IAM_CREATE_OIDC_SESSION_API, IAM_GET_SES… | #117 E1 認証・参加者（identity-and-participant… | #122 `IAM-03` API 社内認証 Entra OIDC・セッション（IAM_CREATE_OIDC_AUTHORI… | — |
| SPEC-IAM-010, SPEC-IAM-020, IAM_CREATE_EXTERNAL_SESSION_API, IAM_CREATE_OTP_API, IAM_CONF… | #117 E1 認証・参加者（identity-and-participant… | #123 `IAM-04` API 外部参加者認証（IAM_CREATE_EXTERNAL_SESSION, IAM_CREA… | — |
| SPEC-IAM-021, SPEC-IAM-011, SPEC-AUD-001, IAM_LIST_ACCOUNTS_API, IAM_GET_ACCOUNT_API, IAM… | #117 E1 認証・参加者（identity-and-participant… | #124 `IAM-05` API アカウント照会（IAM_LIST_ACCOUNTS, IAM_GET_ACCOUNT, I… | — |
| SPEC-IAM-011, SPEC-IAM-022, IAM_CREATE_ACCOUNT_API, IAM_UPDATE_ACCOUNT_ROLE_API, IAM_UPDA… | #117 E1 認証・参加者（identity-and-participant… | #125 `IAM-06` API アカウント書込み（IAM_CREATE_ACCOUNT, IAM_UPDATE_ACCOU… | — |
| SPEC-IAM-022, SPEC-IAM-011, IAM_LIST_ROLES_API, IAM_LIST_ROLE_PERMISSIONS_API, IAM_UPDATE… | #117 E1 認証・参加者（identity-and-participant… | #126 `IAM-07` API ロール・権限（IAM_LIST_ROLES, IAM_LIST_ROLE_PERMISSI… | — |
| SPEC-IAM-002, SPEC-IAM-003, IAM_LIST_PARTIES_API, IAM_GET_PARTY_API, IAM_CREATE_PARTY_API… | #117 E1 認証・参加者（identity-and-participant… | #127 `IAM-08` API 参加者（IAM_LIST_PARTIES, IAM_GET_PARTY, IAM_CREA…（#128, #129） | — |
| SPEC-IAM-002, SPEC-IAM-003, SPEC-IAM-024, IAM_CREATE_QUALIFICATION_REQUEST_API, IAM_GET_Q… | #117 E1 認証・参加者（identity-and-participant… | #130 `IAM-09` API 参加資格申請（IAM_CREATE_QUALIFICATION_REQUEST, IAM_…（#131, #132） | — |
| SPEC-IAM-003, SPEC-IAM-024, IAM_CREATE_QUALIFICATION_ATTACHMENT_API, IAM_GET_QUALIFICATIO… | #117 E1 認証・参加者（identity-and-participant… | #133 `IAM-10` API 資格証跡（IAM_CREATE_QUALIFICATION_ATTACHMENT, IAM… | — |
| SPEC-IAM-023, SPEC-IAM-025, IAM_LIST_APPROVAL_QUEUE_API, IAM_LIST_EXPIRING_QUALIFICATIONS… | #117 E1 認証・参加者（identity-and-participant… | #134 `IAM-11` API 承認待ちキュー・失効警告（IAM_LIST_APPROVAL_QUEUE, IAM_LIS… | — |
| IAM_PARTY_ELIGIBILITY_TECH, PARTY_DB, TRADE_DB, ADR-001, ADR-002 | #117 E1 認証・参加者（identity-and-participant… | #135 `IAM-12` 業務ロジック IAM_PARTY_ELIGIBILITY（BR-PERM-01 取引確定時の資格判…（#136, #137） | — |
| IAM_PARTY_STATUS_TRANSITION_TECH, PARTY_DB, PF-02, ADR-002, ADR-003, ADR-014 | #117 E1 認証・参加者（identity-and-participant… | #138 `IAM-13` 業務ロジック IAM_PARTY_STATUS_TRANSITION（参加資格の一時停止・申請・承…（#139, #140, #141, #142） | — |
| SPEC-IAM-001, IAM_CREATE_OIDC_AUTHORIZATION_API, IAM_CREATE_OIDC_SESSION_API, IAM_GET_SES… | #117 E1 認証・参加者（identity-and-participant… | #143 `IAM-14` 画面 SCR-001 社内ログイン | — |
| SPEC-IAM-010, IAM_CREATE_EXTERNAL_SESSION_API, IAM_REVOKE_SESSION_API | #117 E1 認証・参加者（identity-and-participant… | #144 `IAM-15` 画面 SCR-002 外部参加者ログイン | — |
| SPEC-IAM-020, IAM_CREATE_OTP_API, IAM_CONFIRM_OTP_API | #117 E1 認証・参加者（identity-and-participant… | #145 `IAM-16` 画面 SCR-003 メールOTP検証 | — |
| SPEC-IAM-021, IAM_LIST_ACCOUNTS_API | #117 E1 認証・参加者（identity-and-participant… | #146 `IAM-17` 画面 SCR-004 アカウント一覧 | — |
| SPEC-IAM-011, IAM_GET_ACCOUNT_API, IAM_CREATE_ACCOUNT_API, IAM_UPDATE_ACCOUNT_ROLE_API, I… | #117 E1 認証・参加者（identity-and-participant… | #147 `IAM-18` 画面 SCR-005 アカウント詳細・権限編集 | — |
| SPEC-IAM-022, IAM_LIST_ROLES_API, IAM_LIST_ROLE_PERMISSIONS_API, IAM_UPDATE_ROLE_PERMISSI… | #117 E1 認証・参加者（identity-and-participant… | #148 `IAM-19` 画面 SCR-006 ロール・権限マスタ | — |
| SPEC-IAM-002, IAM_LIST_PARTIES_API, IAM_CREATE_QUALIFICATION_REQUEST_API | #117 E1 認証・参加者（identity-and-participant… | #149 `IAM-20` 画面 SCR-007 参加者一覧（#150, #151, #152） | — |
| SPEC-IAM-003, IAM_GET_PARTY_API, IAM_CREATE_PARTY_API, IAM_UPDATE_PARTY_API, IAM_CREATE_Q… | #117 E1 認証・参加者（identity-and-participant… | #153 `IAM-21` 画面 SCR-008 参加者詳細・編集（#154, #155, #156） | — |
| SPEC-IAM-023, IAM_LIST_APPROVAL_QUEUE_API | #117 E1 認証・参加者（identity-and-participant… | #157 `IAM-22` 画面 SCR-009 承認待ち一覧 | — |
| SPEC-IAM-024, IAM_GET_QUALIFICATION_REQUEST_API, IAM_GET_QUALIFICATION_ATTACHMENT_API, IA… | #117 E1 認証・参加者（identity-and-participant… | #158 `IAM-23` 画面 SCR-010 承認依頼詳細（#159, #160） | — |
| SPEC-IAM-025, IAM_LIST_EXPIRING_QUALIFICATIONS_API | #117 E1 認証・参加者（identity-and-participant… | #161 `IAM-24` 画面 SCR-011 失効警告一覧 | — |
| SPEC-IAM-001, SPEC-IAM-010, SPEC-IAM-020, SPEC-IAM-021, SPEC-IAM-011, SPEC-IAM-022, SPEC-… | #117 E1 認証・参加者（identity-and-participant… | #162 `IAM-25` 受入テスト identity-and-participants（SCR-001〜011 の受入条件… | — |
| ADR-002, PF-02, IAM_PARTY_ELIGIBILITY_TECH, IAM_PARTY_STATUS_TRANSITION_TECH, SPEC-IAM-00… | #117 E1 認証・参加者（identity-and-participant… | #163 `IAM-26` 検証 許可≠承認 分離（ADR-002・BR-PERM-01）横断テスト | — |
| ADR-010, SPEC-IAM-001, SPEC-IAM-010, SPEC-IAM-020, IAM_CREATE_OIDC_SESSION_API, IAM_CREAT… | #117 E1 認証・参加者（identity-and-participant… | #164 `IAM-27` 検証 認証セキュリティ（二経路 ADR-010：ロック・OTP 総当たり・列挙・リダイレクト・CS… | — |
| SPEC-IAM-001, SPEC-IAM-010, SPEC-IAM-020, SPEC-IAM-011, ADR-010, IAM_CREATE_ACCOUNT_API, … | #117 E1 認証・参加者（identity-and-participant… | #165 `IAM-Q` 確認事項（identity-and-participants）— 6 件 | — |
| SPEC-IAM-003 E9／E10（E-TRD-003／004 参照用）・取引確定時の資格判定の API 側テスト | #117 E1 認証・参加者（identity-and-participant… | — | 判定は negotiated-trade（SCR-019）／auction-result（SCR-024）の確定 API で発火する。本 feature は関数・トリガー（#135（IAM-12））のみ所有し、画面側の表示・テストは TRD-／AUC- の issue |
| IAM_LIST_PARTY_CANDIDATES・IAM_LIST_USER_CANDIDATES の呼出画面（SCR-020／031／041／063） | #117 E1 認証・参加者（identity-and-participant… | — | API は #128（IAM-08-a）／#124（IAM-05） で実装するが、画面側の共通コンポーネント利用は各 feature（TRD-／DLV-／STL-／AUD-）の FE issue |
| QUALIFICATION_EXPIRING 通知の配信・再試行・受信設定（SCR-060／061） | #117 E1 認証・参加者（identity-and-participant… | — | #141（IAM-13-c） は notification 行の発行まで。配信・既読・設定は notification feature（NTF-） |
| OTP メールの送信基盤・bounce 記録（notification_delivery_log、SCR-062） | #117 E1 認証・参加者（identity-and-participant… | — | 送信 I/F と delivery_log は NTF- が所有。#123（IAM-04-b） は呼出と delivery_log_id の連結のみ |
| ElastiCache・ALB mTLS・WAF 場内 IP・S3 署名 URL・Entra アプリ登録 | #117 E1 認証・参加者（identity-and-participant… | — | 基盤は infra-nfr 側（#56（XC-02））。#122（IAM-03）／04／10 はそれらを前提に利用 |
| 共通 attachment 表・audit_log・set_audit_context・forbid_delete・rule_config（COMMON_DB） | #117 E1 認証・参加者（identity-and-participant… | — | cross-cutting（#55（XC-01））の migration。#118（IAM-01）／02 は FK とトリガー利用のみ |
| ROLE-MIGRATION・producta_migration ロール・移行データの資格警告（AS-031／402） | #117 E1 認証・参加者（identity-and-participant… | — | data-migration epic の範囲。#118（IAM-01-a） は enum 値追加、#136（IAM-12-a） は current_user 判定の分岐のみ |
| SCR-033 のログアウト抑止（未同期キュー）・オフライン時のセッション失効（AS-080／289） | #117 E1 認証・参加者（identity-and-participant… | — | offline-continuity（OFF-）。IAM_REVOKE_SESSION はキューを検査しない（AS-316） |
| SCR-063／064 の監査検索（権限変更・異常ログイン）、SCR-065 のセキュリティアラート | #117 E1 認証・参加者（identity-and-participant… | — | audit-trail・operations-monitoring の範囲。本 feature は login_attempt の記録と alert_event への発行点のみ（#123（IAM-04-a）） |
| SCR-005 Q1／Q3／Q5、SCR-003 Q2、SCR-006 Q1、SCR-007 Q1、SCR-008 Q1／Q2、SCR-010 Q1、PARTY_DB T1、IA… | #117 E1 認証・参加者（identity-and-participant… | — | 統合レビューで closed／前提採用済み。issue 化不要 |
| SCR-039／040（訂正・締め解除の承認画面）への遷移先実装 | #117 E1 認証・参加者（identity-and-participant… | — | settlement-and-correction（STL-）。#157（IAM-22） はリンクのみ |
| RPT-03 参加者有効性レポート（party_status_history の集計） | #117 E1 認証・参加者（identity-and-participant… | — | reporting-and-print（RPT-）。本 feature は履歴表の提供のみ |
| INCENTIVE_DB, ADR-015, ADR-005, COMMON_DB | #166 E8 奨励金・規則version（incentive-and-rul… | #167 `INC-01` DB マイグレーション INCENTIVE_DB（rate_version・rate_line・i…（#168, #169） | — |
| INCENTIVE_PART2_DB, INCENTIVE_DB, ADR-013, ADR-004, COMMON_DB | #166 E8 奨励金・規則version（incentive-and-rul… | #170 `INC-02` DB マイグレーション INCENTIVE_PART2_DB（incentive_result・i…（#171, #172） | — |
| SPEC-TECH-INC_INCENTIVE_CALC, INC_UPDATE_INCENTIVE_PAYMENT_API, INC_RECALCULATE_INCENTIVE… | #166 E8 奨励金・規則version（incentive-and-rul… | #173 `INC-03` 業務ロジック INC_INCENTIVE_CALC（候補行・入金記録・判定日バッチ・再計算・期の確…（#174, #175, #176, #177） | — |
| SPEC-TECH-INC_RATE_VERSION, INCENTIVE_DB, INCENTIVE_PART2_DB, ADR-015, PF-07, IAM_DB | #166 E8 奨励金・規則version（incentive-and-rul… | #178 `INC-04` 業務ロジック INC_RATE_VERSION（起票・承認依頼・承認・差戻し・取下げ・発効・遡及例…（#179, #180, #181, #182） | — |
| SPEC-INC-001, INC_LIST_RATE_VERSIONS_API, STL_GET_OPEN_BUSINESS_DAY_API | #166 E8 奨励金・規則version（incentive-and-rul… | #183 `INC-05` 画面 SCR-043 料率version一覧（#184, #185） | — |
| SPEC-INC-002, INC_GET_RATE_VERSION_API, INC_CREATE_RATE_VERSION_API, INC_UPDATE_RATE_VERS… | #166 E8 奨励金・規則version（incentive-and-rul… | #186 `INC-06` 画面 SCR-044 料率version編集（#187, #188, #189） | — |
| SPEC-INC-003, INC_GET_RATE_VERSION_API, INC_APPROVE_RATE_VERSION_API, INC_REJECT_RATE_VER… | #166 E8 奨励金・規則version（incentive-and-rul… | #190 `INC-07` 画面 SCR-045 料率version承認・ロールバック（#191, #192, #193） | — |
| SPEC-INC-010, INC_GET_RATE_VERSION_API, INC_PREVIEW_RETRO_IMPACT_API, INC_CREATE_RETRO_AP… | #166 E8 奨励金・規則version（incentive-and-rul… | #194 `INC-08` 画面 SCR-046 遡及適用影響プレビュー（#195, #196） | — |
| SPEC-INC-011, INC_LIST_INCENTIVE_PERIODS_API, INC_LIST_INCENTIVE_RESULTS_API, INC_UPDATE_… | #166 E8 奨励金・規則version（incentive-and-rul… | #197 `INC-09` 画面 SCR-047 奨励金計算結果照会（#198, #199, #200） | — |
| SPEC-TECH-INC_INCENTIVE_CALC, ADR-014, REPORT_DB, OPS_DB | #166 E8 奨励金・規則version（incentive-and-rul… | #201 `INC-10` バッチ登録 INCENTIVE_MONTHLY（判定日実行・日次枠外・alert 連携） | — |
| INC_LIST_RATE_VERSIONS_API, INC_GET_RATE_VERSION_API, INC_CREATE_RATE_VERSION_API, INC_UP… | #166 E8 奨励金・規則version（incentive-and-rul… | #202 `INC-11` API 料率版の起票・更新・一覧・取得・承認依頼・取下げ（INC_LIST_RATE_VERSIO… | — |
| INC_APPROVE_RATE_VERSION_API, INC_REJECT_RATE_VERSION_API, INC_PREVIEW_RATE_VERSION_ROLLB… | #166 E8 奨励金・規則version（incentive-and-rul… | #203 `INC-12` API 料率版の承認・差戻し・ロールバック（INC_APPROVE_RATE_VERSION, I… | — |
| INC_PREVIEW_RETRO_IMPACT_API, INC_CREATE_RETRO_APPROVAL_API, INC_UPDATE_RETRO_APPROVAL_IM… | #166 E8 奨励金・規則version（incentive-and-rul… | #204 `INC-13` API 遡及例外承認（INC_PREVIEW_RETRO_IMPACT, INC_CREATE_R… | — |
| INC_LIST_INCENTIVE_PERIODS_API, INC_LIST_INCENTIVE_RESULTS_API, INC_UPDATE_INCENTIVE_PAYM… | #166 E8 奨励金・規則version（incentive-and-rul… | #205 `INC-14` API 奨励金の期・結果・入金・再計算・確定（INC_LIST_INCENTIVE_PERIODS… | — |
| SPEC-INC-001, SPEC-INC-002, SPEC-INC-003, SPEC-INC-010, SPEC-INC-011 | #166 E8 奨励金・規則version（incentive-and-rul… | #206 `INC-15` 受入テスト incentive-and-rule-version（SCR-043〜047 の受入条… | — |
| SPEC-TECH-INC_INCENTIVE_CALC, INCENTIVE_PART2_DB, COMMON_DB, PF-07, PF-05, PF-06 | #166 E8 奨励金・規則version（incentive-and-rul… | #207 `INC-16` 受入テスト DS-INC-EDGE-01 厳格合格基準（ACC-02）— BR-INC-01 計算…（#208, #209） | — |
| SPEC-TECH-INC_RATE_VERSION, INCENTIVE_DB, PF-07, ADR-015, SPEC-INC-003 | #166 E8 奨励金・規則version（incentive-and-rul… | #210 `INC-17` 受入テスト TBL-RATE-01 ガバナンス（年 4 回・起票承認分離・将来発効・ロールバック追… | — |
| SPEC-TECH-INC_INCENTIVE_CALC, COMMON_DB, SPEC-INC-011, SPEC-TECH-DLV_DELIVERY_COMPLETION_… | #166 E8 奨励金・規則version（incentive-and-rul… | #211 `INC-Q` 確認事項（incentive-and-rule-version）— 6 件 | — |
| COMMON_DB §4.5 `br_inc01_incentive_with_tax()` / `settlement_tax_from_gross()` の実装 | #166 E8 奨励金・規則version（incentive-and-rul… | — | cross-cutting（COMMON_DB）の範囲。本 feature は呼び出すだけ（#174（INC-03-a））。 |
| STL_SETTLEMENT_TAX_TECH §4.6 テストベクター V1〜V5 / S1〜S5 | #166 E8 奨励金・規則version（incentive-and-rul… | — | settlement-and-correction の TECH。#208（INC-16-a） は参照実行のみで、settlement 側の issue は分解しない（指示どおり）。 |
| SCR-053（RPT-07 奨励金帳票）・SCR-056（RPT-12 規則変更・適用版帳票） | #166 E8 奨励金・規則version（incentive-and-rul… | — | reporting-and-print の範囲。本 feature は帳票が読む `incentive_result` / `incentive_delta` / `audit_log` を正しく書くことまで（#173（INC-03） / #178（INC-04） の DoD）。 |
| 訂正依頼の承認 `apply_correction_delta()` と `affects_closed_incentive_period` | #166 E8 奨励金・規則version（incentive-and-rul… | — | settlement-and-correction（PF-06）の範囲。#176（INC-03-c） は差額関数を提供し、起因側（STL）が同一トランザクションで呼ぶ。 |
| 業務日オープンジョブ BUSINESS_DAY_OPEN・SCR-066 手動オープン | #166 E8 奨励金・規則version（incentive-and-rul… | — | settlement-and-correction の範囲。#180（INC-04-b） は呼ばれる関数のみ（GAP-#190（INC-07））。 |
| SCR-005 / 006 での `RETRO_RATE_APPROVE` 個人付与 | #166 E8 奨励金・規則version（incentive-and-rul… | — | identity-and-participants の範囲（GAP-#197（INC-09））。 |
| SCR-060 通知センター・`report_run` 非同期基盤（cold 照会） | #166 E8 奨励金・規則version（incentive-and-rul… | — | notification / reporting-and-print の範囲。#205（INC-14） は受付と通知契約の呼出しのみ。 |
| 各 SPEC の 画面項目定義（SCR-043: 17、044: 20、045: 21、046: 19、047: 31 項目） | #166 E8 奨励金・規則version（incentive-and-rul… | — | brief の指示により件数のみ計上。各 FE sub-issue (a) が参照。 |
| ARCH-DEPLOYMENT, ADR-009, ARCH-NFR | #212 E16 インフラ・非機能（infra-nfr） | #213 `INF-01` AWS ランディングゾーン: Organizations 配下 3 アカウント（dev/stagi… | — |
| ARCH-DEPLOYMENT, ADR-009, ADR-010, ARCH-NFR | #212 E16 インフラ・非機能（infra-nfr） | #214 `INF-02` ネットワーク: VPC 3 層サブネット × 2 AZ・ALB（TLS 終端・mTLS 端末証明書… | — |
| ARCH-DEPLOYMENT, ADR-009, ADR-013, ARCH-NFR, ADR-007 | #212 E16 インフラ・非機能（infra-nfr） | #215 `INF-03` データ層: RDS PostgreSQL 17 Multi-AZ（db.t4g.medium・gp… | — |
| ARCH-DEPLOYMENT, ADR-014, ADR-009, ADR-007 | #212 E16 インフラ・非機能（infra-nfr） | #216 `INF-04` コンピュート: ECS Fargate app × 2（2 AZ、×3 へ水平拡張）・batch … | — |
| ARCH-DEPLOYMENT, ARCH-INTEGRATIONS, ADR-007, ARCH-NFR | #212 E16 インフラ・非機能（infra-nfr） | #217 `INF-05` シークレット・鍵管理: Secrets Manager（DB 5 ロール・Entra client… | — |
| ARCH-DEPLOYMENT, ADR-007, ARCH-NFR | #212 E16 インフラ・非機能（infra-nfr） | #218 `INF-06` CI/CD パイプライン: CodePipeline/CodeBuild（gate → test:… | — |
| ARCH-DEPLOYMENT, ADR-013, ARCH-NFR, COMMON_DB | #212 E16 インフラ・非機能（infra-nfr） | #219 `INF-07` S3 設計: バケット分離（添付／帳票・CSV 出力／会計 CSV・ACK 原本／ログエクスポート… | — |
| ARCH-NFR, ARCH-DEPLOYMENT, ADR-014, ADR-009, OPS_DB | #212 E16 インフラ・非機能（infra-nfr） | #220 `INF-08` 監視・アラート（NFR-OPS-01）: CloudWatch アラーム 4 分類＋業務・Rout… | — |
| ARCH-DEPLOYMENT, ARCH-NFR, ADR-009, ADR-013 | #212 E16 インフラ・非機能（infra-nfr） | #221 `INF-09` バックアップ・DR（NFR-AVL-03）: PITR 検証・月次手動スナップショット 13 か月… | — |
| ARCH-INTEGRATIONS, ADR-012, ARCH-DEPLOYMENT, ARCH-NFR | #212 E16 インフラ・非機能（infra-nfr） | #222 `INF-10` 会計 SFTP 接続基盤（IF-ACC-01）: NAT 固定 EIP の許可リスト登録依頼・発注… | — |
| ARCH-INTEGRATIONS, ADR-010, ARCH-DEPLOYMENT | #212 E16 インフラ・非機能（infra-nfr） | #223 `INF-11` 外部連携の環境準備: Entra アプリ登録 × 3（環境別 redirect URI）依頼・メー… | — |
| ARCH-DEPLOYMENT, ADR-009, ARCH-NFR | #212 E16 インフラ・非機能（infra-nfr） | #224 `INF-12` 環境構築 staging（本番同等: ミドルウェア版・DDL・設定値・rule_config 版、… | — |
| ARCH-NFR, ADR-013, ADR-014 | #212 E16 インフラ・非機能（infra-nfr） | #225 `INF-13` 性能・容量試験（NFR-PERF-01/02）: 層別 load test（hot p95 ≤ 2… | — |
| ARCH-NFR, ARCH-DEPLOYMENT, ADR-010, ADR-009 | #212 E16 インフラ・非機能（infra-nfr） | #226 `INF-14` セキュリティ検証（NFR-SEC-01/03/04、SEC-IAM-02、09-06）: TLS … | — |
| ARCH-DEPLOYMENT, ARCH-NFR, ADR-013, ADR-007, ADR-014, ARCH-INTEGRATIONS | #212 E16 インフラ・非機能（infra-nfr） | #227 `INF-15` 運用手順書（RFP 11-02）: リリース窓・通知済み保守 5 営業日前・DR・purge ru… | — |
| ARCH-NFR, ARCH-DEPLOYMENT | #212 E16 インフラ・非機能（infra-nfr） | #228 `INF-16` アラート演習（ACC-05）・運用引継ぎ: staging でのアラート一覧実演（4 分類＋業務）… | — |
| ARCH-NFR, ADR-009, ASSUMPTIONS, ARCH-INTEGRATIONS, ARCH-DEPLOYMENT, ADR-014, ADR-013 | #212 E16 インフラ・非機能（infra-nfr） | #229 `INF-Q` 確認事項（infra-nfr）— 4 件 | — |
| nfr.md §1 NFR-AVL-02（オフライン継続）・FR-NOTIFY-02・FR-SETTLE-03・IF-ACC-01 のアプリ側 | #212 E16 インフラ・非機能（infra-nfr） | — | offline-continuity／notification／settlement／accounting-integration feature の issue。本 epic は基盤（接続・監視・閾値の測定）のみ。 |
| ADR-014 日次ジョブ順序・冪等性・batch_job_run・遅延アラート 3 段の判定ロジック | #212 E16 インフラ・非機能（infra-nfr） | — | reporting-and-print feature（REPORT_DB・SCR-057）。#216（INF-04） はスケジューラとタスク定義、#220（INF-08） はアラーム配線のみ。 |
| OPS_DB（health_snapshot・alert_event）の DDL と SCR-065・OPS_* API | #212 E16 インフラ・非機能（infra-nfr） | — | operations-monitoring feature。#220（INF-08-b） は SNS からの取込アダプタだけを担当。 |
| integrations.md §4 印刷エージェント本体（Windows サービス・ESC/POS・PDF 印刷） | #212 E16 インフラ・非機能（infra-nfr） | — | reporting-and-print feature（印刷ジョブ・FORM-DEL-01 等）。#223（INF-11） は MSI 配布計画と社内 CA 証明書のみ。 |
| ADR-009 案 F 大阪 cold-standby | #212 E16 インフラ・非機能（infra-nfr） | — | Q15 の回答待ち（#229（INF-17））。保証が必要になった場合のみ追加見積の別 epic。 |
| deployment.md §2.4 費用分担・12-08 定期費用 | #212 E16 インフラ・非機能（infra-nfr） | — | 商務条件。#224（INF-12-b） の費用表を PM が見積・契約へ反映する範囲で扱い、タスク化しない。 |
| LOT_DB, PF-03, ADR-001, ADR-013 | #230 E2 ロット・品目（lot-and-item-master） | #231 `LOT-01` DB migration LOT_DB（item_master / lot / lot_appra… | — |
| LOT_PART2_DB, LOT_DB, TRADE_DB, PF-03 | #230 E2 ロット・品目（lot-and-item-master） | #232 `LOT-02` DB migration LOT_PART2_DB（lot_adjustment） | — |
| LOT_CREATE_LOT_API, LOT_LIST_LOTS_API, LOT_GET_LOT_API, LOT_UPDATE_LOT_STATUS_API, SPEC-L… | #230 E2 ロット・品目（lot-and-item-master） | #233 `LOT-03` API ロット（LOT_CREATE_LOT, LOT_LIST_LOTS, LOT_GET_LO… | — |
| LOT_CREATE_LOT_APPRAISAL_API, LOT_CREATE_LOT_ADJUSTMENT_API, LOT_LIST_LOT_ADJUSTMENTS_API… | #230 E2 ロット・品目（lot-and-item-master） | #234 `LOT-04` API 目利き・調整（LOT_CREATE_LOT_APPRAISAL, LOT_CREATE_L… | — |
| LOT_CREATE_LOT_ATTACHMENT_API, LOT_GET_LOT_ATTACHMENT_API, LOT_WITHDRAW_LOT_ATTACHMENT_AP… | #230 E2 ロット・品目（lot-and-item-master） | #235 `LOT-05` API 受入証憑（LOT_CREATE_LOT_ATTACHMENT, LOT_GET_LOT_A… | — |
| LOT_CREATE_ITEM_API, LOT_GET_ITEM_API, LOT_UPDATE_ITEM_API, LOT_UPDATE_ITEM_STATUS_API, S… | #230 E2 ロット・品目（lot-and-item-master） | #236 `LOT-06` API 品目マスタ更新（LOT_CREATE_ITEM, LOT_GET_ITEM, LOT_UP… | — |
| LOT_LIST_ITEMS_API, LOT_LIST_ITEM_CATEGORIES_API, LOT_LIST_ITEM_CANDIDATES_API, SPEC-LOT-… | #230 E2 ロット・品目（lot-and-item-master） | #237 `LOT-07` API 品目マスタ検索（LOT_LIST_ITEMS, LOT_LIST_ITEM_CATEGOR… | — |
| LOT_OFFLINE_CODE_RESERVATION, LOT_RESERVE_LOT_CODES_API, COMMON_DB, OFFLINE_DB, SPEC-LOT-… | #230 E2 ロット・品目（lot-and-item-master） | #238 `LOT-08` 業務ロジック LOT_OFFLINE_CODE_RESERVATION（番号帯予約・同期時範囲検査）（#239, #240） | — |
| SPEC-LOT-001, LOT_CREATE_LOT_API, LOT_RESERVE_LOT_CODES_API, LOT_LIST_ITEM_CANDIDATES_API… | #230 E2 ロット・品目（lot-and-item-master） | #241 `LOT-09` 画面 SCR-012 ロット受付 | — |
| SPEC-LOT-002, LOT_LIST_LOTS_API, STL_GET_OPEN_BUSINESS_DAY_API, PF-01 | #230 E2 ロット・品目（lot-and-item-master） | #242 `LOT-10` 画面 SCR-013 ロット一覧 | — |
| SPEC-LOT-003, LOT_GET_LOT_API, LOT_UPDATE_LOT_STATUS_API, LOT_CREATE_LOT_ATTACHMENT_API, … | #230 E2 ロット・品目（lot-and-item-master） | #243 `LOT-11` 画面 SCR-014 ロット詳細 | — |
| SPEC-LOT-004, LOT_GET_LOT_API, LOT_CREATE_LOT_APPRAISAL_API, OFF_CREATE_SYNC_RECEIPT_API,… | #230 E2 ロット・品目（lot-and-item-master） | #244 `LOT-12` 画面 SCR-015 目利き結果入力 | — |
| SPEC-LOT-010, LOT_GET_LOT_API, LOT_CREATE_LOT_ADJUSTMENT_API, LOT_LIST_LOT_ADJUSTMENTS_AP… | #230 E2 ロット・品目（lot-and-item-master） | #245 `LOT-13` 画面 SCR-016 ロット属性調整 | — |
| SPEC-LOT-011, LOT_LIST_ITEMS_API, LOT_LIST_ITEM_CATEGORIES_API | #230 E2 ロット・品目（lot-and-item-master） | #246 `LOT-14` 画面 SCR-017 品目マスタ一覧 | — |
| SPEC-LOT-012, LOT_GET_ITEM_API, LOT_LIST_ITEM_CATEGORIES_API, LOT_CREATE_ITEM_API, LOT_UP… | #230 E2 ロット・品目（lot-and-item-master） | #247 `LOT-15` 画面 SCR-018 品目マスタ編集 | — |
| SPEC-LOT-001, SPEC-LOT-002, SPEC-LOT-003, SPEC-LOT-004, SPEC-LOT-010, SPEC-LOT-011, SPEC-… | #230 E2 ロット・品目（lot-and-item-master） | #248 `LOT-16` 受入テスト lot-and-item-master（SCR-012〜018 E2E） | — |
| SPEC-LOT-001, SPEC-LOT-004, LOT_OFFLINE_CODE_RESERVATION, OFF_CREATE_SYNC_RECEIPT_API, PF… | #230 E2 ロット・品目（lot-and-item-master） | #249 `LOT-17` 受入テスト（特殊）オフライン継続・番号帯予約・再送競合の結合 | — |
| SPEC-LOT-001, SPEC-LOT-004, SPEC-LOT-010, SPEC-LOT-011, LOT_DB, LOT_OFFLINE_CODE_RESERVAT… | #230 E2 ロット・品目（lot-and-item-master） | #250 `LOT-Q` 確認事項（lot-and-item-master）— 6 件 | — |
| SCR-012 / SCR-015 のデータ・API マッピング OFF_CREATE_SYNC_RECEIPT・端末キュー共通処理 | #230 E2 ロット・品目（lot-and-item-master） | — | offline-continuity feature の issue（#293（OFF-02） / #297（OFF-03））。本 feature は呼び出し側の接続と業務キー形式のみ担当。 |
| SCR-012 / 013 / 016 の STL_GET_OPEN_BUSINESS_DAY | #230 E2 ロット・品目（lot-and-item-master） | — | settlement-and-correction の API。依存として参照。 |
| SCR-018 / SCR-014 の AUD_LIST_ENTITY_AUDIT_LOGS | #230 E2 ロット・品目（lot-and-item-master） | — | audit-trail の API。 |
| SCR-013 A5 の cold 非同期照会（report_run・SCR-049・SCR-060 通知） | #230 E2 ロット・品目（lot-and-item-master） | — | reporting-and-print / notification の責務。本 feature は空一覧と導線のみ。 |
| SCR-016 A10 / SCR-040 締め解除申請の入口・ウィンドウ管理 | #230 E2 ロット・品目（lot-and-item-master） | — | settlement-and-correction（STL_BUSINESS_DAY_UNLOCK）。本 feature はモード表示と GUC 連携のみ。 |
| SCR-014 A6 ロット削除 API / SCR-018 削除エンドポイント | #230 E2 ロット・品目（lot-and-item-master） | — | 提供しない（Appendix B、E-AUD-005）。DB の forbid_delete は #231（LOT-01） に含む。 |
| 品目マスタの移行取込（Wave 1、MIG-01/02） | #230 E2 ロット・品目（lot-and-item-master） | — | data-migration epic の責務。#236（LOT-06） の検証関数を共用する契約のみ。 |
| SCR-013 対象外節 RPT-02 ロット履歴帳票 | #230 E2 ロット・品目（lot-and-item-master） | — | reporting-and-print。 |
| TRADE_DB, PF-04, ADR-001, ADR-002, ADR-006, ADR-013, IAM_PARTY_ELIGIBILITY | #251 E3 相対取引（negotiated-trade） | #252 `TRD-01` DB migration TRADE_DB（trade / trade_line・確定／取消／買い…（#253, #254, #255） | — |
| TRD_TRADE_CONFIRM, TRD_CREATE_TRADE_API, SPEC-TRD-001, TRADE_DB, LOT_DB, COMMON_DB, ADR-0… | #251 E3 相対取引（negotiated-trade） | #256 `TRD-02` 業務ロジック TRD_TRADE_CONFIRM（相対取引の確定・TRD_CREATE_TRADE）（#257, #258） | — |
| TRD_TRADE_CANCEL_RESTORE, TRD_CANCEL_TRADE_API, TRD_PREVIEW_TRADE_CANCEL_API, SPEC-TRD-01… | #251 E3 相対取引（negotiated-trade） | #259 `TRD-03` 業務ロジック TRD_TRADE_CANCEL_RESTORE（取引取消とロット数量復元・TRD_…（#260, #261） | — |
| TRD_LIST_TRADES_API, TRD_GET_TRADE_API, TRD_CREATE_ARCHIVE_SEARCH_API, SPEC-TRD-002, SPEC… | #251 E3 相対取引（negotiated-trade） | #262 `TRD-04` API 取引照会（TRD_LIST_TRADES, TRD_GET_TRADE, TRD_CREA… | — |
| TRD_LIST_BUYER_CANDIDATES_API, TRD_LIST_LOT_CANDIDATES_API, TRD_GET_LOT_SALES_API, SPEC-T… | #251 E3 相対取引（negotiated-trade） | #263 `TRD-05` API 入力補助・分割販売（TRD_LIST_BUYER_CANDIDATES, TRD_LIST… | — |
| SPEC-TRD-001, TRD_CREATE_TRADE_API, TRD_LIST_BUYER_CANDIDATES_API, TRD_LIST_LOT_CANDIDATE… | #251 E3 相対取引（negotiated-trade） | #264 `TRD-06` 画面 SCR-019 相対取引入力（#265, #266, #267） | — |
| SPEC-TRD-002, TRD_LIST_TRADES_API, TRD_CREATE_ARCHIVE_SEARCH_API, RPT_GET_REPORT_RUN_API,… | #251 E3 相対取引（negotiated-trade） | #268 `TRD-07` 画面 SCR-020 取引一覧・検索 | — |
| SPEC-TRD-003, TRD_GET_TRADE_API, STL_LIST_CORRECTIONS_API, AUD_LIST_ENTITY_AUDIT_LOGS_API… | #251 E3 相対取引（negotiated-trade） | #269 `TRD-08` 画面 SCR-021 取引詳細（#270, #271） | — |
| SPEC-TRD-010, TRD_GET_TRADE_API, TRD_PREVIEW_TRADE_CANCEL_API, TRD_CANCEL_TRADE_API | #251 E3 相対取引（negotiated-trade） | #272 `TRD-09` 画面 SCR-022 取引取消 | — |
| SPEC-TRD-011, TRD_GET_LOT_SALES_API, LOT_LIST_LOT_ADJUSTMENTS_API | #251 E3 相対取引（negotiated-trade） | #273 `TRD-10` 画面 SCR-023 ロット分割販売状況 | — |
| SPEC-TRD-001, SPEC-TRD-002, SPEC-TRD-003, SPEC-TRD-010, SPEC-TRD-011 | #251 E3 相対取引（negotiated-trade） | #274 `TRD-11` 受入テスト negotiated-trade（SCR-019〜023 E2E） | — |
| SPEC-TRD-001, TRD_TRADE_CONFIRM, TRADE_DB, IAM_PARTY_ELIGIBILITY, ADR-002 | #251 E3 相対取引（negotiated-trade） | #275 `TRD-12` 受入テスト（特殊）FR-AITAI-02 拒否理由 × 許可≠承認・同時実行・売り越し 0 | — |
| SPEC-TRD-010, SPEC-TRD-003, SPEC-TRD-011, TRD_TRADE_CANCEL_RESTORE, ADR-004, PF-06 | #251 E3 相対取引（negotiated-trade） | #276 `TRD-13` 受入テスト（特殊）取消復元・締め解除モード・締め後 reverse/delta の整合 | — |
| SPEC-TRD-010, SPEC-TRD-011, SPEC-LOT-010, TRD_TRADE_CANCEL_RESTORE, LOT_DB, SPEC-TRD-001,… | #251 E3 相対取引（negotiated-trade） | #277 `TRD-Q` 確認事項（negotiated-trade）— 4 件 | — |
| SCR-020 / SCR-021 の STL_LIST_CORRECTIONS・訂正依頼起票 SCR-037〜039 | #251 E3 相対取引（negotiated-trade） | — | settlement-and-correction の責務。本 feature は表示と導線のみ。 |
| SCR-021 ⑦ 取引伝票印刷 SCR-058 / FORM-TRADE-01 | #251 E3 相対取引（negotiated-trade） | — | reporting-and-print。 |
| SCR-020 cold 非同期検索の実行基盤（report_run・SCR-060 通知） | #251 E3 相対取引（negotiated-trade） | — | reporting-and-print / notification。本 feature は起票 API（#262（TRD-04））と導線のみ。 |
| 資格判定関数 `assert_party_eligible_as_buyer()` と候補の資格 SQL | #251 E3 相対取引（negotiated-trade） | — | identity-and-participants（IAM_PARTY_ELIGIBILITY TECH）。本 feature は呼び出しと 4 コードの透過のみ。 |
| SCR-019 / 022 の締め解除申請（SCR-040）・ウィンドウ・影響レコード一覧 | #251 E3 相対取引（negotiated-trade） | — | settlement-and-correction（STL_BUSINESS_DAY_UNLOCK）。 |
| `trade.delivery_completed_at` の書込み（完納確定）・引渡し例外 SCR-030 | #251 E3 相対取引（negotiated-trade） | — | delivery feature。TRADE_DB のバイパス条件のみ #255（TRD-01-c） に含む。 |
| せり由来取引の生成（`trade_kind=AUCTION`） | #251 E3 相対取引（negotiated-trade） | — | auction-result（#24（AUC-02））。本 feature は同じトリガー群を提供し、一覧・詳細で表示する。 |
| `trade.eligibility_warning` を立てる移行ロール経路 | #251 E3 相対取引（negotiated-trade） | — | data-migration epic。#254（TRD-01-b） は接続ロール分岐の存在のみテスト。 |
| SPEC-NOTIFICATION_DB-001, SPEC-COMMON_DB-001, SPEC-IAM_DB-001 | #278 E11 通知（notification） | #279 `NTF-01` DB マイグレーション NOTIFICATION_DB（notification・notifica… | — |
| SPEC-NOTIFICATION_DB-001, SPEC-NTF-001, SPEC-NTF-002, SPEC-COMMON_DB-001, SPEC-IAM_DB-001… | #278 E11 通知（notification） | #280 `NTF-02` 通知ディスパッチャ（イベント捕捉・受信者展開・重複防止・in-app 作成・日次まとめ） | — |
| SPEC-NOTIFICATION_DB-001, SPEC-NTF-001, SPEC-NTF-003, SPEC-OPS_DB-001, ADR-009 | #278 E11 通知（notification） | #281 `NTF-03` メール送信ワーカー・webhook（配信サービス連携・再試行・Critical 5 分監視・bou… | — |
| SPEC-NTF-001, NTF_GET_UNREAD_COUNT, NTF_LIST_NOTIFICATIONS, NTF_UPDATE_NOTIFICATION_READ,… | #278 E11 通知（notification） | #282 `NTF-04` API 通知センター（NTF_GET_UNREAD_COUNT, NTF_LIST_NOTIFIC… | — |
| SPEC-NTF-002, NTF_LIST_NOTIFICATION_SETTINGS, NTF_GET_NOTIFICATION_SETTING, NTF_UPDATE_NO… | #278 E11 通知（notification） | #283 `NTF-05` API 通知設定（NTF_LIST_NOTIFICATION_SETTINGS, NTF_GET_… | — |
| SPEC-NTF-003, NTF_LIST_DELIVERY_LOGS, NTF_LIST_DELIVERY_ATTEMPTS, NTF_RESEND_NOTIFICATION… | #278 E11 通知（notification） | #284 `NTF-06` API 通知送信ログ・手動再送（NTF_LIST_DELIVERY_LOGS, NTF_LIST_… | — |
| SPEC-NTF-001, NTF_GET_UNREAD_COUNT, NTF_LIST_NOTIFICATIONS, NTF_UPDATE_NOTIFICATION_READ | #278 E11 通知（notification） | #285 `NTF-07` 画面 SCR-060 通知センター（未読バッジ・Critical 全画面バナーを含む） | — |
| SPEC-NTF-002, NTF_LIST_NOTIFICATION_SETTINGS, NTF_GET_NOTIFICATION_SETTING, NTF_UPDATE_NO… | #278 E11 通知（notification） | #286 `NTF-08` 画面 SCR-061 通知設定 | — |
| SPEC-NTF-003, NTF_LIST_DELIVERY_LOGS, NTF_LIST_DELIVERY_ATTEMPTS, NTF_RESEND_NOTIFICATION… | #278 E11 通知（notification） | #287 `NTF-09` 画面 SCR-062 通知送信ログ | — |
| SPEC-NTF-001, SPEC-NTF-002, SPEC-NTF-003 | #278 E11 通知（notification） | #288 `NTF-10` 受入テスト notification（SCR-060／061／062 E2E・配信シナリオ） | — |
| SPEC-NOTIFICATION_DB-001, SPEC-NTF-003, ADR-009 | #278 E11 通知（notification） | #289 `NTF-11` メール配信 結合テスト（サンドボックス・bounce／complaint・5 分 SLA・再試行・… | — |
| SPEC-NTF-001, SPEC-NTF-002, SPEC-NOTIFICATION_DB-001, SPEC-NTF-003 | #278 E11 通知（notification） | #290 `NTF-Q` 確認事項（notification）— 4 件 | — |
| SCR-060 対象外: 通知の原因となる業務操作・運用アラートの一覧 | #278 E11 通知（notification） | — | 各発生元 feature と operations-monitoring の領域。 |
| SCR-061 対象外: 業務しきい値（rule_config）の変更、利用者メールアドレスの登録 | #278 E11 通知（notification） | — | ADR-005 のリリース手順と identity-and-participants（SCR-005）。 |
| IAM_LIST_USER_CANDIDATES（SCR-061 の個人受信者候補） | #278 E11 通知（notification） | — | identity-and-participants の API を呼び出すだけ。 |
| SCR-065 側の NOTIFICATION_FAILED／NOTIFICATION_SLA_MISSED アラートの一覧・対応 | #278 E11 通知（notification） | — | operations-monitoring（#310（OPS-06）／07）。本 feature は #307（OPS-02） の発行ライブラリを呼ぶ。 |
| OFFLINE_DB, ADR-011, ADR-013 | #291 E6 オフライン（offline-continuity） | #292 `OFF-01` DB マイグレーション OFFLINE_DB（sync_receipt・sync_conflict… | — |
| SPEC-TECH-OFF_OFFLINE_SYNC, OFF_CREATE_SYNC_RECEIPT_API, OFF_RESOLVE_SYNC_CONFLICT_API, O… | #291 E6 オフライン（offline-continuity） | #293 `OFF-02` 業務ロジック OFF_OFFLINE_SYNC（受領・冪等判定・業務行適用・競合解決）（#294, #295, #296） | — |
| SPEC-TECH-OFF_OFFLINE_SYNC, OFFLINE_DB, ADR-011, SPEC-OFF-001, PF-09 | #291 E6 オフライン（offline-continuity） | #297 `OFF-03` PWA 端末キュー基盤（Service Worker・IndexedDB pending_ops・… | — |
| SPEC-OFF-001, OFF_LIST_SYNC_RECEIPTS_API, OFF_GET_SYNC_SUMMARY_API, OFF_CREATE_SYNC_RECEI… | #291 E6 オフライン（offline-continuity） | #298 `OFF-04` 画面 SCR-033 オフライン同期状況 | — |
| SPEC-OFF-002, OFF_LIST_SYNC_CONFLICTS_API, OFF_GET_SYNC_CONFLICT_API, OFF_RESOLVE_SYNC_CO… | #291 E6 オフライン（offline-continuity） | #299 `OFF-05` 画面 SCR-034 同期競合処理 | — |
| OFF_CREATE_SYNC_RECEIPT_API, OFF_LIST_SYNC_RECEIPTS_API, OFF_GET_SYNC_SUMMARY_API, SPEC-T… | #291 E6 オフライン（offline-continuity） | #300 `OFF-06` API 同期受領（OFF_CREATE_SYNC_RECEIPT, OFF_LIST_SYNC_R… | — |
| OFF_LIST_SYNC_CONFLICTS_API, OFF_GET_SYNC_CONFLICT_API, OFF_RESOLVE_SYNC_CONFLICT_API, SP… | #291 E6 オフライン（offline-continuity） | #301 `OFF-07` API 同期競合（OFF_LIST_SYNC_CONFLICTS, OFF_GET_SYNC_CO… | — |
| SPEC-OFF-001, SPEC-OFF-002, SPEC-TECH-OFF_OFFLINE_SYNC, PF-09, ADR-011 | #291 E6 オフライン（offline-continuity） | #302 `OFF-08` 受入テスト offline-continuity（SCR-033 / 034 E2E・通信断シミュ… | — |
| ADR-011, SPEC-TECH-OFF_OFFLINE_SYNC, OFFLINE_DB | #291 E6 オフライン（offline-continuity） | #303 `OFF-09` インフラ PWA 配信と端末識別（Service Worker 配信・mTLS 端末証明書 CN … | — |
| SPEC-OFF-001, SPEC-OFF-002, SPEC-TECH-OFF_OFFLINE_SYNC, OFFLINE_DB, ADR-011 | #291 E6 オフライン（offline-continuity） | #304 `OFF-Q` 確認事項（offline-continuity）— 3 件 | — |
| OFFLINE_DB §4.0 端末ローカルキュー（論理構造） | #291 E6 オフライン（offline-continuity） | — | DB 外のため migration issue にせず、#297（OFF-03-a）（IndexedDB スキーマ）に含める。 |
| SCR-012 / SCR-015 / SCR-028 のオフライン入力 UI とキューへの積み方 | #291 E6 オフライン（offline-continuity） | — | 各画面の feature（lot-and-item-master / delivery）が所有。本 feature は共通基盤（#297（OFF-03））と契約だけを持つ。 |
| LOT_OFFLINE_CODE_RESERVATION（予約ロット番号帯、`reserve_number_block()`） | #291 E6 オフライン（offline-continuity） | — | lot-and-item-master の TECH。#294（OFF-02-a） は番号帯の範囲検査を呼ぶだけ。 |
| SCR-034 ⑲ の遷移先（SCR-014 / 016 / 029 / 030 / 037 / 040）の各画面 | #291 E6 オフライン（offline-continuity） | — | 遷移先は各 feature。本 feature はリンクと案内のみ（#299（OFF-05-a））。 |
| SCR-065 端末・サービスの死活監視 | #291 E6 オフライン（offline-continuity） | — | operations-monitoring の範囲。 |
| 各 SPEC の 画面項目定義（SCR-033: 25 項目、SCR-034: 21 項目） | #291 E6 オフライン（offline-continuity） | — | brief の指示により件数のみ計上。各 FE sub-issue (a) が参照。 |
| SPEC-OPS_DB-001, SPEC-COMMON_DB-001, ADR-003 | #305 E13 運用監視（operations-monitoring） | #306 `OPS-01` DB マイグレーション OPS_DB（health_snapshot・alert_event・トリ… | — |
| SPEC-OPS_DB-001, SPEC-NOTIFICATION_DB-001, SPEC-OPS-001 | #305 E13 運用監視（operations-monitoring） | #307 `OPS-02` 運用アラート発行ライブラリ（alert_event 起票・dedup・Critical 通知 OP… | — |
| SPEC-OPS_DB-001, SPEC-OPS-001, ADR-009, ADR-014 | #305 E13 運用監視（operations-monitoring） | #308 `OPS-03` 監視ワーカー（health_snapshot 1 分間隔・7 構成要素・HEALTH_DEGRAD… | — |
| ADR-014, SPEC-REPORT_DB-001, SPEC-OPS_DB-001, SPEC-RPT-023, SPEC-COMMON_DB-001 | #305 E13 運用監視（operations-monitoring） | #309 `OPS-05` ジョブ実行枠組み（batch_job_run 状態遷移・並走禁止・締切監視・遅延アラート 3 段） | — |
| SPEC-OPS-001, OPS_GET_HEALTH_SUMMARY, OPS_LIST_ALERTS, OPS_GET_MAINTENANCE_STATUS, OPS_AC… | #305 E13 運用監視（operations-monitoring） | #310 `OPS-06` API 運用監視（OPS_GET_HEALTH_SUMMARY, OPS_LIST_ALERTS,… | — |
| SPEC-OPS-001, OPS_GET_HEALTH_SUMMARY, OPS_LIST_ALERTS, OPS_GET_MAINTENANCE_STATUS, OPS_AC… | #305 E13 運用監視（operations-monitoring） | #311 `OPS-07` 画面 SCR-065 システム稼働状況（保守案内を含む） | — |
| SPEC-OPS-001, ADR-014 | #305 E13 運用監視（operations-monitoring） | #312 `OPS-08` 受入テスト operations-monitoring（SCR-065 E2E・4 分類演習 AC… | — |
| ADR-014, SPEC-RPT-023, SPEC-REPORT_DB-001 | #305 E13 運用監視（operations-monitoring） | #313 `OPS-09` 日次バッチ枠・遅延アラート演習（11:00 証跡・3 段アラート・worker 障害・再実行） | — |
| SPEC-OPS-001, SPEC-OPS_DB-001 | #305 E13 運用監視（operations-monitoring） | #314 `OPS-Q` 確認事項（operations-monitoring）— 2 件 | — |
| SCR-065 E5／E6／E16 の発行元（締め解除回数超過・異常ログイン・遡及版発効見送り） | #305 E13 運用監視（operations-monitoring） | — | アラートの発行は settlement-and-correction・identity-and-participants・incentive-and-rule-version 側の処理。本 epic は #307（OPS-02） の発行ライブラリと表示のみ。 |
| ADR-009 CloudWatch メトリクス・ログ検索・ダッシュボード | #305 E13 運用監視（operations-monitoring） | — | 生データは CloudWatch が正本で画面対象外（SCR-065 対象外）。基盤は infra-nfr epic。 |
| NFR-AVL-01 の正式な月次可用性報告（外形監視 uptime ログ） | #305 E13 運用監視（operations-monitoring） | — | 独立した外形監視の成果物。infra-nfr epic に申し送り（GAP-#313（OPS-09））。 |
| REPORT_DB §4.3 batch_job_run の DDL | #305 E13 運用監視（operations-monitoring） | — | DB ファイル単位の原則により reporting-and-print（#318（RPT-03））で起票。本 epic は書込み枠組み（#309（OPS-05））を持つ。 |
| SPEC-RPT-001, RPT_LIST_REPORTS, RPT_GET_DAILY_BATCH_STATUS, RPT_LIST_REPORT_RUNS, RPT_GET… | #315 E9 報告・出力・帳票（reporting-and-print） | #316 `RPT-01` 画面 SCR-048 レポートハブ | — |
| SPEC-RPT-001, SPEC-RPT-002, SPEC-RPT-003, SPEC-RPT-004, SPEC-RPT-005, SPEC-RPT-006, SPEC-… | #315 E9 報告・出力・帳票（reporting-and-print） | #317 `RPT-02` 帳票画面 共通コンポーネント（期間フィルタ・31 日検査・cold 案内・暫定バナー・タブ・ページ… | — |
| SPEC-REPORT_DB-001, SPEC-COMMON_DB-001, ADR-013, ADR-014 | #315 E9 報告・出力・帳票（reporting-and-print） | #318 `RPT-03` DB マイグレーション REPORT_DB（report_run・export_file・batc… | — |
| SPEC-RPT-001, RPT_LIST_REPORTS, RPT_GET_DAILY_BATCH_STATUS, RPT_LIST_REPORT_RUNS, RPT_GET… | #315 E9 報告・出力・帳票（reporting-and-print） | #319 `RPT-04` API レポートハブ・照会履歴（RPT_LIST_REPORTS, RPT_GET_DAILY_B… | — |
| SPEC-RPT-001, RPT_EXPORT_REPORT_CSV, RPT_GET_EXPORT_FILE, SPEC-REPORT_DB-001, SPEC-BIZDAY… | #315 E9 報告・出力・帳票（reporting-and-print） | #320 `RPT-05` 帳票 CSV 共通基盤と API（RPT_EXPORT_REPORT_CSV, RPT_GET_E… | — |
| SPEC-RPT-002, SPEC-RPT-003, RPT_GET_DAILY_TRADE_SUMMARY, RPT_LIST_LOT_HISTORY, RPT_LIST_P… | #315 E9 報告・出力・帳票（reporting-and-print） | #321 `RPT-06` API 日次帳票 RPT-01〜04（RPT_GET_DAILY_TRADE_SUMMARY, R… | — |
| SPEC-RPT-004, SPEC-RPT-005, RPT_GET_DAILY_SETTLEMENT, RPT_GET_ACCOUNTING_EXTRACT, SPEC-SE… | #315 E9 報告・出力・帳票（reporting-and-print） | #322 `RPT-07` API 照合・会計帳票 RPT-05／06（RPT_GET_DAILY_SETTLEMENT, R… | — |
| SPEC-RPT-006, SPEC-RPT-021, RPT_LIST_INCENTIVE_RESULTS, RPT_LIST_MONTHLY_BY_PARTY, RPT_LI… | #315 E9 報告・出力・帳票（reporting-and-print） | #323 `RPT-08` API 奨励金・月次帳票 RPT-07／10／11（RPT_LIST_INCENTIVE_RESU… | — |
| SPEC-RPT-006, SPEC-RPT-020, RPT_LIST_POST_LOCK_ADJUSTMENTS, RPT_GET_DISPUTE_SLA_SUMMARY, … | #315 E9 報告・出力・帳票（reporting-and-print） | #324 `RPT-09` API ロック後調整・紛争帳票 RPT-08／09（RPT_LIST_POST_LOCK_ADJU… | — |
| SPEC-RPT-022, RPT_LIST_RULE_CHANGES, RPT_LIST_APPLIED_RULE_VERSIONS, SPEC-INCENTIVE_DB-00… | #315 E9 報告・出力・帳票（reporting-and-print） | #325 `RPT-10` API 規則変更・適用版帳票 RPT-12（RPT_LIST_RULE_CHANGES, RPT_… | — |
| SPEC-RPT-023, RPT_LIST_BATCH_JOB_RUNS, RPT_GET_BATCH_JOB_RUN, RPT_RERUN_BATCH_JOB, SPEC-R… | #315 E9 報告・出力・帳票（reporting-and-print） | #326 `RPT-11` API バッチ実行状況（RPT_LIST_BATCH_JOB_RUNS, RPT_GET_BATC… | — |
| SPEC-RPT-024, RPT_LIST_PRINT_TARGETS, RPT_PREVIEW_PRINT_FORM, RPT_CREATE_PRINT_JOB, RPT_U… | #315 E9 報告・出力・帳票（reporting-and-print） | #327 `RPT-12` API 伝票印刷（RPT_LIST_PRINT_TARGETS, RPT_PREVIEW_PRIN… | — |
| ADR-014, SPEC-RPT-001, SPEC-RPT-021, SPEC-RPT-022, SPEC-RPT-023, SPEC-REPORT_DB-001 | #315 E9 報告・出力・帳票（reporting-and-print） | #328 `RPT-13` 帳票バッチ（DAILY_REPORT 事前生成・MONTHLY_REPORT 確定 CSV） | — |
| SPEC-REPORT_DB-001, ADR-013, SPEC-RPT-001, SPEC-AUD-001, SPEC-COMMON_DB-001 | #315 E9 報告・出力・帳票（reporting-and-print） | #329 `RPT-14` cold 非同期照会ランナー（report_run ARCHIVE_QUERY・15 分上限・結果… | — |
| SPEC-RPT-024, SPEC-DLV-002, SPEC-REPORT_DB-001, ADR-014 | #315 E9 報告・出力・帳票（reporting-and-print） | #330 `RPT-15` 印刷エージェント（現場 PC 常駐・localhost 受信・ESC/POS 80mm・A4 PD… | — |
| SPEC-RPT-024, SPEC-RPT-004, SPEC-DLV-002 | #315 E9 報告・出力・帳票（reporting-and-print） | #331 `RPT-16` 伝票様式 3 種のデザイン（FORM-DEL-01 80mm・FORM-TRADE-01 A4・F… | — |
| SPEC-RPT-002, RPT_GET_DAILY_TRADE_SUMMARY, RPT_LIST_LOT_HISTORY, RPT_EXPORT_REPORT_CSV, R… | #315 E9 報告・出力・帳票（reporting-and-print） | #332 `RPT-17` 画面 SCR-049 RPT-01/02 日次取引・ロット履歴 | — |
| SPEC-RPT-003, RPT_LIST_PARTICIPANT_VALIDITY, RPT_LIST_STALE_DELIVERIES, RPT_EXPORT_REPORT… | #315 E9 報告・出力・帳票（reporting-and-print） | #333 `RPT-18` 画面 SCR-050 RPT-03/04 参加者有効性・滞留引渡し | — |
| SPEC-RPT-004, RPT_GET_DAILY_SETTLEMENT, RPT_EXPORT_REPORT_CSV, RPT_GET_EXPORT_FILE | #315 E9 報告・出力・帳票（reporting-and-print） | #334 `RPT-19` 画面 SCR-051 RPT-05 日次照合表 | — |
| SPEC-RPT-005, ACC_LIST_EXPORT_BATCHES, RPT_GET_ACCOUNTING_EXTRACT, RPT_EXPORT_REPORT_CSV,… | #315 E9 報告・出力・帳票（reporting-and-print） | #335 `RPT-20` 画面 SCR-052 RPT-06 会計照合用出力 | — |
| SPEC-RPT-006, RPT_LIST_INCENTIVE_RESULTS, RPT_LIST_POST_LOCK_ADJUSTMENTS, RPT_EXPORT_REPO… | #315 E9 報告・出力・帳票（reporting-and-print） | #336 `RPT-21` 画面 SCR-053 RPT-07/08 奨励金・ロック後調整ログ（#337, #338, #339） | — |
| SPEC-RPT-020, RPT_GET_DISPUTE_SLA_SUMMARY, RPT_LIST_DISPUTE_SLA, RPT_EXPORT_REPORT_CSV, R… | #315 E9 報告・出力・帳票（reporting-and-print） | #340 `RPT-22` 画面 SCR-054 RPT-09 紛争・SLA | — |
| SPEC-RPT-021, RPT_LIST_MONTHLY_BY_PARTY, RPT_LIST_MONTHLY_BY_TRADE_KIND, RPT_EXPORT_REPOR… | #315 E9 報告・出力・帳票（reporting-and-print） | #341 `RPT-23` 画面 SCR-055 RPT-10/11 月次レポート | — |
| SPEC-RPT-022, RPT_LIST_RULE_CHANGES, RPT_LIST_APPLIED_RULE_VERSIONS, RPT_EXPORT_REPORT_CS… | #315 E9 報告・出力・帳票（reporting-and-print） | #342 `RPT-24` 画面 SCR-056 RPT-12 規則変更・適用版 | — |
| SPEC-RPT-023, RPT_LIST_BATCH_JOB_RUNS, RPT_GET_BATCH_JOB_RUN, RPT_RERUN_BATCH_JOB | #315 E9 報告・出力・帳票（reporting-and-print） | #343 `RPT-25` 画面 SCR-057 バッチ実行状況 | — |
| SPEC-RPT-024, RPT_LIST_PRINT_TARGETS, RPT_PREVIEW_PRINT_FORM, RPT_CREATE_PRINT_JOB, RPT_U… | #315 E9 報告・出力・帳票（reporting-and-print） | #344 `RPT-26` 画面 SCR-058 帳票プレビュー・印刷 | — |
| SPEC-RPT-001, SPEC-RPT-002, SPEC-RPT-003, SPEC-RPT-004, SPEC-RPT-005, SPEC-RPT-006, SPEC-… | #315 E9 報告・出力・帳票（reporting-and-print） | #345 `RPT-27` 受入テスト 帳票画面（SCR-048〜056 E2E・帳票別ロール・CSV 形式） | — |
| SPEC-RPT-023, SPEC-RPT-024 | #315 E9 報告・出力・帳票（reporting-and-print） | #346 `RPT-28` 受入テスト バッチ実行状況・印刷（SCR-057／058 E2E） | — |
| SPEC-RPT-004, SPEC-RPT-005, SPEC-RPT-021, SPEC-RPT-006, SPEC-ACCOUNTING_DB-001, ADR-004, … | #315 E9 報告・出力・帳票（reporting-and-print） | #347 `RPT-29` 帳票金額整合テスト（RPT-05 ↔ RPT-06 ↔ 会計 batch・RPT-10 ↔ 日次合… | — |
| SPEC-RPT-006, SPEC-RPT-021, SPEC-INCENTIVE_DB-001 | #315 E9 報告・出力・帳票（reporting-and-print） | #348 `RPT-30` RPT-07 奨励金帳票の検証（INC テストベクトル・次期差額・期段階・CSV 期状態列） | — |
| SPEC-RPT-024, SPEC-DLV-002 | #315 E9 報告・出力・帳票（reporting-and-print） | #349 `RPT-31` 印刷 実機テスト（現場 PC 6 台相当・80mm 4 台・A4 2 台・ダイアログなし・p95 … | — |
| ADR-014, SPEC-RPT-001, SPEC-RPT-023 | #315 E9 報告・出力・帳票（reporting-and-print） | #350 `RPT-32` 帳票バッチ 性能テスト（ピーク 1,560 取引・10:45 目標・+30% 成長・並列 2 本） | — |
| SPEC-RPT-001, SPEC-RPT-020, SPEC-RPT-021, SPEC-REPORT_DB-001, SPEC-RPT-002, SPEC-RPT-003,… | #315 E9 報告・出力・帳票（reporting-and-print） | #351 `RPT-Q` 確認事項（reporting-and-print）— 10 件 | — |
| SCR-048 対象外: self-service の帳票作成・テンプレート編集（FR-RPT-03） | #315 E9 報告・出力・帳票（reporting-and-print） | — | 対象外と明記（RFP 08-02）。 |
| SCR-052 の会計送信・ACK・再出力操作、ACC_LIST_EXPORT_BATCHES・ACC_GET_EXPORT_FILE | #315 E9 報告・出力・帳票（reporting-and-print） | — | accounting-integration（#16（ACC-04）／05）。本 feature は呼び出すだけ。 |
| SCR-053 の奨励金計算・入金記録・期の確定、SCR-056 の料率版の起票・承認・ロールバック・遡及 | #315 E9 報告・出力・帳票（reporting-and-print） | — | incentive-and-rule-version。本 feature は結果の表示のみ。 |
| SCR-053 RPT-08 の締め解除・訂正の操作、`締め解除:{id}` 接頭辞の付与（AS-296） | #315 E9 報告・出力・帳票（reporting-and-print） | — | settlement-and-correction の TECH（STL_UNLOCK_MODE_WRITE・STL_CORRECTION_APPROVAL）。 |
| SCR-057 の BUSINESS_DAY_OPEN・ACC_EXPORT・ACC_ACK_POLL・INCENTIVE_MONTHLY・QUALIFICATION_EXPIR… | #315 E9 報告・出力・帳票（reporting-and-print） | — | 各 feature（STL・ACC・INC・IAM・XC）が持つ。本 feature は表示（SCR-057）と DAILY_REPORT／MONTHLY_REPORT のみ。 |
| SCR-058 対象外: SCR-067 窓口クイック照会の画面、印刷エージェントの導入・プリンタ IP 設定 | #315 E9 報告・出力・帳票（reporting-and-print） | — | SCR-067 は delivery、導入は発注者情報システム部門の運用。 |
| SCR-063 の cold 検索クエリ（report_code SCR-063）、SCR-020／047 の cold 検索 | #315 E9 報告・出力・帳票（reporting-and-print） | — | ランナー（#329（RPT-14））は本 feature、各クエリプラグインは audit-trail（#48（AUD-04））・negotiated-trade・incentive。 |
| AUDIT_DB v_audit_search（RPT-02・RPT-08 が読む） | #315 E9 報告・出力・帳票（reporting-and-print） | — | audit-trail（#46（AUD-02））。 |
| BIZDAY_DB, STL_BUSINESS_DAY_LOCK_TECH, STL_BUSINESS_DAY_UNLOCK_TECH, ADR-006, ADR-004 | #352 E7 照合・締め・訂正（settlement-and-correct… | #353 `STL-01` DB マイグレーション BIZDAY_DB（business_day・unlock_request… | — |
| SETTLEMENT_DB, STL_CORRECTION_APPROVAL_TECH, ADR-004, ADR-013 | #352 E7 照合・締め・訂正（settlement-and-correct… | #354 `STL-02` DB マイグレーション SETTLEMENT_DB（settlement_daily・correc…（#355, #356, #357） | — |
| STL_BUSINESS_DAY_OPEN_TECH, BIZDAY_DB, SPEC-STL-009, ADR-006, ADR-014 | #352 E7 照合・締め・訂正（settlement-and-correct… | #358 `STL-03` 業務ロジック STL_BUSINESS_DAY_OPEN（02:00 自動オープン・遅延オープン・…（#359, #360） | — |
| STL_BUSINESS_DAY_LOCK_TECH, BIZDAY_DB, SETTLEMENT_DB, SPEC-STL-002, ADR-006, ADR-004 | #352 E7 照合・締め・訂正（settlement-and-correct… | #361 `STL-04` 業務ロジック STL_BUSINESS_DAY_LOCK（締めプレビュー・ロック 1 トランザクシ…（#362, #363） | — |
| STL_CORRECTION_APPROVAL_TECH, SETTLEMENT_DB, SPEC-STL-005, SPEC-STL-003, ADR-004, PF-06 | #352 E7 照合・締め・訂正（settlement-and-correct… | #364 `STL-05` 業務ロジック STL_CORRECTION_APPROVAL（承認・却下・apply_correc…（#365, #366） | — |
| STL_BUSINESS_DAY_UNLOCK_TECH, BIZDAY_DB, SPEC-STL-006, PF-01, ADR-006, ADR-012 | #352 E7 照合・締め・訂正（settlement-and-correct… | #367 `STL-06` 業務ロジック STL_BUSINESS_DAY_UNLOCK（締め解除の申請・承認・却下・再締め・…（#368, #369, #370） | — |
| STL_UNLOCK_MODE_WRITE_TECH, BIZDAY_DB, SPEC-STL-006, ADR-004, ADR-006 | #352 E7 照合・締め・訂正（settlement-and-correct… | #371 `STL-07` 業務ロジック STL_UNLOCK_MODE_WRITE（締め解除モードの行単位バイパス・Unlo…（#372, #373） | — |
| STL_SETTLEMENT_TAX_TECH, COMMON_DB, SETTLEMENT_DB, ADR-008, ADR-005 | #352 E7 照合・締め・訂正（settlement-and-correct… | #374 `STL-08` 業務ロジック STL_SETTLEMENT_TAX（税の不変関数 2 本: br_inc01_in…（#375, #376） | — |
| STL_GET_OPEN_BUSINESS_DAY_API, STL_LIST_BUSINESS_DAYS_API, STL_GET_BUSINESS_DAY_OPEN_STAT… | #352 E7 照合・締め・訂正（settlement-and-correct… | #377 `STL-09` API 業務日・日次照合 照会 (STL_GET_OPEN_BUSINESS_DAY, STL_L… | — |
| STL_OPEN_BUSINESS_DAY_API, STL_CANCEL_BUSINESS_DAY_OPEN_API, STL_PREVIEW_BUSINESS_DAY_CLO… | #352 E7 照合・締め・訂正（settlement-and-correct… | #378 `STL-10` API 業務日 操作 (STL_OPEN_BUSINESS_DAY, STL_CANCEL_BUS… | — |
| STL_LIST_CORRECTION_TARGETS_API, STL_PREVIEW_CORRECTION_LEVEL_API, STL_CREATE_CORRECTION_… | #352 E7 照合・締め・訂正（settlement-and-correct… | #379 `STL-11` API 訂正依頼 起票 (STL_LIST_CORRECTION_TARGETS, STL_PRE… | — |
| STL_LIST_CORRECTIONS_API, STL_GET_CORRECTION_API, STL_GET_CORRECTION_ATTACHMENT_API, STL_… | #352 E7 照合・締め・訂正（settlement-and-correct… | #380 `STL-12` API 訂正依頼 一覧・承認 (STL_LIST_CORRECTIONS, STL_GET_COR… | — |
| STL_PREVIEW_BUSINESS_DAY_UNLOCK_API, STL_LIST_UNLOCK_REQUESTS_API, STL_GET_UNLOCK_REQUEST… | #352 E7 照合・締め・訂正（settlement-and-correct… | #381 `STL-13` API 締め解除 照会 (STL_PREVIEW_BUSINESS_DAY_UNLOCK, STL… | — |
| STL_CREATE_UNLOCK_REQUEST_API, STL_APPROVE_UNLOCK_REQUEST_API, STL_REJECT_UNLOCK_REQUEST_… | #352 E7 照合・締め・訂正（settlement-and-correct… | #382 `STL-14` API 締め解除 操作 (STL_CREATE_UNLOCK_REQUEST, STL_APPRO… | — |
| STL_LIST_DISPUTES_API, STL_GET_DISPUTE_API, STL_CREATE_DISPUTE_ATTACHMENT_API, STL_GET_DI… | #352 E7 照合・締め・訂正（settlement-and-correct… | #383 `STL-15` API 紛争 照会・添付 (STL_LIST_DISPUTES, STL_GET_DISPUTE,… | — |
| STL_CREATE_DISPUTE_API, STL_UPDATE_DISPUTE_API, STL_CLOSE_DISPUTE_API, SPEC-STL-008 | #352 E7 照合・締め・訂正（settlement-and-correct… | #384 `STL-16` API 紛争 操作 (STL_CREATE_DISPUTE, STL_UPDATE_DISPUTE… | — |
| SPEC-STL-008, SPEC-STL-007, SETTLEMENT_DB, NOTIFICATION_DB | #352 E7 照合・締め・訂正（settlement-and-correct… | #385 `STL-17` バッチ 紛争 SLA 判定（自動エスカレーション・解決期限超過の Critical 通知） | — |
| SPEC-STL-009, STL_GET_BUSINESS_DAY_OPEN_STATUS_API, STL_OPEN_BUSINESS_DAY_API, STL_CANCEL… | #352 E7 照合・締め・訂正（settlement-and-correct… | #386 `STL-18` 画面 SCR-066 業務日オープン操作 | — |
| SPEC-STL-002, STL_GET_OPEN_BUSINESS_DAY_API, STL_PREVIEW_BUSINESS_DAY_CLOSE_API, STL_CLOS… | #352 E7 照合・締め・訂正（settlement-and-correct… | #387 `STL-19` 画面 SCR-036 業務日ロック操作 | — |
| SPEC-STL-001, STL_LIST_BUSINESS_DAYS_API, STL_GET_DAILY_SETTLEMENT_API, STL_LIST_SETTLEME… | #352 E7 照合・締め・訂正（settlement-and-correct… | #388 `STL-20` 画面 SCR-035 日次照合表 | — |
| SPEC-STL-003, STL_LIST_CORRECTION_TARGETS_API, STL_PREVIEW_CORRECTION_LEVEL_API, STL_CREA… | #352 E7 照合・締め・訂正（settlement-and-correct… | #389 `STL-21` 画面 SCR-037 訂正依頼起票（#390, #391, #392） | — |
| SPEC-STL-004, STL_LIST_CORRECTIONS_API, STL_PREVIEW_CORRECTION_LEVEL_API | #352 E7 照合・締め・訂正（settlement-and-correct… | #393 `STL-22` 画面 SCR-038 訂正依頼一覧 | — |
| SPEC-STL-005, STL_GET_CORRECTION_API, STL_GET_CORRECTION_ATTACHMENT_API, STL_APPROVE_CORR… | #352 E7 照合・締め・訂正（settlement-and-correct… | #394 `STL-23` 画面 SCR-039 訂正依頼承認（#395, #396, #397） | — |
| SPEC-STL-006, STL_PREVIEW_BUSINESS_DAY_UNLOCK_API, STL_LIST_UNLOCK_REQUESTS_API, STL_GET_… | #352 E7 照合・締め・訂正（settlement-and-correct… | #398 `STL-24` 画面 SCR-040 締め解除申請 | — |
| SPEC-STL-007, STL_LIST_DISPUTES_API | #352 E7 照合・締め・訂正（settlement-and-correct… | #399 `STL-25` 画面 SCR-041 紛争一覧 | — |
| SPEC-STL-008, STL_GET_DISPUTE_API, STL_CREATE_DISPUTE_API, STL_UPDATE_DISPUTE_API, STL_CL… | #352 E7 照合・締め・訂正（settlement-and-correct… | #400 `STL-26` 画面 SCR-042 紛争詳細（#401, #402, #403） | — |
| SPEC-STL-001, SPEC-STL-002, SPEC-STL-003, SPEC-STL-004, SPEC-STL-005, SPEC-STL-006, SPEC-… | #352 E7 照合・締め・訂正（settlement-and-correct… | #404 `STL-27` 受入テスト settlement-and-correction（9 画面の受入条件 E2E） | — |
| ADR-006, ADR-004, STL_BUSINESS_DAY_OPEN_TECH, STL_BUSINESS_DAY_LOCK_TECH, STL_BUSINESS_DA… | #352 E7 照合・締め・訂正（settlement-and-correct… | #405 `STL-28` 受入テスト 業務日の不変条件・並行性（OPEN 1 件・取消競合・ロック順序・ウィンドウ期限） | — |
| ADR-004, PF-06, STL_CORRECTION_APPROVAL_TECH, SETTLEMENT_DB | #352 E7 照合・締め・訂正（settlement-and-correct… | #406 `STL-29` 受入テスト 締め後訂正の統制（maker≠checker 直呼び・バイパス悪用・強制 2 段・繰越… | — |
| STL_SETTLEMENT_TAX_TECH, ADR-008, SETTLEMENT_DB, ACCOUNTING_DB | #352 E7 照合・締め・訂正（settlement-and-correct… | #407 `STL-30` 受入テスト 税テストベクトルの共通検証（BR-INC-01 110/100 と精算内税 10/11… | — |
| SPEC-STL-003, SETTLEMENT_DB, ADR-004, SPEC-STL-006, SPEC-STL-002, BIZDAY_DB, STL_BUSINESS… | #352 E7 照合・締め・訂正（settlement-and-correct… | #408 `STL-Q` 確認事項（settlement-and-correction）— 10 件 | — |
| SCR-040 A8・PF-01 §4.1 — 遷移先 6 画面（SCR-016・019・022・026・028・030）の締め解除モード UI | #352 E7 照合・締め・訂正（settlement-and-correct… | — | 各画面は lot-and-item-master・negotiated-trade・delivery・auction-result の SPEC に属し、本 feature は UnlockModeGuard と組込み契約（#371（STL-07））だけを持つ。 |
| SCR-053 RPT-08 ロック後調整ログ、SCR-051 RPT-05 印刷、SCR-054 RPT-09 紛争・SLA | #352 E7 照合・締め・訂正（settlement-and-correct… | — | reporting-and-print の範囲（README §5）。本 feature は突合キー（監査 reason 接頭辞・correction_request_id）を提供するのみ。 |
| SCR-059 会計連携状況、SUPPLEMENT batch の起票・送信・ACK、`accounting_exported_at` の設定トリガー | #352 E7 照合・締め・訂正（settlement-and-correct… | — | accounting-integration（PF-08、ADR-012）の範囲。本 feature は承認コミット後の起票依頼（#364（STL-05） §4.6）と遅着 ACK フック（#369（STL-06-b））の契約だけを持つ。 |
| 奨励金の翌期差分 `incentive_delta` の生成（PF-07、FR-INC-03）、`br_inc01_incentive_with_tax` の月次バッチからの呼出し | #352 E7 照合・締め・訂正（settlement-and-correct… | — | incentive-and-rule-version の範囲。本 feature は関数と `affects_closed_incentive_period` の入力を提供する。 |
| SCR-005／006 の `UNLOCK_APPROVE`・`CORRECTION_L2_APPROVE` の個人付与、SCR-009 共用承認キュー | #352 E7 照合・締め・訂正（settlement-and-correct… | — | identity-and-participants の範囲（README §5）。 |
| 市場カレンダー（COMMON_DB `market_calendar`）の登録・保守 | #352 E7 照合・締め・訂正（settlement-and-correct… | — | 画面が無く運用手順のみ（SCR-066 Q2、GAP-#361（STL-04））。保守画面を設ける場合は別 issue。 |
| 02:00 バッチの worker 基盤・スケジューラ（ADR-014 Fargate worker）、`batch_job_run` 表、SCR-065／057 のアラート・再… | #352 E7 照合・締め・訂正（settlement-and-correct… | — | infra-nfr／reporting-and-print／operations-monitoring の範囲。本 feature はジョブ本体（#358（STL-03）・06-b・17）のみ。 |
| SCR-030 引渡し例外の自動再計算（締め前）、SCR-022 取引取消、SCR-016 ロット調整 | #352 E7 照合・締め・訂正（settlement-and-correct… | — | README §5 で明示的に対象外。締め後の経路（訂正依頼・締め解除モード）だけが本 feature。 |
| 各 SPEC の 画面項目定義（詳細表）・NFR 節・関連資料 | #352 E7 照合・締め・訂正（settlement-and-correct… | — | 項目数・NFR は FE issue の作業内容と DoD に取り込み済みで、個別 issue にはしない。 |

## 3. 案件固有の制約を受ける項目

Product A では、金額や取引資格に直結する業務ルールを共通処理に混ぜると、受入基準（DS-INC-EDGE-01 など）を個別に証明できなくなる。
そこで次の 5 つの制約を持つ Issue をラベル `constraint:*` と Project の `Constraint` 欄で分け、制約付き Issue は sub-issue で「実装」と「テストベクトル」を別担当にした（§1.1）。

| 制約 | Issue 数 |
|---|---|
| BR-INC-01 完納奨励金 | 19 |
| TBL-RATE-01 料率版 | 12 |
| 許可≠承認（BR-PERM-01） | 24 |
| 締め後訂正（reverse/delta・2 段階承認） | 26 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | 63 |

**完納奨励金（BR-INC-01）を特に分けた理由:** 奨励金は「完納確定」という人の操作（#99 SCR-029）を起点に、引渡し・訂正・料率版・月次バッチの 4 feature をまたいで金額が決まる。
完納の判定（#90 DLV-03）、計算（#173 INC-03）、税係数 110/100・円未満切り捨ての共通関数（#374 STL-08）、受入テストベクトル（#207 INC-16、#113 DLV-18、#407 STL-30）を、それぞれ独立した Issue にした。
どこかを共通の「精算処理」に含めると、完納取消（DLV-Q の確認項目 DLV-22）や期またぎ（INC-Q の INC-19）の回答が来たとき、影響範囲を Issue 単位で追えなくなるためである。

| 制約 | Issue | 分離した理由（Issue 本文 §備考 より） |
|---|---|---|
| BR-INC-01 完納奨励金 | #83 `MIG-Q` 確認事項（data-migration）— 2 件 | 確認項目 #83（MIG-11） が BR-#167（INC-01） 完納奨励金 の前提（回答で金額・資格・締めの扱いが変わる）。項目単位で回答を追跡するため確認 Issue 内でも制約ラベルを付ける。 |
| BR-INC-01 完納奨励金 | #90 `DLV-03` 業務ロジック DLV_DELIVERY_COMPLETION_CONFIRM（完納確定 c… | BR-#167（INC-01） で単独 issue にする理由: ① 完納の有無が奨励金（金額）の算入可否を直接決める、② 締め済み業務日への例外書込みで監査・税務上の説明責任を負う、③ 6 回目例外（D57）と訂正（PF-06）の両方から完納状態が左右されるため専用 test vector が要る。完納の取消経路は未定（GAP-#86（DLV-02）、#116（DLV-22））。 |
| BR-INC-01 完納奨励金 | #99 `DLV-07` 画面 SCR-029 引渡し詳細（完納確定） | BR-#167（INC-01） で単独 issue にする理由: 完納確定ボタンは奨励金の算入条件（完納）を人が確定する唯一の UI であり、誤操作・二重押下・オフライン時の挙動がそのまま金額に響く。完納確定の取消経路がない（SCR-029 Q4、#116（DLV-22））。 |
| BR-INC-01 完納奨励金 | #108 `DLV-13` API 完納確定（DLV_CONFIRM_COMPLETION） | BR-#167（INC-01）: 他 API と束ねず 1 API 1 issue とする（resource 単位 3〜6 本の原則の例外）。完納の書込み経路はこれ 1 本だけで、奨励金の算入条件を決めるため、監査・権限・冪等性の扱いを他の記録 API と混ぜない。 |
| BR-INC-01 完納奨励金 | #113 `DLV-18` 受入テスト BR-INC-01 完納状態の横断（完納→奨励金対象・6 回目算入・完納後の例… | BR-#167（INC-01） で単独 issue にする理由: 完納は delivery が書き、金額は incentive が計算し、取消は settlement の訂正が担う — 3 feature にまたがる状態遷移で、どの feature の受入テストにも収まらないため。 |
| BR-INC-01 完納奨励金 | #116 `DLV-Q` 確認事項（delivery）— 6 件 | 確認項目 #116（DLV-22） が BR-#167（INC-01） 完納奨励金 の前提（回答で金額・資格・締めの扱いが変わる）。項目単位で回答を追跡するため確認 Issue 内でも制約ラベルを付ける。 |
| BR-INC-01 完納奨励金 | #170 `INC-02` DB マイグレーション INCENTIVE_PART2_DB（incentive_resu… | BR-#167（INC-01） で単独 issue: 奨励金の金額と差額を持つ表で、「確定期は不変・翌期差額」（FR-#173（INC-03））を DB 制約で強制する。入金 3 列の手入力（AS-089）は #211（INC-21） で確認。 |
| BR-INC-01 完納奨励金 | #173 `INC-03` 業務ロジック INC_INCENTIVE_CALC（候補行・入金記録・判定日バッチ・再計算… | BR-#167（INC-01） で単独 issue: ① 金額を決める唯一の処理、② 税係数 110/100 と切捨て順序（料率適用後に先に切捨てると 1 円ずれる、§4.7 ケース 3）、③ 確定期は不変で差額のみ、④ 完納（delivery）・入金（手入力）・料率版（INC_RATE_VERSION）・訂正（settlement）の 4 feature の状態に依存。DS-INC-EDGE-01 の数値は仮置き（AS-286、#2… |
| BR-INC-01 完納奨励金 | #197 `INC-09` 画面 SCR-047 奨励金計算結果照会 | BR-#167（INC-01） で単独 issue: 金額の説明責任（FR-AUDIT-03、全行に版と発効日）と、算入条件を決める入金の手入力（AS-089）・期の確定（不変化）を照合部門が行う唯一の画面。入金経路・確定の職務分離・期の帰属は #211（INC-21） / #211（INC-20）。 |
| BR-INC-01 完納奨励金 | #201 `INC-10` バッチ登録 INCENTIVE_MONTHLY（判定日実行・日次枠外・alert 連携） | BR-#167（INC-01）: 金額を確定させる処理の起動であり、失敗時に部分計算を残さない（期全体 rollback）ことを運用面でも保証する。 |
| BR-INC-01 完納奨励金 | #205 `INC-14` API 奨励金の期・結果・入金・再計算・確定（INC_LIST_INCENTIVE_PER… | BR-#167（INC-01）: 入金記録 API は算入条件（期限内全額）の入力そのもので、整数円・未来日時不可・理由必須・確定期不可を API と DB の二重で守る。 |
| BR-INC-01 完納奨励金 | #207 `INC-16` 受入テスト DS-INC-EDGE-01 厳格合格基準（ACC-02）— BR-INC-0… | BR-#167（INC-01） で単独 issue: 奨励金の合格基準そのもので、通常の受入テストと分けて「金額差 0 円」を監査可能にする。数値は仮置き（#211（INC-19））。 |
| BR-INC-01 完納奨励金 | #211 `INC-Q` 確認事項（incentive-and-rule-version）— 6 件 | 確認項目 #211（INC-18）, #211（INC-19）, #211（INC-20） が BR-#167（INC-01） 完納奨励金 の前提（回答で金額・資格・締めの扱いが変わる）。項目単位で回答を追跡するため確認 Issue 内でも制約ラベルを付ける。 |
| BR-INC-01 完納奨励金 | #323 `RPT-08` API 奨励金・月次帳票 RPT-07／10／11（RPT_LIST_INCENTIVE_… | - **制約 BR-#167（INC-01） で分離する理由**: #322（RPT-07）／10 は完納奨励金（完納確定・期限内入金・×110/100・次期差額 DS-INC-EDGE-01）の計算結果を表示・集計する帳票で、INC の計算ロジックと同じテストベクトル（AS-286 仮置き数値）で突合する必要がある。計算自体は INC 側で、本 issue は表示のみ。 |
| BR-INC-01 完納奨励金 | #336 `RPT-21` 画面 SCR-053 RPT-07/08 奨励金・ロック後調整ログ | - **制約 BR-#167（INC-01） で分離する理由**: #322（RPT-07） タブは完納奨励金の判定結果・適用料率版・次期差額を照合事務局が支払確定に使う画面で、INC の計算テストベクトル（DS-INC-EDGE-01）と同じ seed で表示を突合する。#323（RPT-08） タブは post-close-correction の性質だが 1 画面 SPEC のため本 issue にまとめ、API 側（#324（… |
| BR-INC-01 完納奨励金 | #348 `RPT-30` RPT-07 奨励金帳票の検証（INC テストベクトル・次期差額・期段階・CSV 期状態列） | - **制約 BR-#167（INC-01） で分離する理由**: 帳票は計算しないが、完納奨励金の全ルール（完納確定・tax 110/100・次期差額・DS-INC-EDGE-01）の表示が照合事務局の支払確定の根拠になるため、INC の境界ケースと同じ seed で突合する専用テストが要る。 |
| BR-INC-01 完納奨励金 | #351 `RPT-Q` 確認事項（reporting-and-print）— 10 件 | 確認項目 #351（RPT-38） が BR-#167（INC-01） 完納奨励金 の前提（回答で金額・資格・締めの扱いが変わる）。項目単位で回答を追跡するため確認 Issue 内でも制約ラベルを付ける。 |
| BR-INC-01 完納奨励金 | #374 `STL-08` 業務ロジック STL_SETTLEMENT_TAX（税の不変関数 2 本: br_inc0… | BR-#167（INC-01） として分離する理由: 110/100（奨励金）と 10/110（精算内税）は別規定で、1 関数にまとめると奨励金に内税式が使われる誤りを招く（プロトタイプのコメント誤記が実例）。テストベクターは incentive feature（#173（INC-03） 奨励金計算）と共用し、キーは INC 側で採番されるため本 issue では「#173（INC-03）」と記す。数値は AS-291 の仮置き（RF… |
| BR-INC-01 完納奨励金 | #407 `STL-30` 受入テスト 税テストベクトルの共通検証（BR-INC-01 110/100 と精算内税 1… | BR-#167（INC-01） として分離する理由: 110/100 と 10/110 の取り違えは金額を直接狂わせ、奨励金・精算・会計の 3 feature を跨ぐため、feature 単位の受入では検出できない。数値は AS-291 の仮置き（GAP-#386（STL-18））。 |
| TBL-RATE-01 料率版 | #167 `INC-01` DB マイグレーション INCENTIVE_DB（rate_version・rate_li… | TBL-RATE-01 で単独 issue: 料率は `rule_config` にもコードにも置かず版表だけが正（ADR-005 選択肢 C 不採用）で、年 4 回・分離・将来日・ロールバックの 4 規則を DB 制約で強制する。年度開始月 4 月（AS-010、第 2 回 Q10 未回答）は #211（INC-22） で確認。 |
| TBL-RATE-01 料率版 | #178 `INC-04` 業務ロジック INC_RATE_VERSION（起票・承認依頼・承認・差戻し・取下げ・発効… | TBL-RATE-01 で単独 issue: 年 4 回（会計年度、承認 + ロールバック、取下げ・差戻しは数えない）、起票・承認分離（+ ロールバックは第 3 者）、将来発効日（遡及は例外経路のみ）、追跡可能なロールバック（直前版に戻す・差額）を 1 状態機械で守る。業務日オープンへのフックの所有は STL 側（GAP-#190（INC-07））。 |
| TBL-RATE-01 料率版 | #183 `INC-05` 画面 SCR-043 料率version一覧 | TBL-RATE-01: 改定回数は BE 集計値をそのまま表示（FE で再計算しない）。「発効見送り」の情報源（`alert_event`）が API に含まれるかは #202（INC-11） で確認（GAP-#194（INC-08））。閲覧ロール範囲 AS-177 は INC-24。 |
| TBL-RATE-01 料率版 | #186 `INC-06` 画面 SCR-044 料率version編集 | TBL-RATE-01: 将来発効日と年 4 回の事前検査を UI で先出しする画面。入力精度・0% の許容（AS-172）は INC-24、事前検査タイミング（AS-170）は #211（INC-22）。 |
| TBL-RATE-01 料率版 | #190 `INC-07` 画面 SCR-045 料率version承認・ロールバック | TBL-RATE-01: 承認分離（E-INC-003）・年 4 回（E-INC-001）・将来日（E-INC-002）・ロールバック第 3 者（E-INC-012）を 1 画面で扱う。発行前確定（RACI-01）をチェックで足りるかは #211（INC-22）。 |
| TBL-RATE-01 料率版 | #194 `INC-08` 画面 SCR-046 遡及適用影響プレビュー | TBL-RATE-01 の例外経路（遡及）を扱う唯一の画面。申請者 = 起票者可否（AS-240）、上限見込み（AS-241）、却下後再申請不可、次回業務日オープン発効（AS-243）は #211（INC-23）。影響額の算出式は BR-#167（INC-01）（#176（INC-03-c） と同式）。 |
| TBL-RATE-01 料率版 | #202 `INC-11` API 料率版の起票・更新・一覧・取得・承認依頼・取下げ（INC_LIST_RATE_VE… | TBL-RATE-01: 一覧 API が「改定回数 n/4」と「起票可否」の正。発効見送りの情報源（OPS_DB `alert_event`）を一覧に含める設計が API 設計書にあるかは実装時に確認（GAP-#194（INC-08））。 |
| TBL-RATE-01 料率版 | #203 `INC-12` API 料率版の承認・差戻し・ロールバック（INC_APPROVE_RATE_VERSIO… | TBL-RATE-01: 承認とロールバックは年 4 回に数える 2 操作で、監査理由の書式（`料率版承認: v{n}（照合部門長の発行前確定あり）`）を固定する。 |
| TBL-RATE-01 料率版 | #204 `INC-13` API 遡及例外承認（INC_PREVIEW_RETRO_IMPACT, INC_CREA… | TBL-RATE-01 の例外経路。影響額の算出は BR-#167（INC-01） の式（#176（INC-03-c））を共用する。 |
| TBL-RATE-01 料率版 | #210 `INC-17` 受入テスト TBL-RATE-01 ガバナンス（年 4 回・起票承認分離・将来発効・ロール… | TBL-RATE-01 で単独 issue: 規則が「年度」「人」「日付」の 3 軸にまたがり、画面単位の受入条件では年度境界と発効連鎖を通せないため。 |
| TBL-RATE-01 料率版 | #325 `RPT-10` API 規則変更・適用版帳票 RPT-12（RPT_LIST_RULE_CHANGES, … | - **制約 TBL-RATE-01 で分離する理由**: 料率版の年 4 回・起票者≠承認者・ロールバック・遡及の記録を説明責任として出す帳票で、回数の数え方（AS-170）と版解決（ADR-015）を INC と同じ定義で検証する必要がある。 |
| TBL-RATE-01 料率版 | #342 `RPT-24` 画面 SCR-056 RPT-12 規則変更・適用版 | - **制約 TBL-RATE-01 で分離する理由**: 年 4 回の改定回数・遡及の例外承認・ロールバックを表示する画面で、INC の料率版画面（SCR-043〜046）と同じ seed・同じ用語で検証する。 |
| 許可≠承認（BR-PERM-01） | #24 `AUC-02` 業務ロジック AUC_AUCTION_SESSION_CLOSE（せりセッション確定と取引… | - permit-vs-approval: 落札者の資格は確定時に TRADE_DB と同じ関数で ①状態→②許可→③承認→④種別 の順に判定し、E-TRD-008/003/004/009 を行番号付きで返す。入力時は警告のみ（AS-169）で確定時に DB が拒否するという二段構えが本 feature 固有のため独立 issue。 |
| 許可≠承認（BR-PERM-01） | #31 `AUC-05` 画面 SCR-024 せり結果連続入力 | - permit-vs-approval: 候補表示では許可失効・承認失効・状態を別の警告文言で示し（⑮⑯）、確定時の E6/E7/E8 も別文言で行番号付きで出す。記録は止めず確定で拒否する二段構え（AS-169）を画面で正しく表現する必要があるため独立 issue。 |
| 許可≠承認（BR-PERM-01） | #40 `AUC-09` 受入テスト（特殊）せり確定→取引生成の結合（全体 ROLLBACK・maker≠check… | - permit-vs-approval: せり落札者にも許可≠承認の 3 コードを確定時・変更時の両方で適用することを feature 横断で保証する専用テスト。 |
| 許可≠承認（BR-PERM-01） | #41 `AUC-Q` 確認事項（auction-result）— 3 件 | 確認項目 #41（AUC-11） が 許可≠承認（BR-PERM-01） の前提（回答で金額・資格・締めの扱いが変わる）。項目単位で回答を追跡するため確認 Issue 内でも制約ラベルを付ける。 |
| 許可≠承認（BR-PERM-01） | #73 `MIG-03` 列単位マッピング定義 mapping/v1,v2,v3/*.csv（テンプレート 3 世代… | `permit-vs-approval` で分離する理由: 許可と承認は別の参加根拠・別の列・別の状態機械（RFP 12-06 失格条件、ADR-002）。台帳 1 枚の「許可／承認番号」列を `party_type` で振り分け誤ると資格判定（`party_is_eligible`）が狂うため、マッピングを独立レビュー対象にする。 |
| 許可≠承認（BR-PERM-01） | #75 `MIG-05` Wave 1 ロード: party・party_status_history・item_m… | `permit-vs-approval` で分離する理由: W1 は `permit_*` と `approval_*` を別列へ写す唯一の工程で、誤ると稼働初日から BR-PERM-01 判定が誤る。`market_calendar` は W2 の `business_day` 生成と Q19 繰下げの前提（business-day）でもある。 |
| 許可≠承認（BR-PERM-01） | #119 `IAM-02` DB migration PARTY_DB（party・party_status_hist… | - permit-vs-approval: 許可（仲卸）と承認（売買参加者）を別列・別状態機械・別履歴 kind で保持する ADR-002 の最終防衛線が本 migration であり、CHECK／トリガーの組み合わせが他 feature と異なるため独立 issue として切り出す |
| 許可≠承認（BR-PERM-01） | #127 `IAM-08` API 参加者（IAM_LIST_PARTIES, IAM_GET_PARTY, IAM_… | - permit-vs-approval: 一覧の期限条件・応答・登録入力を許可／承認で分離し「資格」の共通語で括らない（RFP 12-06）。種別に該当しない資格項目の送信は DB に渡す前に 400（AS-327）。他 feature の一覧 API と共通化できないため独立 issue |
| 許可≠承認（BR-PERM-01） | #130 `IAM-09` API 参加資格申請（IAM_CREATE_QUALIFICATION_REQUEST, … | - permit-vs-approval: 申請の kind はサーバーが party_type から決め、本文の指定より優先、不一致は E-IAM-023。エンドポイントの検査順（権限→理由→maker≠checker→PENDING→証跡→期間）が TECH §4.4 固有のため独立 issue |
| 許可≠承認（BR-PERM-01） | #134 `IAM-11` API 承認待ちキュー・失効警告（IAM_LIST_APPROVAL_QUEUE, IAM… | - permit-vs-approval: 資格の行とタブを許可／承認で分け、共通語で括らない。訂正・締め解除の閲覧規則を混ぜないため、STL 側の一覧 API と統合せず独立 issue |
| 許可≠承認（BR-PERM-01） | #135 `IAM-12` 業務ロジック IAM_PARTY_ELIGIBILITY（BR-PERM-01 取引確定時… | - permit-vs-approval: 仲卸は許可列のみ、売買参加者は承認列のみを見て、拒否理由を E-TRD-003／004 に分ける（12-06 の「同一視」を避ける）。状態判定を先に置く順序が業務固有のため独立 issue |
| 許可≠承認（BR-PERM-01） | #138 `IAM-13` 業務ロジック IAM_PARTY_STATUS_TRANSITION（参加資格の一時停止・… | - permit-vs-approval: §4.1 No.4 で決めた 1 組の列だけを読み書きし、もう一方に触れない。遷移表は形が同じでも列・kind・通知を分けるため、汎用ワークフローと共通化せず独立 issue |
| 許可≠承認（BR-PERM-01） | #149 `IAM-20` 画面 SCR-007 参加者一覧 | - permit-vs-approval: 列・絞り込み・バッジを許可／承認で分け「資格」の共通語で括らない。プロトタイプの 1 列・1 条件からの作り直しであり他一覧と部品共有できないため独立 issue |
| 許可≠承認（BR-PERM-01） | #153 `IAM-21` 画面 SCR-008 参加者詳細・編集 | - permit-vs-approval: 許可グループと承認グループを別部品にし、該当しない側は「対象外」で入力欄を持たない。登録後の番号・期間は読取専用（申請経由のみ）。資格の入力規則が種別で分岐する画面は本画面だけのため独立 issue |
| 許可≠承認（BR-PERM-01） | #157 `IAM-22` 画面 SCR-009 承認待ち一覧 | - permit-vs-approval: 資格種別フィルタと行表示を許可／承認で分ける（ADR-002）。3 種の承認規則を混ぜない表示のため、訂正一覧 SCR-038 と部品共有せず独立 issue |
| 許可≠承認（BR-PERM-01） | #158 `IAM-23` 画面 SCR-010 承認依頼詳細 | - permit-vs-approval: ①⑥⑦⑨㉑ は申請の資格種別だけを表示し反対側を出さない。プレビューが許可／承認で項目名（許可番号／承認番号）を変えるため SCR-039／040 の承認画面と部品共有せず独立 issue |
| 許可≠承認（BR-PERM-01） | #161 `IAM-24` 画面 SCR-011 失効警告一覧 | - permit-vs-approval: 両タブを同時表示する切替を設けず、件数・見出し・通知を分ける（ADR-002）。許可／承認で別の通知・別一覧を要求する FR-PARTY-03 固有の画面のため独立 issue |
| 許可≠承認（BR-PERM-01） | #163 `IAM-26` 検証 許可≠承認 分離（ADR-002・BR-PERM-01）横断テスト | - permit-vs-approval: 失格条件に直結するため受入テストとは別に独立 issue とし、Constraint フィールドで追跡する |
| 許可≠承認（BR-PERM-01） | #165 `IAM-Q` 確認事項（identity-and-participants）— 6 件 | 確認項目 #165（IAM-30）, #165（IAM-32） が 許可≠承認（BR-PERM-01） の前提（回答で金額・資格・締めの扱いが変わる）。項目単位で回答を追跡するため確認 Issue 内でも制約ラベルを付ける。 |
| 許可≠承認（BR-PERM-01） | #252 `TRD-01` DB migration TRADE_DB（trade / trade_line・確定／取… | - permit-vs-approval: 確定時の資格判定を単一真偽（プロトタイプ BR-PERM-01）から 4 コード（状態／許可／承認／種別）に分割し、確定後の買い手変更（せり落札者変更）でも同じ関数・同じ順序で再判定する。IAM の関数契約に依存するため DB 単位で独立 issue にする。 |
| 許可≠承認（BR-PERM-01） | #256 `TRD-02` 業務ロジック TRD_TRADE_CONFIRM（相対取引の確定・TRD_CREATE_T… | - permit-vs-approval: 拒否理由 3 を E-TRD-003（許可）／E-TRD-004（承認）／E-TRD-008（状態）／E-TRD-009（種別）に分けて返し、API は DB の HINT を言い換えない。許可≠承認（RFP 12-06、ADR-002）を守る実装・テストの単位として独立させる。 |
| 許可≠承認（BR-PERM-01） | #263 `TRD-05` API 入力補助・分割販売（TRD_LIST_BUYER_CANDIDATES, TRD_… | - permit-vs-approval: 候補を「許可」「承認」別に判定し、表示でも区別する（候補に出ない理由を同一語にしない）。候補 API は入力補助であり正は DB だが、両者の不一致が窓口での誤案内に直結するため独立 issue。 |
| 許可≠承認（BR-PERM-01） | #264 `TRD-06` 画面 SCR-019 相対取引入力 | - permit-vs-approval: E3（許可失効）・E4（承認失効）・E5（状態）を別文言で表示し、候補空状態でも「許可／承認」を区別する。FE は DB の理由を言い換えない（ADR-001）。 |
| 許可≠承認（BR-PERM-01） | #275 `TRD-12` 受入テスト（特殊）FR-AITAI-02 拒否理由 × 許可≠承認・同時実行・売り越し 0 | - permit-vs-approval: 本テストは「許可≠承認」を実装横断で保証する唯一の場であり、通常の受入テスト（#274（TRD-11））と分けて独立させる。 |
| 締め後訂正（reverse/delta・2 段階承認） | #13 `ACC-03` 業務ロジック ACC_EXPORT_ACK §4.6（締め後訂正の SUPPLEMENT … | - **制約 post-close-correction で分離する理由**: reverse/delta 行（ADR-004）の会計への追送は、訂正承認の 2 段階（50 万円）・`affected_batch_code`・締め解除との排他と絡み、DAILY の出力規則とは判定時点も冪等キーも異なる（訂正依頼 1 件 1 本）。 |
| 締め後訂正（reverse/delta・2 段階承認） | #21 `ACC-Q` 確認事項（accounting-integration）— 5 件 | 確認項目 #21（ACC-13） が 締め後訂正（reverse/delta・2 段階承認） の前提（回答で金額・資格・締めの扱いが変わる）。項目単位で回答を追跡するため確認 Issue 内でも制約ラベルを付ける。 |
| 締め後訂正（reverse/delta・2 段階承認） | #28 `AUC-04` API せり結果行（AUC_CREATE_AUCTION_RESULT, AUC_UPDA… | - post-close-correction: セッション確定後の修正は業務日 OPEN 中のみ直接（履歴付き・第 2 承認なし）、業務日締め後は訂正依頼（reverse/delta、50 万円以上は 2 段階承認）へ回す。同じ PATCH が「確定前の自由修正」「確定後の統制修正」「締め解除モード」の 3 モードを持つため、経路分離を本 issue で明示する（GAP-#24（AUC-02））。 |
| 締め後訂正（reverse/delta・2 段階承認） | #36 `AUC-07` 画面 SCR-026 せり結果照会 | - post-close-correction: 業務日 OPEN なら直接修正（履歴付き）、CLOSED なら ㉙ 訂正依頼へ、締め解除モードは影響レコード行のみ。3 経路を画面で正しく出し分ける必要があるため独立 issue。 |
| 締め後訂正（reverse/delta・2 段階承認） | #82 `MIG-09` 切替・ロールバック手順（MIG-04 / 10-04）: freeze 前日 10:00・… | `post-close-correction` で分離する理由: 稼働後の移行誤りは reverse/delta の訂正経路（2 段階承認 50 万円）に乗せる唯一の手段であり、移行チームが業務表を直接 UPDATE する誘惑を手順で禁止する必要がある。 |
| 締め後訂正（reverse/delta・2 段階承認） | #105 `DLV-10` 画面 SCR-032 引渡し⇔精算追跡 | post-close-correction: 訂正は元行を書き換えず reverse/delta 行で積む（ADR-004）前提の表示で、訂正行の業務日は反映業務日（D35）。自動再計算（引渡し例外）が既存精算行に反映されない（AS-292）ことを画面で説明する必要があり、未確認（SCR-032 Q3、#116（DLV-26））。 |
| 締め後訂正（reverse/delta・2 段階承認） | #259 `TRD-03` 業務ロジック TRD_TRADE_CANCEL_RESTORE（取引取消とロット数量復元・… | - post-close-correction: 締め前は本 TECH で取消＋復元、締め後は訂正依頼（reverse/delta、ADR-004）のみという二経路を厳密に分け、例外は承認済み締め解除ウィンドウ内の影響レコードだけ（E-STL-010／E-STL-038）。訂正経路と混ぜないために独立 issue にする。 |
| 締め後訂正（reverse/delta・2 段階承認） | #269 `TRD-08` 画面 SCR-021 取引詳細 | - post-close-correction: 締め後の訂正は元の `trade`・`trade_line` を書き換えず `settlement_daily` の差額行で表す（ADR-004）。本画面は元値と承認済み差額を並べ、承認待ち・却下は合算しない。訂正経路（STL）の契約に依存するため独立 issue。 |
| 締め後訂正（reverse/delta・2 段階承認） | #276 `TRD-13` 受入テスト（特殊）取消復元・締め解除モード・締め後 reverse/delta の整合 | - post-close-correction: 「取消（締め前）」と「訂正（締め後、reverse/delta）」が同じ取引に対して排他的に適用されることを検証する専用テスト。 |
| 締め後訂正（reverse/delta・2 段階承認） | #277 `TRD-Q` 確認事項（negotiated-trade）— 4 件 | 確認項目 #277（TRD-14） が 締め後訂正（reverse/delta・2 段階承認） の前提（回答で金額・資格・締めの扱いが変わる）。項目単位で回答を追跡するため確認 Issue 内でも制約ラベルを付ける。 |
| 締め後訂正（reverse/delta・2 段階承認） | #324 `RPT-09` API ロック後調整・紛争帳票 RPT-08／09（RPT_LIST_POST_LOCK_… | - **制約 post-close-correction で分離する理由**: #323（RPT-08） は reverse/delta 行・締め解除・解除中修正（ADR-004、Q16「#323（RPT-08） に直接反映」）の完全性が監査性要件で、STL の訂正承認・締め解除 TECH と同じテストデータで検証する必要がある。#324（RPT-09） は紛争解決の訂正金額を #323（RPT-08） に委ねる対になる帳票。 |
| 締め後訂正（reverse/delta・2 段階承認） | #347 `RPT-29` 帳票金額整合テスト（RPT-05 ↔ RPT-06 ↔ 会計 batch・RPT-10 ↔… | - **制約 post-close-correction で分離する理由**: 整合が崩れる唯一の経路が reverse/delta 行（元行不変・反映業務日・SUPPLEMENT）で、訂正承認の 2 段階と締め解除の seed を STL と共有して検証するため。 |
| 締め後訂正（reverse/delta・2 段階承認） | #354 `STL-02` DB マイグレーション SETTLEMENT_DB（settlement_daily・co… | post-close-correction として分離する理由: 「元行を書き換えない」「承認段数は DB が毎回再計算する」「差額行は 1 回だけ」という統制を DB 層で閉じる必要があり、API 側の実装と独立に検証可能にするため。AS-039（しきい値は 1 依頼の差額）・AS-270（繰越反映）・AS-433（規則 14 のロール判定時点）を前提。`next_number('dispute')` は COMMON_DB への追… |
| 締め後訂正（reverse/delta・2 段階承認） | #364 `STL-05` 業務ロジック STL_CORRECTION_APPROVAL（承認・却下・apply_co… | post-close-correction として分離する理由: 締め後の金額変更はこの 1 経路だけであり、2 段承認・別人 3 名・1 回反映の統制が会計・奨励金に連鎖するため、単独で RED→GREEN を取る。AS-039・AS-157・AS-270・AS-433 を前提。SCR-039 A2 の「BE-owned」は DB＋BE に読み替える（GAP-#379（STL-11））。 |
| 締め後訂正（reverse/delta・2 段階承認） | #379 `STL-11` API 訂正依頼 起票 (STL_LIST_CORRECTION_TARGETS, STL… | post-close-correction として分離する理由: 起票は元行に触れず、証憑必須・段数自動決定・会計出力済でも止めない、という訂正経路の入口規則を API 契約として固定する。AS-153〜155・AS-357・AS-358 が前提。しきい値の判定単位・分割回避は未決（GAP-#353（STL-01））。 |
| 締め後訂正（reverse/delta・2 段階承認） | #380 `STL-12` API 訂正依頼 一覧・承認 (STL_LIST_CORRECTIONS, STL_GET… | post-close-correction として分離する理由: maker≠checker・2 段目の個人権限・反映プレビューは承認 API の契約そのもので、画面を迂回した直呼びでも同じ結果を返すことを API テストで保証する。SCR-039 E18（E-COM-007）は v1 では発生しない（GAP-#389（STL-21））。 |
| 締め後訂正（reverse/delta・2 段階承認） | #383 `STL-15` API 紛争 照会・添付 (STL_LIST_DISPUTES, STL_GET_DISP… | post-close-correction として分離する理由: 紛争 SLA（3／5 営業日、高額 3 営業日）は締め後の差異処理の統制で、#324（RPT-09） と同じ判定式を共有する。担当者ロール・既定表示は未決（GAP-#358（STL-03）・06）。 |
| 締め後訂正（reverse/delta・2 段階承認） | #384 `STL-16` API 紛争 操作 (STL_CREATE_DISPUTE, STL_UPDATE_DIS… | post-close-correction として分離する理由: 解決と終了の分離・訂正依頼との連動（CORRECTED／承認待ちあり）は締め後訂正の統制と一体。AS-237〜239 が前提。自動 ESCALATED の是非は未決（GAP-#367（STL-06））。 |
| 締め後訂正（reverse/delta・2 段階承認） | #385 `STL-17` バッチ 紛争 SLA 判定（自動エスカレーション・解決期限超過の Critical 通知） | post-close-correction として分離する理由: SLA 超過を誰にも気づかれずに流さないための自動処理で、画面・API のどれにも属さない。TECH 文書が無く job_code も ADR-014 に無い（GAP-#381（STL-13））。 |
| 締め後訂正（reverse/delta・2 段階承認） | #389 `STL-21` 画面 SCR-037 訂正依頼起票 | post-close-correction として分離する理由: 起票画面は「元行は変わらない」「証憑必須」「段数は自動」を利用者に明示する入口。AS-153〜155・AS-357 前提。分割起票の回避と返品の締め前扱いは未決（GAP-#353（STL-01））。 |
| 締め後訂正（reverse/delta・2 段階承認） | #393 `STL-22` 画面 SCR-038 訂正依頼一覧 | post-close-correction として分離する理由: 承認段階の導出表示（1/2 済・業務オーナー待ち）が 2 段統制の可視化そのもの。AS-156 前提。起票者閲覧・SCR-009 との分担は未決（GAP-#358（STL-03））。 |
| 締め後訂正（reverse/delta・2 段階承認） | #394 `STL-23` 画面 SCR-039 訂正依頼承認 | post-close-correction として分離する理由: 承認画面は 2 段承認・別人 3 名・1 回反映を人に見せ、CHECK 違反を 500 でなくコード付きで表示する（DP-05）唯一の面。AS-157・AS-158・AS-270 前提。照合部門長の代行者は未決（GAP-#358（STL-03））。 |
| 締め後訂正（reverse/delta・2 段階承認） | #399 `STL-25` 画面 SCR-041 紛争一覧 | post-close-correction として分離する理由: SLA 区分の判定式は #324（RPT-09） と共有し、締め後差異の統制指標そのもの。AS-237・AS-239 前提。既定表示・担当者ロールは未決（GAP-#367（STL-06）・03）。 |
| 締め後訂正（reverse/delta・2 段階承認） | #400 `STL-26` 画面 SCR-042 紛争詳細 | post-close-correction として分離する理由: 紛争の解決は訂正依頼（reverse／delta）に接続し、承認待ちが残る間は終了できない統制を画面で見せる。AS-237〜239 前提。CLOSED 権限・解決者≠終了者・自動 ESCALATED は未決（GAP-#358（STL-03）・06）。 |
| 締め後訂正（reverse/delta・2 段階承認） | #406 `STL-29` 受入テスト 締め後訂正の統制（maker≠checker 直呼び・バイパス悪用・強制 2 … | post-close-correction として分離する理由: 承認 UI が壊れていても DB 層が正しく動く（逆も）状態が実際に起きたため、UI を通さない検証を独立に持つ。 |
| 締め後訂正（reverse/delta・2 段階承認） | #408 `STL-Q` 確認事項（settlement-and-correction）— 10 件 | 確認項目 #408（STL-31）, #408（STL-33）, #408（STL-36） が 締め後訂正（reverse/delta・2 段階承認） の前提（回答で金額・資格・締めの扱いが変わる）。項目単位で回答を追跡するため確認 Issue 内でも制約ラベルを付ける。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #5 `ACC-01` DB マイグレーション ACCOUNTING_DB（acc_export_batch・ac… | - **制約 business-day で分離する理由**: 行の存在条件（業務日 CLOSED・ウィンドウなし）と `accounting_exported_at` による締め解除不可が業務日ライフサイクル（PF-01）の状態機械を直接拘束するため、BIZDAY_DB の変更と同じ sprint で扱う。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #6 `ACC-02` 業務ロジック ACC_EXPORT_ACK（DAILY 出力・SFTP 送信・ACK 回収… | - **制約 business-day で分離する理由**: DAILY の起票契機は業務日の締め、起票可否は CLOSED・ウィンドウなし、ACK_OK で締め解除不可に転じるなど、処理の前提条件と結果が業務日の状態遷移そのもの。締め解除 TECH（STL）と `business_day` の `for update` 順序を合わせて同時期に実装する。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #17 `ACC-05` API 会計連携操作（ACC_RESEND_EXPORT_BATCH, ACC_CREAT… | - **制約 business-day で分離する理由**: 再出力の可否は業務日が締め済みかつ締め解除ウィンドウが開いていないこと（E-ACC-001）に依存し、手動 ACK は業務日を締め解除不可へ転じさせる。照会 API（#16（ACC-04））と分け、STL の締め解除 API と同じ sprint で結合する。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #18 `ACC-06` 画面 SCR-059 会計連携状況 | - **制約 business-day で分離する理由**: 画面は業務日の締め状態（締め前・締め済み・締め解除中・会計出力済）を軸に操作可否が変わり、SCR-036／040（STL）との整合確認を同じ sprint で行う。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #20 `ACC-09` 会計 IF 結合テスト（/test/ 検証・実結合 2 回・PF-08 全遷移・11:00… | - **制約 business-day で分離する理由**: 検証は締め・締め解除・翌営業日オープンの実時刻に沿って行う必要があり、PF-01 の運用演習と同じ時間割で組む。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #23 `AUC-01` DB migration AUCTION_DB（auction_session / auc… | - business-day: 1 業務日 1 セッション（UNIQUE）、OPEN 業務日でのみ作成・入力・確定、締め済みは訂正依頼のみ。業務日の状態がセッション状態機械の前提になるため DB 単位で独立 issue。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #27 `AUC-03` API せりセッション（AUC_CREATE_AUCTION_SESSION, AUC_L… | - business-day: 作成条件は「OPEN 業務日あり」「当日未作成」「オンライン」の 3 つで、時間帯 02:30〜05:00 は目安。業務日のオープン遅延・臨時開場も同じ扱い（AS-220、#41（AUC-12））。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #35 `AUC-06` 画面 SCR-025 せりセッション一覧 | - business-day: OPEN 業務日の有無で作成ボタンと ③ の表示が切り替わり、休市日・未オープン日は作成不可。作成時刻制限（Q1）・2 年度前照会（Q2）は #41（AUC-12）。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #55 `XC-01` DB 共通テーブル COMMON_DB（audit_log・rule_config・mar… | `business-day` で分離する理由: `rule_config` は壁時計ではなく**対象行の業務日**で版を解決し（AS-056）、`market_calendar` は締め解除 3 営業日・Q19 繰下げ・SLA 営業日計算の唯一の正本であるため、他 feature のトリガーが Sprint 1 で参照できる状態にする。GAP-#59（XC-05）（E-COM-006 と E-COM-017 の重複）、GAP-#62（… |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #60 `XC-06` 監査コンテキスト・トランザクション基盤 withAudit()（set_audit_con… | `business-day` で分離する理由: トリガー先頭の `business_day for share` と全書込みのロック順序は締め後遮断（BR-CLOSE-01）の前提であり、各 feature が同じヘルパーを使わないとデッドロックが再発する（NEW-H1）。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #62 `XC-08` 業務日・会計年度・hot/cold 判定の共通ユーティリティ（rule_value 呼出し… | `business-day` で分離する理由: 業務日は暦日ではなく `business_day.biz_date` を軸にし、`created_at::date` を使わない（ADR-006 決定 1）。この規則を破る実装が 1 箇所でもあると奨励金期・会計出力・hot/cold 境界がずれるため、共通ユーティリティ以外からの日付判定を禁止する。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #67 `XC-13` E2E テスト基盤（Playwright・ロール別ログインフィクスチャ・業務日 OPEN/… | `business-day` で分離する理由: E2E は「OPEN は常に 1 件」制約の下で並列実行できないため、業務日フィクスチャで直列化・後片付け（締め）を保証する必要がある。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #74 `MIG-04` 移行ツール共通基盤（Fargate 一回限りタスク・読込・規則エンジン R-1〜R-8・r… | `business-day` で分離する理由: 移行でも `assert_business_day_open` を外さず（M-2）、OPEN は常に 1 件のため日次ループの直列化と失敗時の CLOSED 復帰が必要。GAP-#80（MIG-07）（移行年度に有効な `rule_config` 版が無い）は着手前に解消必須。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #79 `MIG-06` Wave 2 ロード: FY2026 business_day（全日 CLOSED）・lo… | `business-day` で分離する理由: 全日を OPEN → ロード → CLOSED で処理し、ロード中は OPEN が存在しない M-7 の制約（当日 10:00 ロック後の窓）を守る。GAP-#81（MIG-08）（FY2025 取引を参照する FY2026 受渡の複合 FK）。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #80 `MIG-07` Wave 3 ロード: FY2022〜25 全明細（3 世代）・FY2021 相対明細＋せ… | `business-day` で分離する理由: 過去 7 年分の `business_day` を生成しつつ、稼働中の OPEN 業務日（当日）と競合しないよう DB 変更窓 11:00〜01:00 内でのみ実行する。GAP-#73（MIG-03）（奨励金は移行しない、初月期の「次期差額」）。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #85 `DLV-01` DB マイグレーション DELIVERY_DB（delivery・delivery_exc… | business-day: 引渡し行の書込み遮断は**引渡しの業務日**（AS-073）、例外の締め前/後判定は**取引の業務日**（AS-223）で判定軸が 2 つあるため、トリガー単位で業務日列の意味を明記し単独 issue にする。`delivery_exception_split_limit_settle` は完納累計（C5）と精算へ影響するため BR-#167（INC-01） 側のテスト（#113（DLV-18））でも検証す… |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #86 `DLV-02` 業務ロジック DLV_DELIVERY_RECORD（分割 5 回・累計上限・未完了 1 … | business-day: 記録は OPEN 業務日のみ・OPEN は常に 1 件（ADR-006）・締め解除モードでは解除日に書く、という 3 通りの業務日決定を持つため単独 issue。按分方式は DELIVERY_DB T3（closed、AS-278/292）に従う — SCR-028 A7・TECH §4.4 No.2 の「T3 open」表記は古い（GAP-#103（DLV-08））。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #93 `DLV-04` 業務ロジック DLV_DELIVERY_EXCEPTION_RECALC（例外起票・締め前… | business-day: 「記録できるか」は引渡し業務日（OPEN）、「再計算するか」は取引業務日（OPEN/CLOSED）、「精算をどの日に計上するか」は起票業務日か解決時の OPEN 日（AS-466）— 3 つの業務日判断が 1 サービスに集まるため単独 issue。締め後の不足等の訂正依頼必須は DB CHECK でなく API 判定（R2-16）なので API テストで担保する。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #97 `DLV-05` 画面 SCR-027 引渡しボード | business-day: 既定 OPEN・締め済み日は参照のみ・OPEN なしのとき直近の締め済み日、の 3 状態を UI が持つ。自動更新なし（A6）は SCR-027 Q2 で未確認（GAP-#99（DLV-07）、前提採用）。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #98 `DLV-06` 画面 SCR-028 引渡し記録入力 | business-day: 記録は OPEN 業務日（引渡し日）、取引業務日は別でよい（AS-073）、締め解除モードでは解除日 — 画面が 2 つの業務日を併記する。SCR-028 A4 の「契約上限 CHECK 1..5」は DB の P5 R2-03（`seq >= 1`）より古い記述（GAP-#104（DLV-09））。AS-145（未完了 1 回）は運用未確認（#116（DLV-21））。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #103 `DLV-08` 画面 SCR-030 引渡し例外入力 | business-day: 画面が「例外を記録する業務日（OPEN）」と「取引の業務日（締め前/後の判定軸）」を同時に扱い、締め解除モードでは窓内を締め前扱いにする。締め後・返品は post-close-correction（PF-06）へ渡すだけで本画面は金額を動かさない。AS-225（締め前不足の起票者本人による自動解決）は FR-DEL-03「例外確認者」との整合が未確認（#116（DLV-23））。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #104 `DLV-09` 画面 SCR-031 滞留引渡し一覧 | business-day: OPEN 業務日内の時間しきい値と、締め済み業務日基準の営業日数（休市日を数えない AS-104）の 2 軸。しきい値 60 分と「最後の動き」の定義は未確認（AS-228、#116（DLV-25））。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #107 `DLV-12` API 引渡し記録・ボード（DLV_LIST_DELIVERIES, DLV_LIST_D… | business-day: 一覧は引渡し業務日で抽出（AS-073、DL-07）、候補は業務日を問わない（AS-144）、書込みは OPEN 業務日のみ、という 3 つの業務日ルールを API ごとに切り分けるため。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #109 `DLV-14` API 引渡し例外（DLV_GET_DELIVERY_EXCEPTION_CONTEXT,… | business-day: コンテキスト API が「取引業務日の状態（OPEN / CLOSED）」と「OPEN 業務日の有無」を両方返し、FE の処理区分表示の正になる。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #111 `DLV-16` API 照会系（DLV_LIST_STALE_DELIVERIES, DLV_LIST_Q… | business-day: 滞留の「当日」は OPEN 業務日、「持ち越し」は締め済み業務日と締め時刻、窓口の「当日」は OPEN 業務日に記録した引渡し — 画面ごとに業務日の意味が異なるため API 側に定義を集約する。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #114 `DLV-19` 連携 引渡しのオフライン業務キー・同期契約（{trade.code}#{seq} / #{… | business-day: 同期では「現在の OPEN 業務日」ではなく「入力時点の業務日」で書く唯一の経路。SCR-027 のオフライン状態変更（UPDATE）は PF-09 の遷移表に明示がなく AS-436 に依存。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #216 `INF-04` コンピュート: ECS Fargate app × 2（2 AZ、×3 へ水平拡張）・ba… | `business-day` で分離する理由: 日次枠は「業務日ロック（10:00）後〜11:00」で、ロックが遅れた場合も 11:00 期限は変えない（ADR-014）。Scheduler は壁時計、ジョブ内の判定は業務日である点をタスク定義の環境変数と手順に明記する。batch worker を常駐サービスにするか Scheduled Task にするかの記述揺れ（GAP-#214（INF-02））は常駐で確定。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #231 `LOT-01` DB migration LOT_DB（item_master / lot / lot_a… | - business-day: `lot`・`lot_appraisal` の書込みは `assert_business_day_open()` で OPEN 業務日に縛られ、締め後は訂正経路のみ。業務日 TECH（STL）の GUC 契約に依存するため独立 issue とする。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #232 `LOT-02` DB migration LOT_PART2_DB（lot_adjustment） | - business-day: 調整行の業務日は OPEN 業務日（`business_day_id`）で、ロットの業務日と異なり得る。締め解除モードでは解除日で記録する（SCR-016 A10）ため、STL の GUC 契約に合わせて `lot_adjustment_day_open` を実装する。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #233 `LOT-03` API ロット（LOT_CREATE_LOT, LOT_LIST_LOTS, LOT_GE… | - business-day: 受付・公開とも OPEN 業務日にのみ書込み、締め済みは E-STL-010 で訂正依頼へ誘導する。cold 年度の一覧は同期で返さず SCR-049 へ誘導（ADR-013 D61）。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #234 `LOT-04` API 目利き・調整（LOT_CREATE_LOT_APPRAISAL, LOT_CREA… | - business-day: 調整は OPEN 業務日にのみ記録。締め解除モード（SCR-040 入口）だけが CLOSED 日への書込みを許し、業務日＝解除日・理由に申請 ID を付す。別 feature の TECH と契約を揃える必要があるため独立 issue。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #238 `LOT-08` 業務ロジック LOT_OFFLINE_CODE_RESERVATION（番号帯予約・同期時… | - business-day: 予約は OPEN 業務日スコープのみ。業務日が変わると端末は旧帯を破棄し未使用は欠番（AS-057）。offline-continuity との統合ポイントであるため TECH 単位で独立させる。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #241 `LOT-09` 画面 SCR-012 ロット受付 | - business-day: OPEN 業務日が無ければ入力欄を出さず E-STL-031、入力中の締めは E-STL-010。業務日の表示・判定は STL API に依存。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #242 `LOT-10` 画面 SCR-013 ロット一覧 | - business-day: 既定業務日と「締め済みは読取専用」の予告表示が業務日状態に依存。全期間検索の可否（Q1）は #250（LOT-21）。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #243 `LOT-11` 画面 SCR-014 ロット詳細 | - business-day: 締め済み業務日のロットは ⑮⑯㉑ 非表示、ただし証憑の追加・取り下げだけは締め後も可（AS-075）という例外を持つ。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #244 `LOT-12` 画面 SCR-015 目利き結果入力 | - business-day: 締め済み業務日は記録不可（⑫ 表示）。ロール範囲（Q1）・再評価回数（Q2）は #250（LOT-18） / #250（LOT-23）。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #245 `LOT-13` 画面 SCR-016 ロット属性調整 | - business-day: 通常は OPEN 業務日のみ、締め解除モードでは解除した業務日として記録しバナー（申請 ID・残り時間）を出す。入口が別 feature（SCR-040）のため独立 issue とし、STL との契約（URL パラメータ・GUC）を先に固定する。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #249 `LOT-17` 受入テスト（特殊）オフライン継続・番号帯予約・再送競合の結合 | - business-day: 業務日の切替・締めが帯破棄と DAY_CLOSED_AFTER_CAPTURE の契機。30 分バッファ（AS-043）と失効後再送（AS-080）は顧客確認待ちのため、値変更に備えてパラメータ化しておく。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #250 `LOT-Q` 確認事項（lot-and-item-master）— 6 件 | 確認項目 #250（LOT-20） が 業務日・締め（OPEN 1 件・休市日・締め解除） の前提（回答で金額・資格・締めの扱いが変わる）。項目単位で回答を追跡するため確認 Issue 内でも制約ラベルを付ける。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #272 `TRD-09` 画面 SCR-022 取引取消 | - business-day: 取引の業務日が OPEN のときだけ取消でき、締め済みは E-STL-010 で訂正依頼へ、OPEN 業務日なしは E-STL-031。締め解除モードでは解除日として記録する。業務日状態で画面全体が切り替わるため独立 issue。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #293 `OFF-02` 業務ロジック OFF_OFFLINE_SYNC（受領・冪等判定・業務行適用・競合解決） | business-day: 再送は「入力時点の `business_day_id`」で書き、その日が CLOSED なら競合にする唯一の経路（付け替えはしない）。締め解除ウィンドウ中の APPLY_CLIENT は STL 側の GUC 契約に依存。`APPLY_AS_ADJUSTMENT` で作る `delivery_exception` の `exception_kind` は SPEC に明示がない（GAP-#298（OFF-0… |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #299 `OFF-05` 画面 SCR-034 同期競合処理 | business-day: `DAY_CLOSED_AFTER_CAPTURE` の「端末側を適用」は締め解除ウィンドウ中のみ可で、`unlock_request.unlock_until` を画面に出す。可否表 AS-232・監査主体 AS-233 は未確認（#304（OFF-11））。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #300 `OFF-06` API 同期受領（OFF_CREATE_SYNC_RECEIPT, OFF_LIST_SY… | business-day: 一覧は OPEN 業務日（無ければ直近）のみ、受領は入力時点の業務日で適用。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #301 `OFF-07` API 同期競合（OFF_LIST_SYNC_CONFLICTS, OFF_GET_SYN… | business-day: 詳細 API が締め解除ウィンドウの残り時間と対象レコードの該当有無を返し、FE の案内 ⑱ の正になる。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #309 `OPS-05` ジョブ実行枠組み（batch_job_run 状態遷移・並走禁止・締切監視・遅延アラート … | - **制約 business-day で分離する理由**: 枠の開始は業務日ロック（OPEN 1 件・10:00 ロック）、締切は業務日時点の `rule_config`、休市日の扱いと翌 02:00 オープンへの警告まで業務日ライフサイクル（PF-01）に直結するため、帳票ジョブの中身と分けて先に固める。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #313 `OPS-09` 日次バッチ枠・遅延アラート演習（11:00 証跡・3 段アラート・worker 障害・再実… | - **制約 business-day で分離する理由**: 検証の軸が業務日ロック時刻・締切・休市日・翌日オープンにあり、業務日ライフサイクル（PF-01）の E2E と一緒に走らせる必要があるため。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #320 `RPT-05` 帳票 CSV 共通基盤と API（RPT_EXPORT_REPORT_CSV, RPT_G… | - **制約 business-day で分離する理由**: 確定 CSV の可否は業務日の締め（CLOSED）で決まり、帳票ごとに適用の有無が異なる表（AS-180／185／253）を本 issue が一元管理する。締め状態の正は STL の `business_day` で、休市日は 404 ではなく「業務日ではない」空状態。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #322 `RPT-07` API 照合・会計帳票 RPT-05／06（RPT_GET_DAILY_SETTLEMEN… | - **制約 business-day で分離する理由**: #320（RPT-05） は締め後の公式記録で締め前は暫定、#321（RPT-06） は締め前を表示もしない（AS-180）。見出しの確認者・備考は締め・締め解除の記録そのもので、PF-01 の状態と同期して検証する。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #328 `RPT-13` 帳票バッチ（DAILY_REPORT 事前生成・MONTHLY_REPORT 確定 CSV） | - **制約 business-day で分離する理由**: 起動契機は業務日ロック、生成可否は CLOSED、休市日スキップ、月次は翌月最初の開場日と、全て業務日カレンダーで決まる。帳票 API（同期照会）とは別に、#313（OPS-09） の枠演習と同じ sprint で検証する。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #334 `RPT-19` 画面 SCR-051 RPT-05 日次照合表 | - **制約 business-day で分離する理由**: 画面の意味が「締め後の公式記録」で、締め前・締め解除中・会計出力済の各状態で見出し（確認者・備考）と CSV 可否が変わる。SCR-035／036（STL）と同じ seed で状態ごとに確認する。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #353 `STL-01` DB マイグレーション BIZDAY_DB（business_day・unlock_req… | business-day として分離する理由: 「OPEN は常に 1 件」「締め後は遮断」「締め解除は状態を変えずウィンドウで表す」という不変条件が全 feature の書込みトリガーの前提になるため、他 DB より先に単独で確定・検証する。AS-083（休市日は占位行）、AS-084（120 分）、AS-234〜236 を前提にする。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #358 `STL-03` 業務ロジック STL_BUSINESS_DAY_OPEN（02:00 自動オープン・遅延オ… | business-day として分離する理由: 業務日オープンは全業務入力の前提で、Sprint 1 の「なし」ではロット受付・取引が一切動かないため、他ロジックより先に単独で完了させる。AS-159（当日固定・常に MANUAL_LATE）、AS-275（再試行）、AS-083（占位行）が前提。市場カレンダーの保守画面は無い（GAP-#361（STL-04））。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #361 `STL-04` 業務ロジック STL_BUSINESS_DAY_LOCK（締めプレビュー・ロック 1 トラ… | business-day として分離する理由: 締めはグローバルなロック順の先頭 `business_day for update` を取る唯一の「葉」処理で、以後の全書込み遮断の起点になる。AS-109（OPEN→CONFIRMED）、AS-152（件数一致をサーバは検査しない）が前提。未完了引渡し・未解決紛争でロックを止めるかは未決（GAP-#374（STL-08））。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #367 `STL-06` 業務ロジック STL_BUSINESS_DAY_UNLOCK（締め解除の申請・承認・却下・… | business-day として分離する理由: 締め解除は「OPEN 1 件」を崩さずに締め済み日へ書く唯一の例外で、3 営業日・業務オーナー承認・会計 ACK との直列化を独立に検証する必要がある。AS-084・AS-234・AS-235・AS-236・AS-283・AS-284 が前提。ウィンドウ強制終了の通知種別は NOTIFICATION_DB に無い（GAP-#377（STL-09））。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #371 `STL-07` 業務ロジック STL_UNLOCK_MODE_WRITE（締め解除モードの行単位バイパス・… | business-day として分離する理由: 締め済み日への書込みを「一覧の行だけ・ウィンドウ内だけ」に閉じ込める最終防衛線で、6 feature を横断するため 1 か所で契約を持つ。AS-293〜296 が前提。せり結果修正→生成取引明細の同期トリガーは AUCTION_DB に未定義で、`auction_result` 経路の結合テストは #28（AUC-04） の決定待ち（GAP-#378（STL-10））。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #377 `STL-09` API 業務日・日次照合 照会 (STL_GET_OPEN_BUSINESS_DAY, S… | business-day として分離する理由: OPEN 業務日の取得は全画面の入口で、「OPEN なし＝正常状態（締め後〜02:00）」の契約を 1 か所で固定する。AS-151・AS-150・AS-027・AS-355・AS-359 が前提。差異の定義は未決（GAP-#371（STL-07））。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #378 `STL-10` API 業務日 操作 (STL_OPEN_BUSINESS_DAY, STL_CANCEL… | business-day として分離する理由: 4 本すべてが `business_day` を `for update` で取る葉の処理で、ロック順序規約（ADR-006 決定 5）の遵守をまとめてレビューする。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #381 `STL-13` API 締め解除 照会 (STL_PREVIEW_BUSINESS_DAY_UNLOCK,… | business-day として分離する理由: 解除可否は 3 営業日・会計 ACK・ウィンドウ重複の事前判定で、確定判定（DB）と同じ式を共有する必要がある。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #382 `STL-14` API 締め解除 操作 (STL_CREATE_UNLOCK_REQUEST, STL_A… | business-day として分離する理由: 申請者≠承認者・業務オーナー個人権限・3 営業日・会計状態の再検査を API 直呼びでも同じ結果にするため。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #386 `STL-18` 画面 SCR-066 業務日オープン操作 | business-day として分離する理由: 「オープン中は 1 日だけ」「締め済みは再オープン不可」を利用者に見せる唯一の画面で、Sprint 1 の動作確認の入口になる。AS-159・AS-048 前提。市場カレンダー保守画面は無い（GAP-#361（STL-04））。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #387 `STL-19` 画面 SCR-036 業務日ロック操作 | business-day として分離する理由: 締めは正式数値の確定点で、プレビュー再取得の UX が誤締めを防ぐ最後の人の判断（CAP-HUMAN-01）。ロックを止める条件は未決（GAP-#374（STL-08））。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #398 `STL-24` 画面 SCR-040 締め解除申請 | business-day として分離する理由: 締め解除は OPEN 1 件を崩さない例外経路で、影響レコードの宣言と「一覧の行だけ書ける」導線をこの画面だけが持つ。AS-234〜236 前提。影響レコードの入力方法・120 分・3 営業日の起点は未決（GAP-#364（STL-05））。 |
| 業務日・締め（OPEN 1 件・休市日・締め解除） | #405 `STL-28` 受入テスト 業務日の不変条件・並行性（OPEN 1 件・取消競合・ロック順序・ウィンドウ期… | business-day として分離する理由: 画面の受入条件では再現できない競合をプロセス並行で検証する必要があり、プロトタイプで実際に破られた履歴（C4／C5／H2）がある。 |

## 4. 分解中に見つけた LAB-4 仕様の穴・矛盾

191 件。処理の内訳: 設計修正 25 件（PREMISE.md §1）、仮定 70 件（PREMISE.md §2）、確認 Issue 69 件（feature ごとの `確認事項` Issue）、保留 27 件（理由つき）。
「処理」列の #番号は GitHub Issue、C-／A- は PREMISE.md の行番号。

| ID | Spec | 穴・矛盾 | 処理 |
|---|---|---|---|
| GAP-ACC-01 | ACC_EXPORT_ACK_TECH §4.2 エラー表 vs ACC_RESEND_EXPORT_BATCH §4 エラー一覧 / S… | 手動再試行の対象を TECH は「`CREATED` でない → E-COM-009」（CREATED なら可）、API と SCR-059 は「送信失敗（CREATED かつ自動試行が上限到達）のみ」とする。自動再試行中に人が割り込めるかが食い違う。 | 設計修正 → PREMISE.md C-01 |
| GAP-ACC-02 | PF-08 遷移 7 vs ACC_EXPORT_ACK_TECH §4.3 エラー表 / SCR-059 A3 | 11:00 の締切超過判定を PF-08 は「`SENT`／`ACK_OK` にならない」、TECH と SCR-059 は「`ACK_OK` にならない」とする。SENT を合格とするかで E-RPT-003 の発火が変わる。 | 確認 Issue 起票 #21（ACC-Q）（GAP-#6（ACC-02） を確認項目に追加、D-16） |
| GAP-ACC-03 | ACC_EXPORT_ACK_TECH §4.1 出力「REPORT_DB.export_file」 vs REPORT_DB §4.2 … | 会計 CSV のメタデータを `export_file` にも書くかが矛盾。 | 設計修正 → PREMISE.md C-02 |
| GAP-ACC-04 | ACC_GET_CONNECTION_STATUS §2 / OPS_DB §4.1 metrics（AS-367） | 接続状態・鍵有効期限は監視ワーカー（#308（OPS-03））が書く `health_snapshot` に依存し、ACC 単独では表示できない。 | 仮定 → PREMISE.md A-01 |
| GAP-ACC-05 | SCR-052 A1「未送信プレビュー」 / ACC_EXPORT_ACK_TECH §4.1 No.2〜3 | #321（RPT-06） の未送信プレビューは DAILY と同じ抽出・集計を再実行するが、共有する関数の所在（ACC か RPT か）が決まっていない。 | 仮定 → PREMISE.md A-02 |
| GAP-ACC-06 | ACCOUNTING_DB §5 Q2・Q4 / TECH §5 Q2 / SCR-052 Q2 | batch code 書式と CSV 行粒度が会計ベンダー未確認。行粒度は CSV 生成・#321（RPT-06）・性能目標を変える。 | 確認 Issue 起票 #21（ACC-Q） |
| GAP-ACC-07 | SCR-059 Q2 / AS-044・AS-023 / 第 2 回 Q6 | 「会計出力済」の定義と `.ng` 後の扱いが顧客確認待ち。差し替えで締め解除不可の範囲と状態機械が変わる。 | 確認 Issue 起票 #21（ACC-Q） |
| GAP-ACC-08 | SCR-059 Q4 / AS-189 | 手動 ACK の記録項目で監査要件を満たすか、二者確認が要るか未確認。 | 確認 Issue 起票 #21（ACC-Q） |
| GAP-ACC-09 | SCR-059 Q5 / AS-188 | SUPPLEMENT の自動起票と会計側の追加ファイル受入が未確認。 | 確認 Issue 起票 #21（ACC-Q） |
| GAP-ACC-10 | ACC_EXPORT_ACK_TECH §4.6 No.2 / PF-08「承認を契機に worker が」 | 訂正承認（STL）から ACC worker への契機の渡し方（イベント・キュー・同期呼出し）と、保留 (b) を DAILY の ACK_OK 遷移時に再評価する仕組みが未定義。`ACC_EXPORT` ジョブは DAILY 用で SUPPLEMENT 用の job_code も無い。 | 設計修正 → PREMISE.md C-03 |
| GAP-ACC-11 | ACC_EXPORT_ACK_TECH §4.3 No.4「TIMEOUT は終端ではなく後継未起票の間はポーリングを続ける」 | 後継が起票されない TIMEOUT 行を何日ポーリングし続けるかの上限が無い（手動 ACK も再出力もされない行が永続的に残る）。 | 仮定 → PREMISE.md A-03 |
| GAP-ACC-12 | PF-08 遷移 6 E-code 列 | 新 batch 起票の遷移に E-ACC-005（同一 batch code の内容不一致）が書かれているが、E-ACC-005 は同一 batch の再送時のコード。起票時に出るのは E-ACC-009／E-ACC-001。 | 仮定 → PREMISE.md A-04 |
| GAP-ACC-13 | SCR-059 NFR「検証」 / REQ-002 Q24 | 実結合 2 回は会計ベンダーと発注者 IT の作業を伴い、日程が本プロジェクトの管理外。 | 保留: #20（ACC-09） の前提として PM が KO 直後に日程を確保。遅延時は /test/ モックで仮検収 |
| GAP-ACC-14 | ACCOUNTING_DB §4.1 列 3 vs BIZDAY_DB R3 | 「会計 batch がある業務日は締め解除不可」のトリガーを ACCOUNTING_DB と BIZDAY_DB のどちらが持つか（両方に記述）。二重実装や片方欠落の恐れ。 | 仮定 → PREMISE.md A-05 |
| GAP-AUC-01 | AUC_AUCTION_SESSION_CLOSE §4.2 No.2・§5 未決 / AUCTION_DB §4.2 トリガー注記（D4… | 行ロック順が ADR-006 では `business_day → trade → lot → auction_result`、AUCTION_DB・TECH では `business_day → auction_session → auction_result → trade → lot`。SCR-026 の修正（auction_result → trade → lot）と SCR-022 の… | 設計修正 → PREMISE.md C-04 |
| GAP-AUC-02 | AUC_UPDATE_AUCTION_RESULT_API / SCR-024 A4 / SCR-026 A2・A9 | 同一 PATCH が (a) セッション OPEN 中の自由修正（理由なし・履歴なし）、(b) CLOSED 後の統制修正（理由・version 必須・履歴・取引同期）、(c) 締め解除モード の 3 契約を持つ。SPEC は注記で触れるが request の必須項目がモードで変わることを API 契約として明示していない。 | 仮定 → PREMISE.md A-06 |
| GAP-AUC-03 | AUC_AUCTION_SESSION_CLOSE §4.4 No.2 / TRD_TRADE_CONFIRM §4.3 No.3（AS-… | 確定は有効行ごとに `next_number('trade', YYMMDD)` を呼び、採番行ロックはトランザクション終了まで保持される。120〜300 件の取引生成中（数秒〜）は同じ業務日の相対取引確定がすべて採番で待たされる。02:30〜05:00 は相対取引も動く時間帯で、性能目標（Q4）が未定。 | 保留: #25（AUC-02-a） で保持時間を計測し、#41（AUC-Q） で目標値とともに判断。対策案: 確定前に `reserve_number_block('trade', …)` で件数分を一括予約（欠番許容 AS-057）。 |
| GAP-AUC-04 | SCR-026 A4・E11 / AUCTION_DB `auction_result_sync_trade_line` | SCR-026 は「引渡し記録が 1 件でもある行は落札者・ロット・数量・単価の変更と無効化をすべて拒否（E-TRD-007）」とするが、DB の同期トリガーは `assert_trade_qty_not_below_delivered`（数量が累計引渡しを下回る変更のみ）と `assert_trade_cancel_allowed`（取消）しか持たず、単価のみの変更は DB では通る。API … | 設計修正 → PREMISE.md C-05 |
| GAP-AUC-05 | AUC_AUCTION_SESSION_CLOSE §4.4 No.6（AS-299） / AUCTION_DB `auction_res… | 生成取引の `created_by`・`confirmed_by` を確定者とするため、取引側の監査では入力者が見えず、せり結果側の `entered_by` を辿る必要がある。SCR-021 の変更履歴（取引＋明細）には入力者が現れない。 | 仮定 → PREMISE.md A-07 |
| GAP-AUC-06 | SCR-024 A3 / FORM-SERI-01「結果時刻」 | `result_at` は保存時刻を自動記録し入力させない。入力が結果より遅れた場合（確認者差戻し後の再入力など）に帳票の結果時刻が実際のせり時刻とずれるが、修正手段が履歴付き修正（SCR-026）にしか無く、`result_at` が修正対象列に含まれるかは history の before/after に含まれる以外に記載がない。 | 仮定 → PREMISE.md A-08 |
| GAP-AUC-07 | drift DL-11 / SCR-024 A3・NFR | LAB-1 構成ではせり候補を ElastiCache に置くが、SCR-024 は「画面表示時に取得した一覧で絞り込み、サーバ往復なし」としており、キャッシュ層の要否が SPEC 側で決まっていない。 | 仮定 → PREMISE.md A-09 |
| GAP-AUC-08 | SCR-025 項目 20 / AUC_LIST_AUCTION_SESSIONS_API | 一覧の修正件数は `auction_result_history` の件数集計で、1 日 1 セッション × 50 件表示でも history を結合する。性能上は軽微だが API 設計書の応答に修正件数が含まれるかを本 feature の SPEC からは確認できなかった（frontmatter のみ読取）。 | 仮定 → PREMISE.md A-10 |
| GAP-AUD-01 | AUD_LIST_ENTITY_AUDIT_LOGS frontmatter vs SCR-063 画面概要 | 変更履歴 API の呼出画面が API では SCR-018／021／029、SCR-063 本文では SCR-005／016／021／039 と食い違う。閲覧ロール（AS-397）の対象種別一覧も確定していない。 | 仮定 → PREMISE.md A-11 |
| GAP-AUD-02 | AUD_GET_AUDIT_LOG §4 エラー一覧 vs SCR-064 E8 / RPT_GET_REPORT_RUN | cold 1 件取得の失敗は API では HTTP 502（E-RPT-008）、帳票の cold 失敗は 200＋`data.error_code`。同じコードで HTTP の扱いが異なる。 | 仮定 → PREMISE.md A-12 |
| GAP-AUD-03 | AUDIT_DB §4.1 列 16 vs SCR-063 A5／SCR-064 A5／AUD_AUDIT_WRITE §4.2 No.8 | 移行行の判定を AUDIT_DB（P5）は `actor_role = 'ROLE-MIGRATION'`、SPEC と TECH は `reason` の `migration:` 接頭辞としている。 | 設計修正 → PREMISE.md C-06 |
| GAP-AUD-04 | SCR-063 A6 / AUDIT_DB §5 Q2 | FY2019〜20 に監査記録が無い前提は顧客確認待ち（AS-265）。回答次第で移行範囲と画面注記が変わる。 | 確認 Issue 起票 #53（AUD-Q） |
| GAP-AUD-05 | SCR-064 A1 / AUD_GET_AUDIT_LOG | cold 1 件取得は p95 ≤ 10 秒とあるが、何秒で打ち切って 502 にするかの閾値が無い。 | 仮定 → PREMISE.md A-13 |
| GAP-AUD-06 | SCR-063 A3 / AUDIT_DB 索引注記（D34） | cold 監査検索は REPORT_DB `report_run` と cold ランナー・通知ディスパッチャに依存する。監査を phase 1 に置くと、これらは phase 3 の reporting／notification 側にある。 | 設計修正 → PREMISE.md C-07 |
| GAP-AUD-07 | SCR-063 未決事項 Q1・Q2・Q4 | 内部監査ロールの要否、31 日超キー条件、CSV 出力なしが発注者未確認。 | 確認 Issue 起票 #53（AUD-Q） |
| GAP-AUD-08 | SCR-064 未決事項 Q1・Q2 | マスク対象の範囲（連絡先を含むか）と論理名辞書の持ち方が未決。 | 確認 Issue 起票 #53（AUD-Q） |
| GAP-AUD-09 | SCR-064 A3 | 論理名辞書の正本が無い（DB 設計書の論理名列から起こす想定だが生成手順が無い）。 | 仮定 → PREMISE.md A-14 |
| GAP-AUD-10 | nfr OBJ-03 / SCR-063 NFR 表「業務」行 | 完全な監査証跡を持つ取引の割合（≥ 98%）の測定方法が「帳票側」とだけあり、どの帳票・クエリで測るか定義が無い。 | 保留: #52（AUD-08） で測定クエリを定義し docs 化、帳票への組込みは RPT 側の判断 |
| GAP-AUD-11 | AUD_AUDIT_WRITE §4.2 No.1 / OPS_DB alert_event | `alert_event` は確認・クローズの UPDATE だけ監査するが、dedup による `detail.count` の増分（システム UPDATE）も同じ AFTER UPDATE トリガーに掛かり、GUC 未設定なら E-AUD-001 になる。 | 設計修正 → PREMISE.md C-08 |
| GAP-XC-01 | nfr.md §7 / integrations.md §1.1 | 社内セッションの絶対上限が nfr §7「アプリ側は 8 時間で再認証」と integrations §1.1「絶対上限 10 時間（AS-021）」で食い違う。 | 確認 Issue 起票 #69（XC-Q） |
| GAP-XC-02 | log-convention.md §2・§3 | ログ規約は ISO 様式の誤記（TRACE/INFO 説明）を含み、区切り・TZ・Category・禁止項目・保存・所属の 6 項目が未回答で「まだ標準として使用できない」。 | 確認 Issue 起票 #69（XC-Q） |
| GAP-XC-03 | integrations.md §1.2 / ADR-010 D48 / api-list.md 公開 API | ROLE-SYS-ADMIN 用 break-glass ローカル認証アカウント 1 件（AS-021）が定義されているが、それを使うログイン API・画面が api-list・SCR-001 SPEC に存在しない。 | 保留: identity-and-participants の IAM ログイン issue で API 追加要否を判断（#58（XC-04） は allowlist に穴を開けない） |
| GAP-XC-04 | nfr.md §9 / prototype package.json gate | nfr は `check-a11y.mjs` を CI で継続すると定めるが、継承元の `gate` スクリプトに `check:a11y` が含まれていない。 | 設計修正 → PREMISE.md C-09 |
| GAP-XC-05 | COMMON_DB §4.2 契約上限 / error-codes.md E-COM-017 | `rule_config_value_bounds` 違反を COMMON_DB は E-COM-006 と定めるが、error-codes には専用コード E-COM-017 `rule_config_exceeds_contract_ceiling` が別に存在し、api-conventions「領域固有コード優先」と矛盾する。 | 設計修正 → PREMISE.md C-10 |
| GAP-XC-06 | COMMON_DB §4.4 reserve_number_block / ADR-003 決定 1 | `reserve_number_block()` は `audit_log` へ直接 1 行書くが、ADR-003 は「`audit_log` の唯一の書き手は AFTER ROW トリガー」と定める。SECURITY DEFINER 関数内 INSERT の例外が明文化されていない。 | 仮定 → PREMISE.md A-15 |
| GAP-XC-07 | api-list.md §2 権限列 / IAM_DB role_permission | `role_permission(scope='API')` の seed（200 API × 8 ロール）をどの DB migration が投入するかが IAM_DB・COMMON_DB のどちらにも明記されていない。 | 仮定 → PREMISE.md A-16 |
| GAP-XC-08 | COMMON_DB §4.2 標準キー（effective_from = 稼働初日）/ data-migration.md §3 順序 | `rule_value(key, biz_date)` は版が無ければ raise するが、移行行（FY2019〜26）の業務日は稼働初日より前のため、`assert_trade_line_limit` 等のトリガーが W2/W3 ロード中に失敗する。移行用の版（または `producta_migration` 時の解決規則）が未定義。 | 設計修正 → PREMISE.md C-11 |
| GAP-XC-09 | nfr.md §9「14 トークン対」 | コントラスト検証の対象「14 トークン対」の一覧が仕様書に無く、プロトタイプのトークン定義が唯一の出所。 | 仮定 → PREMISE.md A-17 |
| GAP-MIG-01 | data-migration.md §2 / drift-vs-lab1 DL-12 | LAB-1 見積の「約 108 万行」は FY2021 相対明細 16 万行と FY2019〜20 の 900 行を含まず、設計の正本は約 1,240,000 行。見積側の数値と差分が残る。 | 仮定 → PREMISE.md A-18 |
| GAP-MIG-02 | data-migration.md §4 lot 行 / LOT_DB unique lot_code_key | `lot.code` は全期間一意だが、旧ロットコードが業務日をまたいで重複する場合の処理（採番し直し・サフィックス・reject）が未決で、件数も未計測。 | 確認 Issue 起票 #83（MIG-Q）（#71（MIG-01） の実測値を添える） |
| GAP-MIG-03 | data-migration.md §4「奨励金は移行しない」/ BR-INC-01 次期差額 | `incentive_result` を移行しないため、稼働初月期の完納奨励金で「次期差額」の前期実績が存在しない。初期条件の扱いが data-migration にも INCENTIVE_DB にも無い。 | 確認 Issue 起票 #83（MIG-Q） (4)。回答は incentive-and-rule-version feature の計算 issue へ連携 |
| GAP-MIG-04 | data-migration.md §3 W1（staging は切替 4 週間前、UAT 開始前）/ deployment.md §1 … | staging には W1 移行データと発注者提供のマスキング済み UAT データの 2 系統が記述され、UAT がどちらで走るか、W2 リハーサルと UAT 期間のデータ共存方法が未定義。 | 仮定 → PREMISE.md A-19 |
| GAP-MIG-05 | data-migration.md §5 migration.reject / COMMON_DB §4.7 台帳（49 表） | `migration` スキーマの表は削除禁止台帳に含まれず、保持期間・満了削除・`producta_app` からの可視性が未定義。reject には原行 JSON（個人データを含み得る）が入る。 | 保留: #72（MIG-02） で forbid_delete を付与し 7 年保持と仮置き、APPI 観点は #229（INF-Q） と合わせて確認 |
| GAP-MIG-06 | ADR-007 決定 6 / data-migration.md M-3 | 移行専用 `app_user` 行（`ROLE-MIGRATION`）は `provision_app_user()` で作れないと定められているが、代わりにどの経路で作るかが書かれていない。 | 仮定 → PREMISE.md A-20 |
| GAP-MIG-07 | COMMON_DB §4.2 標準キー（effective_from = 稼働初日）/ data-migration.md §3 順序・M… | 移行行の業務日（FY2019〜26）は `rule_config` 初期版の発効日より前のため、`rule_value()` が版無しで raise し、全トリガー有効のままのロード（M-2）が成立しない。 | 設計修正 → PREMISE.md C-12 |
| GAP-MIG-08 | data-migration.md §3 W2（FY2026 のみ）/ ADR-013 複合 FK (trade_id, trade_fi… | FY2026 の受渡・精算が FY2025 末（3 月）の取引を参照する場合、W2 時点で親行（FY2025、W3 対象）が無く複合 FK 違反になる。年度境界をまたぐ参照の W2 での扱いが未定義。 | 保留: #71（MIG-01） で件数を計測し、該当する FY2025 親行を W2 に先行投入するか reject するかを #73（MIG-03） で決める |
| GAP-MIG-09 | data-migration.md §9 SCR-057 / REPORT_DB batch_job_run | 移行ジョブの進捗・reject 件数・照合結果を SCR-057 に出すとあるが、`batch_job_run.job_code` に移行用の値が REPORT_DB で定義されているか未確認。 | 保留: #74（MIG-04） で `MIG_W1/W2/W3` を提案し reporting-and-print feature の DB issue で確認 |
| GAP-DLV-01 | SPEC-DLV-002 §ページレベル前提 A3 / §未決事項 Q1 | 未完了の回を 1 取引 1 つに制限（AS-145、E-DLV-011）するが、同時 2 台積込の運用可否が未回答。 | 確認 Issue 起票 #116（DLV-Q） |
| GAP-DLV-02 | SPEC-DLV-003 §未決事項 Q4 / DLV_DELIVERY_COMPLETION_CONFIRM_TECH §5 | 完納確定の取消経路がない（列は 1 回だけ書ける）。誤確定時に訂正依頼でどう戻すか、計算済み・確定済み期の奨励金をどう差額化するかが未定義。 | 確認 Issue 起票 #116（DLV-Q） |
| GAP-DLV-03 | SPEC-DLV-010 §ページレベル前提 A3 / §未決事項 Q3 | 締め前の不足・一部取消は確認者＝起票者本人で即 RESOLVED（AS-225）。FR-DEL-03 の「例外確認者」要件との整合が未確認。 | 確認 Issue 起票 #116（DLV-Q） |
| GAP-DLV-04 | SPEC-DLV-004 §未決事項 Q1〜Q4 / SPEC-DLV-002 Q3 / DELIVERY_DB §5 T2 | 1 操作印刷の対象（全回 or 未印刷）、「当日」の範囲、印刷ロール（ROLE-TRADE）、iPad 記録分の後追い印刷動線（第 2 回 Q7 未回答、AS-033）が未確定。 | 確認 Issue 起票 #116（DLV-Q） |
| GAP-DLV-05 | SPEC-DLV-011 §ページレベル前提 A2 / §未決事項 Q1 | 滞留しきい値 60 分（`delivery_stale_minutes`）と「最後の動き」の定義（AS-228）が未確認。 | 確認 Issue 起票 #116（DLV-Q） |
| GAP-DLV-06 | SPEC-DLV-002 §未決事項 Q2 / SPEC-DLV-012 §未決事項 Q3 | 部分精算の按分と、自動再計算を既存精算行に反映しない扱いが SPEC 側では open のまま（DB T3 は AS-278/292 で closed）。 | 確認 Issue 起票 #116（DLV-Q） |
| GAP-DLV-07 | SPEC-DLV-001 §ページレベル前提 A6 / §未決事項 Q2 | ボードを手動更新のみとする（A6）運用可否が未回答。SCR-031 の当日タブは 60 秒自動更新で、同じ利用者に 2 つの鮮度ポリシーがある。 | 仮定 → PREMISE.md A-21 |
| GAP-DLV-08 | SPEC-DLV-002 §ページレベル前提 A7 / DLV_DELIVERY_RECORD_TECH §4.4 No.2 | 「按分方法は DELIVERY_DB T3（open）」と記すが、DELIVERY_DB §5 T3 は P4 で closed（AS-278/292）。参照が古い。 | 仮定 → PREMISE.md A-22 |
| GAP-DLV-09 | SPEC-DLV-002 §ページレベル前提 A4 | 「契約上限 CHECK 1..5、引き上げ不可」と記すが、DELIVERY_DB P5 R2-03 で CHECK は `seq >= 1` に緩和され、上限は `rule_num('delivery_max_splits')` と `rule_config_value_bounds` が守る。 | 仮定 → PREMISE.md A-23 |
| GAP-DLV-10 | DELIVERY_DB §4.2 列 14 / DLV_DELIVERY_EXCEPTION_RECALC_TECH §4.6 | 締め後に起票した不足・過剰・一部取消の解決に訂正依頼が必要という規則は API 判定のみで、DB CHECK は RETURN だけ（R2-16）。API を迂回した UPDATE では守れない。 | 仮定 → PREMISE.md A-24 |
| GAP-DLV-11 | SPEC-DLV-001 §ページレベル前提 A5 / PF-09 §4 遷移 1 | ボードからのオフライン状態変更（`{trade.code}#{seq}#{status}`、`delivery_action=UPDATE`）は PF-09 の遷移表に明示がなく AS-436（API 設計）だけが契約。回の特定（`delivery_id` or `origin_client_op_id`）と `expected_status` の扱いは OFF 側実装に依存。 | 保留: #114（DLV-19） と #293（OFF-02） で契約テストを共有。PF-09 の追記は D-11 により spec-changes 候補。 |
| GAP-DLV-12 | DLV_DELIVERY_COMPLETION_CONFIRM_TECH §5 未決 / INC_INCENTIVE_CALC_TECH … | 完納確定時に奨励金の期が既に CLOSED の場合、本機能は判定しないとあるが、INC 側では完納日 > 支払期限は NOT_FULLY_DELIVERED で 0 円（AS-285、open Q3）。期 CLOSED 後の完納は実質「算入されない」だが、顧客合意がない。 | 確認 Issue 起票 #211（INC-Q）（incentive-and-rule-version 側で確認） |
| GAP-IAM-01 | ASSUMPTIONS AS-021 vs SPEC-IAM-001／010 対象外・ADR-010 | AS-021 は SYS-ADMIN 用 break-glass アカウント 1 件を置くとするが、SCR-001／002 は「Entra 障害時のローカルパスワード経路は設けない（裏口を作らない）」と明記し、SCR-002 は SYS-ADMIN も本画面から入れないとする。矛盾。 | 確認 Issue 起票 #165（IAM-Q）（影響: #122（IAM-03）／04／27） |
| GAP-IAM-02 | SPEC-IAM-001 A4 vs SPEC-IAM-011 E18 vs IAM_DB login_attempt | SCR-001 A4 は社内ロックの復旧を「SYS-ADMIN が SCR-005 で手動解除」とするが、SCR-005 E18 は社内アカウントのロック解除要求を E-COM-009（ロックは Entra 側）で拒否し、IAM_DB には社内用 locked_until 列が無く login_attempt 集計のみ。手動解除の手段が無い。 | 確認 Issue 起票 #165（IAM-Q）（影響: #124（IAM-05）／06-b／18） |
| GAP-IAM-03 | SPEC-IAM-010 Q2・IAM_CREATE_ACCOUNT_API AS-317・IAM_DB external_account | 社外アカウントは乱数ハッシュ＋must_change_password=true で発行されるが、パスワード設定・変更・再発行の画面と API が画面一覧・api-list に無い。社外 110 アカウントがログインできない。 | 確認 Issue 起票 #165（IAM-Q）（#123（IAM-04）・#144（IAM-15） が着手不能、FE 1 画面＋BE 2 API 程度の見積増） |
| GAP-IAM-04 | SPEC-IAM-010 Q4 vs IAM_DB §4.2 列 18 | SCR-002 Q4 は「IAM_DB に証明書の列が無い」と open のままだが、IAM_DB は P2 D15 で device_cert_thumbprint を追加済み（失効は NULL 化）。SPEC 側の TBD が未更新。 | 仮定 → PREMISE.md A-25 |
| GAP-IAM-05 | PARTY_DB §4.1 列 5・§5 T2 vs IAM_UPDATE_PARTY_API vs IAM_PARTY_STATUS_T… | 卸売業者・買出人の status は「直接編集」とあるが、更新 API は基本情報のみ、TECH は資格を持たない種別を E-IAM-023 で拒否。状態を変える経路が無い。SCR-007 Q2・SCR-008 Q3 も open。 | 確認 Issue 起票 #165（IAM-Q）（影響: #129（IAM-08-b）／13-a／21-b） |
| GAP-IAM-06 | SPEC-IAM-023 A1・Q1 vs CSV 画面一覧 vs BIZDAY_DB 索引設計 | 共用承認キューに締め解除を含めるかが出所間で一致しない（CSV は資格＋訂正のみ、BIZDAY_DB は共用前提）。 | 確認 Issue 起票 #165（IAM-Q）（影響: #134（IAM-11）／22、#354（STL-02） 依存） |
| GAP-IAM-07 | SPEC-IAM-024 Q2／Q3・SPEC-IAM-025 Q1／Q2・SPEC-IAM-002 Q3・TECH §5 Q2 | 申請中の自動失効（AS-209）、証跡なし承認の例外、30 日前通知の回数と本人通知、期限絞込み選択肢（AS-134）が発注者未確認。 | 確認 Issue 起票 #165（IAM-Q）（影響: #132（IAM-09-b）／11／13-c／23／24） |
| GAP-IAM-08 | SPEC-IAM-021 Q1／Q2・SPEC-IAM-011 Q2・SPEC-IAM-022 Q2・SPEC-IAM-003 Q4・IA… | 担当者交代時の付替主体（第 2 回 Q11 未回答）、長期未ログイン棚卸、ROLE-INTAKE の編集可否、業務オーナー個人付与方式、ロール権限変更の maker≠checker が未確定。 | 確認 Issue 起票 #165（IAM-Q）（影響: #125（IAM-06）／07／08-b／17／19／21） |
| GAP-IAM-09 | IAM_DB app_user.party_id FK ↔ PARTY_DB party.updated_by FK | 2 つの DB 設計書が相互に FK を持つ（循環）。1 DB 設計 = 1 migration の順序では適用できない。 | 仮定 → PREMISE.md A-26 |
| GAP-IAM-10 | IAM_DB §4.5 role_permission・AS-203／204 | 8 ロール × SCREEN／API の初期カタログ（seed）の一覧が spec に無い。AS-204 は固定権限のみ列挙。 | 仮定 → PREMISE.md A-27 |
| GAP-IAM-11 | IAM_DB §4.1 列 5（ROLE-MIGRATION）vs SPEC-IAM-022 A1・IAM_LIST_ROLES「8 ロー… | role_code は P5 で ROLE-MIGRATION を加え 9 値だが、SCR-006／IAM_LIST_ROLES は 8 ロール固定と記す。 | 仮定 → PREMISE.md A-28 |
| GAP-IAM-12 | IAM_PARTY_ELIGIBILITY_TECH・IAM_PARTY_STATUS_TRANSITION_TECH | 2 つの TECH にテストベクトル表が無く、エラー表と PF-02 遷移表のみ。 | 仮定 → PREMISE.md A-29 |
| GAP-IAM-13 | SPEC-IAM-022 Q3（固定権限の管理場所） | 固定権限（AS-204）をコード定数で持つか role_permission の列で持つか open。 | 仮定 → PREMISE.md A-30 |
| GAP-IAM-14 | IAM_PARTY_ELIGIBILITY_TECH §3 vs TRADE_DB／AUCTION_DB | トリガー trade_confirm_eligibility は TRADE_DB.trade に付くが TECH の feature は identity。所有者と migration の置き場所が曖昧。 | 仮定 → PREMISE.md A-31 |
| GAP-IAM-15 | PARTY_DB §5 T3（short_code の付与範囲） | short_code を買手 3 種別全員に付けるかせり参加者のみか open。SCR-008 ⑩ は任意入力 3〜4 文字で実装可能。 | 保留: AUC-（せり落札者入力）側で確定。#129（IAM-08-b） は NULL 許容で実装 |
| GAP-IAM-16 | SPEC-IAM-023 A2・IAM_LIST_APPROVAL_QUEUE_API | 確定後訂正・締め解除の行の閲覧範囲と状態語彙は settlement-and-correction の SPEC（SCR-038／039／040）に依存し、本 feature だけでは閉じない。 | 保留: #353（STL-01）／#354（STL-02） の確定後に #134（IAM-11）・#157（IAM-22） を結合、それまでは資格の行のみでテスト |
| GAP-INC-01 | INC_INCENTIVE_CALC_TECH §4.7 / §5 Q2 · STL_SETTLEMENT_TAX_TECH §4.6（参… | DS-INC-EDGE-01 の原本値（Appendix C）が設計の入力に無く、test vector の数値は設計者の仮置き（AS-286）。#6（ACC-02） の厳格合格基準が仮値のまま。 | 確認 Issue 起票 #211（INC-Q） |
| GAP-INC-02 | INC_INCENTIVE_CALC_TECH §4.3 No.3 / §5 Q3 · SPEC-INC-011 §未決事項 Q4 · D… | 期限後に完納した取引を不算入とする（AS-285）、期またぎ分割引渡しの対象期 = 取引の業務日（第 2 回 Q2 未回答）、完納確定時に期が CLOSED の場合の扱い（DLV 側は「判定しない」、INC 側は期限後 = 0 円）— 3 点が顧客合意なし。 | 確認 Issue 起票 #211（INC-Q） |
| GAP-INC-03 | SPEC-INC-011 §未決事項 Q1〜Q3 · INCENTIVE_PART2_DB §5 Q2 · AS-089 / 244 / … | 入金実績は会計からの取込 IF がなく手入力（月 ≈ 20,000 行）。一括取込の要否、計算済み期で自動再計算しないこと、期の確定の職務分離が未確認。 | 確認 Issue 起票 #211（INC-Q） |
| GAP-INC-04 | SPEC-INC-002 §未決事項 Q1 · SPEC-INC-003 Q1 · INCENTIVE_DB §5 Q1 · AS-010… | 年 4 回の事前検査タイミング（承認依頼時）、会計年度開始月 4 月（第 2 回 Q10 未回答）、発行前確定（RACI-01）の記録方法（列なし・監査理由のみ）が未確認。 | 確認 Issue 起票 #211（INC-Q） |
| GAP-INC-05 | SPEC-INC-010 §未決事項 Q1〜Q4 · INCENTIVE_PART2_DB §4.3 · AS-240 / 241 / 2… | 遡及の申請者 = 起票者可否、期中の期の上限見込み表示、却下後の再申請不可（UNIQUE）、次回業務日オープン発効（即時 ACTIVE 案 AS-287 は却下済み）が未確認。 | 確認 Issue 起票 #211（INC-Q） |
| GAP-INC-06 | SPEC-INC-002 §未決事項 Q3 · SPEC-INC-001 Q2 · AS-172 / 177 | 料率の入力精度（% 小数 4 桁）と 0% の許容、ROLE-SETTLEMENT・業務オーナーへの一覧閲覧の付与が未確認。 | 確認 Issue 起票 #211（INC-Q） |
| GAP-INC-07 | INC_RATE_VERSION_TECH §4.4 · INCENTIVE_DB §4.3 注記（ensure_open_incenti… | 発効処理と期の自動作成は業務日オープンのジョブ `BUSINESS_DAY_OPEN`（settlement-and-correction / SCR-066）の中で同一トランザクションとして呼ばれる。フックの所有（STL 側のジョブに INC の関数呼出しを追加する）が feature 間で未割当。 | 仮定 → PREMISE.md A-32 |
| GAP-INC-08 | SPEC-INC-001 §受入条件「発効を見送った遡及版」· SPEC-INC-003 E19 シナリオ · INC_RATE_VERS… | 「発効見送り」の表示は OPS_DB `alert_event`（`RETRO_RATE_ACTIVATION_DEFERRED` 未クローズ）を情報源とするが、INC_LIST_RATE_VERSIONS / INC_GET_RATE_VERSION がその情報を返す設計かは本分解では API 本文未確認。 | 保留: #202（INC-11） の実装時に API 設計書本文を確認し、無ければ応答に activation_deferred を追加（spec-changes 候補、D-11）。 |
| GAP-INC-09 | SPEC-INC-010 §ページアクセス制御 · IAM_DB role_permission（RETRO_RATE_APPROVE） | 遡及の例外承認はロールでなく個人権限の付与（SCR-005 / 006、AS-110 / 165）が前提。付与者が 0 名または申請者・起票者と同一人物のみの場合、遡及経路が閉塞するが運用上の担保が未定義。 | 保留: IAM 側の権限付与 issue（IAM-xx）への依存として記録。運用手順（最低 1 名の付与）は #211（INC-Q） の回答と合わせて PREMISE に記載。 |
| GAP-INF-01 | deployment.md §2 参照コスト / ADR-009「結果」 | 参照コストは AWS Pricing Calculator 未検証で S3 単価が実勢の約 6 倍と判明済み。Glacier Flexible Retrieval・外部メール配信・RDS バックアップ超過分・RDS Proxy・Secrets Manager が未計上。 | 仮定 → PREMISE.md A-33 |
| GAP-INF-02 | deployment.md §2.1 batch worker 行 / ADR-014「決定」実行基盤 | deployment は「10:00〜11:00 枠外はアイドル。Scheduled Task 化は P4 以降に判断」とし、ADR-014 は「ECS Fargate worker サービス（常駐）を EventBridge Scheduler がトリガー」とする。常駐サービスか Scheduled Task かが二重記述。 | 仮定 → PREMISE.md A-34 |
| GAP-INF-03 | deployment.md §7 検証行 / prototype scripts/check-login.mjs | 本番デプロイ後の検証は「demo アカウントなしで実行できる read-only smoke のみ」とするが、その smoke の対象 API・合否基準が定義されていない（`check-login.mjs` は Supabase 専用で置換対象）。 | 仮定 → PREMISE.md A-35 |
| GAP-INF-04 | deployment.md §1 / ADR-009「決定」 | IaC ツール（Terraform／CDK）、IaC リポジトリの所在、環境差分の管理方式が仕様に無い。 | 仮定 → PREMISE.md A-36 |
| GAP-INF-05 | nfr.md §10 AS-016（Route 53 Health Check は AWS 複数リージョンから発信）/ ADR-009「決… | 外形監視のチェッカーが国外から `/healthz` を叩く構成と「監視目的を含めてリージョン外へコピーしない」原則の整合が、nfr の注記（個人データを含まない）だけで担保されている。発注者 Q1 の解釈として明示確認が無い。 | 仮定 → PREMISE.md A-37 |
| GAP-INF-06 | integrations.md §2.1（モック ACK ライターは入札者構築）/ §2.3 テスト（/test/ は発注者 SFTP） | モック ACK ライターが発注者 SFTP の `/ack/` に書く必要があるが、入札者がそこへ書き込む経路・権限が無い。入札者側に staging 用 SFTP を別に立てるのか、発注者 SFTP 上で動かすのかが未定義。 | 確認 Issue 起票 #229（INF-Q） |
| GAP-INF-07 | deployment.md §5 producta_purge 行 / ADR-013 手順 2 | `producta_purge` のシークレットを本システムの Secrets Manager に置かず発注者情シスが保管するが、ロール作成・パスワード初期発行・再発行（実行のたび）を誰がどの環境で行うかが書かれていない。 | 確認 Issue 起票 #229（INF-Q） |
| GAP-INF-08 | nfr.md §9 / deployment.md §7 | 負荷試験の実施環境は staging（本番同等）とあるが、staging が single-AZ・Fargate ×1 のため本番（×2、Multi-AZ）と性能特性が異なり、p95 の検収値を本番へ外挿する方法が未定義。 | 仮定 → PREMISE.md A-38 |
| GAP-LOT-01 | LOT_DB §3 / PF-03 遷移 4・6・7 / TRD_TRADE_CONFIRM §4.5 No.3 | PUBLISHED→CONFIRMED（残数量 0）・CONFIRMED→DELIVERING（初回引渡し）・DELIVERING→COMPLETED（全取引完納）は「トリガーで自動」とあるが、どのトリガー（trade_line_lot_consumption の AFTER か、lot_adjustment_apply か、delivery 側か）が UPDATE を発行するか未定義。TRD … | 設計修正 → PREMISE.md C-13 |
| GAP-LOT-02 | LOT_DB §3 状態機械 / PF-03 遷移 7 | COMPLETED の条件が LOT_DB は「qty_available = 0 かつ全取引完納」、PF-03 は「全取引が完納」のみ。売れ残り（残 > 0）ロットの全取引が完納したときの終端状態が食い違う。 | 仮定 → PREMISE.md A-39 |
| GAP-LOT-03 | SCR-012 A2 / TRD_TRADE_CONFIRM §4.6 No.3 | ロット受付は `Idempotency-Key` で 5 秒タイムアウト再試行を冪等化するが、同じ現場で使う取引確定（TRD_CREATE_TRADE）は冪等キーを持たない。再試行方針が画面間で不統一。 | 確認 Issue 起票 #277（TRD-Q）。LOT 側は SPEC どおり実装。影響: #233（LOT-03）・#256（TRD-02） |
| GAP-LOT-04 | LOT_DB §4.1 トリガー item_master_guard / SCR-018 E14 | 品目コード変更の拒否コードが LOT_DB では E-COM-009、SCR-018 では E-LOT-013 `item_code_immutable`。 | 設計修正 → PREMISE.md C-14 |
| GAP-LOT-05 | LOT_DB §4.3 トリガー注記 / SCR-014 A1 / PF-03 遷移 2 | 初回目利きでの RECEIVED→INSPECTED を LOT_DB は「app が進める」と記し、SCR-014 は「遷移は DB が強制」と記す。書き手（BE サービス）と検証（トリガー）の分担が明文化されていない。 | 仮定 → PREMISE.md A-40 |
| GAP-LOT-06 | SCR-016 A3 / LOT_DB §4.2 CHECK | 調整後残数量の上限「入荷数量 − 販売済み」は BE 判定のみで、DB の CHECK は `qty_initial` 上限しか持たない。API 直呼びで販売済みを超える増加が DB では止まらない。 | 仮定 → PREMISE.md A-41 |
| GAP-LOT-07 | SCR-013 項目 18 / LOT_LIST_LOTS_API | ロット一覧の販売先数は TRADE_DB（trade・trade_line）結合が必要で、LOT の API が TRD の migration に依存する。README §5 は「数量引当は negotiated-trade 側」と記すのみで一覧 API の依存を明示していない。 | 仮定 → PREMISE.md A-42 |
| GAP-LOT-08 | SCR-014 A2 / COMMON_DB attachment | 締め済み業務日・完了ロットでも証憑の追加・取り下げを許す（AS-075）が、共通 `attachment` 表に業務日トリガーが掛かるかどうかは COMMON_DB の記述に依存し、本 feature の SPEC からは確認できない。 | 保留: #55（XC-01）/#56（XC-02） の担当に「attachment は day_open 対象外」であることを確認。違う場合は締め後添付の経路（行単位バイパス）が別途必要。 |
| GAP-LOT-09 | LOT_OFFLINE_CODE_RESERVATION §4.4 No.2 | 同期時の予約範囲検査の正本が `audit_log` の `after_state` JSON（専用表なし）。1 日 14 台 × 複数回の予約を JSON 条件で検索する設計で、索引・保持期間（audit_log は 7 年）の観点が未記載。 | 保留: #239（LOT-08-a） で実行計画を確認し、必要なら `lot_code_reservation` 専用表を spec-changes/ に提案。 |
| GAP-LOT-10 | SCR-012 A6 / ASSUMPTIONS AS-043・AS-080 | 30 分バッファと失効後再送の前提が顧客確認待ちのまま。値が変わると SCR-012/015 の E8/E4 と #249（LOT-17） のテストが変わる。 | 保留: offline-continuity 側の clarify に相乗り（OFF の clarify key を orchestrator が紐づけ）。LOT 側は `rule_config.offline_queue_buffer_minutes` を読むだけにしておく。 |
| GAP-TRD-01 | TRD_TRADE_CONFIRM §4.5 No.3 / LOT_DB §3 / PF-03 遷移 4 | 取引確定でロットが PUBLISHED→CONFIRMED に「自動遷移する」（LOT_DB・PF-03）と「TECH はロット状態を遷移させない（LOT の責務）」が併記され、残数量 0 到達時に UPDATE を発行する主体が未定義。 | 設計修正 → PREMISE.md C-15 |
| GAP-TRD-02 | TRD_TRADE_CONFIRM §4.6 No.3 / SCR-019 NFR / SCR-012 A6 | 確定 API は冪等キーを持たず「同じ内容を 2 回送れば 2 件」。同じ現場端末のロット受付は 5 秒無応答で `Idempotency-Key` 再試行する設計で、応答喪失時の再送方針が画面間で異なる。二重取引はロット数量を二重に減らす。 | 確認 Issue 起票 #277（TRD-Q）。影響: #257（TRD-02-a）・#266（TRD-06-b） |
| GAP-TRD-03 | SCR-019 A10 / TRD_TRADE_CONFIRM §4.2 No.3 / STL_BUSINESS_DAY_LOCK §4.3 | 締め解除モードの再入力で「作れる取引は 1 件だけ」「同じウィンドウ内で SCR-022 により取り消された取引に限る」の判定は GUC `app.unlock_reentry_trade_id` と BIZDAY_DB §4.2 手順 5 に委ねられ、本 feature の TECH には判定ロジックが無い。STL 側の実装が無ければ E-STL-038 を返せない。 | 保留: #367（STL-06）/#371（STL-07）/#382（STL-14）（STL_BUSINESS_DAY_LOCK/UNLOCK）の担当と GUC 名・判定責務を確認。#257（TRD-02-a） は GUC 設定のみ。 |
| GAP-TRD-04 | SCR-022 E11 / TRD_TRADE_CANCEL_RESTORE §4.4 | 復元後の残数量が入荷数量を超えるデータ不整合を E-COM-010（concurrent_update_conflict）で返す。利用者には「競合」と見えるが実体は整合性エラーで、再試行しても解消しない。 | 仮定 → PREMISE.md A-43 |
| GAP-TRD-05 | SCR-023 データ・API マッピング / TRD_GET_LOT_SALES_API | 分割販売状況は `delivery`（DELIVERY_DB）と `rule_config.delivery_max_splits` を参照し、SCR-021 も引渡し集計を出す。negotiated-trade の API が delivery feature の表に依存するが README §5 は「引渡しは delivery」と範囲外にするのみ。 | 仮定 → PREMISE.md A-44 |
| GAP-TRD-06 | TRADE_DB §4.1 `trade_day_open` 例外（P2 D4） / ADR-004 | 完納列限定バイパス（GUC `app.delivery_completion_trade_id`）は TRADE_DB に書かれているが、設定する関数 `confirm_trade_delivery_completion()` は DELIVERY_DB 側。TRADE_DB の migration テストが DLV の関数なしでは完結しない。 | 仮定 → PREMISE.md A-45 |
| GAP-TRD-07 | TRADE_DB enum `trade_status` / PF-04 §3 / drift DL-10 | enum は 7 値だが使用は 3 値。`SUBMITTED/PENDING/APPROVED/REJECTED` を「予約」とする一方、TRADE_DB T1 と SCR-019 Q3 は確認段階の要否を open のまま。回答が「設ける」なら enum だけでなく SCR-019/021・TECH が大きく変わる。 | 確認 Issue 起票 #277（TRD-Q）。影響: #254（TRD-01-b）・#256（TRD-02）・#264（TRD-06） |
| GAP-TRD-08 | SCR-020 データ・API マッピング | 取引一覧は IAM_LIST_PARTY_CANDIDATES・RPT_GET_REPORT_RUN・notification を使い、cold 検索の起票先 `report_run` は REPORT_DB。TRD_CREATE_ARCHIVE_SEARCH の応答（受付番号）と `report_run` の状態遷移の契約が本 feature 側に無い。 | 保留: #329（RPT-14） の担当と `report_run` の kind・状態・結果格納の契約を確認してから #262（TRD-04） を着手。 |
| GAP-TRD-09 | SCR-021 A4 / AUD_LIST_ENTITY_AUDIT_LOGS_API | 変更履歴は取引と明細行（複数 id）の監査行を時系列で統合して 20 件表示するが、AUD の API は `/{entity_type}/{entity_id}` の単一エンティティ指定。複数 id の統合取得をどちらが行うか未定義。 | 仮定 → PREMISE.md A-46 |
| GAP-NTF-01 | notification README §3 / integrations §3 / AS-034 | ディスパッチャ・メール送信ワーカー・webhook の TECH が無く、再試行間隔（通常 1→5→15 分、Critical 1→2 分）は AS-034 の記述だけ。処理詳細は DB 設計・SPEC・integrations に分散。 | 仮定 → PREMISE.md A-47 |
| GAP-NTF-02 | NOTIFICATION_DB §4.1 概要 FUNC-181 / 各発生元 SPEC | 発生元 feature がイベントをどう渡すか（同一トランザクションの同期呼出し・outbox・DB トリガー）が定義されていない。 | 仮定 → PREMISE.md A-48 |
| GAP-NTF-03 | AS-246 本文 vs NOTIFICATION_DB §4.1 列 2・SCR-061 A3 | AS-246 は Critical 3 種、DB と SCR-061 は `OPS_ALERT_CRITICAL` を加えた 4 種（AS-425）。 | 仮定 → PREMISE.md A-49 |
| GAP-NTF-04 | SCR-061 A8 vs NOTIFICATION_DB §4.2 初期データ | 受信者固定で seed を作らない種別が SCR-061 A8 では 2 種（UNLOCK_REQUESTED・COLD_QUERY_DONE）、DB では 3 種（＋OPS_ALERT_CRITICAL）。 | 設計修正 → PREMISE.md C-16 |
| GAP-NTF-05 | SCR-061 A5 extra_threshold digest_max_items | 日次まとめの最大件数を超えた通知の扱い（翌日送り・切捨て・分割）が定義されていない。 | 保留: 仮置き: 超過分は件数のみ本文に記載し通知センターへ誘導（#280（NTF-02））。SCR-061 の次版で確定 |
| GAP-NTF-06 | SCR-060 A4 / SCR-002 | Critical の全画面バナーは外部参加者（独自認証シェル）にも出す必要があるが、外部側の共通レイアウトに組み込む記述が無い。 | 仮定 → PREMISE.md A-50 |
| GAP-NTF-07 | integrations §3「日次の突合で補正」 vs REPORT_DB §4.3 job_code CHECK | webhook 取りこぼしの日次突合ジョブに対応する `job_code` が CHECK（10 値）に無い。 | 設計修正 → PREMISE.md C-17 |
| GAP-NTF-08 | ADR-014 日次ジョブ 5「通知送信」 vs FR-NOTIFY-02 Critical 5 分 | ADR-014 は通知送信を日次枠のジョブとして書くが、Critical は発生から 5 分以内に送る必要があり常時稼働の送信ループが要る。 | 仮定 → PREMISE.md A-51 |
| GAP-NTF-09 | SCR-060 Q2 / SCR-061 Q3 / AS-248 | 外部参加者を受信者に含めることと宛先メールの同意が未確認（APPI）。 | 確認 Issue 起票 #290（NTF-Q） |
| GAP-NTF-10 | SCR-061 Q1 / NOTIFICATION_DB §5 Q1 / AS-098 | 業務しきい値を画面から変えたいという要望があれば SCR-061 の範囲が変わる。 | 確認 Issue 起票 #290（NTF-Q） |
| GAP-NTF-11 | SCR-062 Q1・Q2 / AS-249・AS-099 | 手動再送条件と 3 年超ログの照会経路が未確認。 | 確認 Issue 起票 #290（NTF-Q） |
| GAP-NTF-12 | SCR-060 A6・SCR-062 A6「3 年で cold」 vs NOTIFICATION_DB（パーティション記述なし）・DP-1… | 通知と送信ログの「cold」が何を指すか（物理移動は無い、D61）が DB 設計に無い。年度パーティションの対象でもない。 | 仮定 → PREMISE.md A-52 |
| GAP-NTF-13 | SCR-060 画面概要「紛争 SLA 超過・滞留引渡し」 / batch_job_run job_code DISPUTE_SLA | 紛争 SLA・滞留引渡しの判定ジョブ（発生元）はどの feature が持つか明示されていない（通知 README は発生元 feature、settlement／delivery README の確認が必要）。 | 保留: #385（STL-17）（紛争 SLA バッチ）は起票済み。DELIVERY_STALLED の判定ジョブは #111（DLV-16） の照会系に含まれるか統合時に確認 |
| GAP-OFF-01 | SPEC-OFF-001 §未決事項 Q1/Q2 · SPEC-OFF-002 Q4 · OFF_OFFLINE_SYNC_TECH §5… | 第 2 回 Q4（未同期時のログアウト可否・実行主体）/ Q5（オフライン中のセッション失効）が未回答。D-05 / AS-080 / AS-289 の前提で設計。 | 確認 Issue 起票 #304（OFF-Q） |
| GAP-OFF-02 | SPEC-OFF-002 §ページレベル前提 A2/A5 · §未決事項 Q1/Q2 | 競合種別 × 判断可否表（AS-232）と、判断で書く業務行の監査 actor = 判断者（AS-233）が未確認。PF-09 の「実行主体は入力者」とは自動同期のときだけ一致。 | 確認 Issue 起票 #304（OFF-Q） |
| GAP-OFF-03 | SPEC-OFF-001 §未決事項 Q4/Q5 · OFFLINE_DB §5 Q3 | 全端末閲覧（AS-230）、20 分注意（AS-231）、受領の保持 13 か月（AS-081）、および第 2 回 Q14（オフライン削減時の代替運用）が未回答。M05B は削減候補。 | 確認 Issue 起票 #304（OFF-Q） |
| GAP-OFF-04 | SPEC-OFF-002 §ページレベル前提 A2 可否表 · OFF_OFFLINE_SYNC_TECH §4.5 No.2 | 「例外・調整として記録」で作る `delivery_exception` の `exception_kind`（SHORTAGE / EXCESS / QTY_MISMATCH のどれか、対象の回・明細行の指定）と `lot_adjustment` の理由区分が SPEC・TECH に明示されていない。 | 設計修正 → PREMISE.md C-18 |
| GAP-OFF-05 | SPEC-OFF-001 §ページレベル前提 A4 / §業務フロー | 再送順を「`captured_at` 昇順」と記すが、TECH §4.2 No.2（P5、AS-438）は端末キューの登録順で `captured_at`（端末時計）に依存しないとする。 | 仮定 → PREMISE.md A-53 |
| GAP-OFF-06 | SPEC-OFF-001 §ページレベル前提 A5 · AS-289 | ログアウト抑止は FE のみで、`IAM_REVOKE_SESSION` はキューや未解決競合を検査しない。API 直呼び・ブラウザ終了では抑止できず、「未同期があればログアウト不可」は UI 上の制御に留まる。 | 仮定 → PREMISE.md A-54 |
| GAP-OFF-07 | OFF_CREATE_SYNC_RECEIPT_API frontmatter（screen_id に SCR-012 / SCR-015… | ロット側の enqueue（SCR-012 / 015）、予約番号帯（LOT_OFFLINE_CODE_RESERVATION）、`#A{n}` の採番は lot-and-item-master の文書に依存し、本 feature だけでは端末キューの 3 業務のうち 2 業務が完結しない。 | 保留: #233（LOT-03） / #234（LOT-04）（ロット受付・目利きサービス）/ LOT 側 FE issue との契約を #297（OFF-03） の enqueue API で共有。orchestrator が LOT 側 issue キーを突合。 |
| GAP-OPS-01 | ADR-014 / REPORT_DB §4.3 / 各 feature README | 日次バッチ worker と `batch_job_run` のジョブ枠組みは全 feature が使うが、TECH も feature 帰属も無い（ADR-014 と REPORT_DB の表定義のみ）。`batch_job_run` の DDL は REPORT_DB にあり、帳票は phase 3 だが枠組みは phase 1 で要る。 | 設計修正 → PREMISE.md C-19 |
| GAP-OPS-02 | SCR-065 A1・A2 / OPS_DB §5 Q3 | ヘルスチェック 1 分・取得遅延 3 分・自動更新 60 秒を `rule_config` 標準キーにするか未決（AS-266）。 | 確認 Issue 起票 #314（OPS-Q） |
| GAP-OPS-03 | OPS_DB §5 Q1 | `health_snapshot` は日 1 万行だが保持期間が未定（案 13 か月）。満了削除はアプリ外のため索引肥大の見積が必要。 | 確認 Issue 起票 #314（OPS-Q） |
| GAP-OPS-04 | OPS_DB §4.1 列 7 metrics.maintenance／declared_disaster / OPS_GET_MAINT… | 保守通知中・災害宣言中のフラグを運用担当が立てる手段（画面・API・CLI）が定義されていない。保守案内の予定時刻も同様。 | 保留: #308（OPS-03） で運用 CLI（または rule_config キー）を仮実装し、運用手順書で確定。画面化は見積外 |
| GAP-OPS-05 | OPS_DB §4.2 dedup_key 注記 / alert_event_audit トリガー | 未クローズの同一 `dedup_key` は `detail.count` を増やす（システムの UPDATE）が、`alert_event_audit` は AFTER UPDATE 全般に掛かるため監査コンテキストが要り、設計上「INSERT はシステム発行で監査しない」意図と噛み合わない。 | 設計修正 → PREMISE.md C-20 |
| GAP-OPS-06 | SCR-065 P2・P3 / AS-268 | ROLE-SETTLEMENT の閲覧範囲と、ロールを持たない業務オーナー（UNLOCK_APPROVE 個人付与）への見せ方が未確認。Critical 通知 `OPS_ALERT_CRITICAL` は SYS-ADMIN 固定。 | 確認 Issue 起票 #314（OPS-Q） |
| GAP-OPS-07 | SCR-065 A7 / AS-269 | 未認証で返す保守案内の情報範囲が未確認。 | 確認 Issue 起票 #314（OPS-Q） |
| GAP-OPS-08 | ADR-014 遅延アラート表 vs SCR-057 A2／REPORT_DB §4.3 列 11 | 11:00 超過の検知を ADR-014 は CloudWatch アラーム、SCR-057／REPORT_DB は監視が `is_deadline_missed` を立てるとする。worker 自体が停止した場合の検知主体が曖昧。 | 仮定 → PREMISE.md A-55 |
| GAP-OPS-09 | SCR-065 A3 / NFR-AVL-01 | 稼働率の参考値は `health_snapshot` の APP 行 OK 比率、正式値は外形監視（1 分間隔・連続 2 回失敗、AS-016）。外形監視と月次報告の仕組みが本 epic にも infra にも起票されていない。 | 保留: infra-nfr epic（XC）で外形監視・月次可用性報告を起票するよう申し送り |
| GAP-OPS-10 | SCR-065 Q4 / AS-012 | 「宣言された災害」の定義は顧客確認待ち（契約時確定）。 | 確認 Issue 起票 #314（OPS-Q） |
| GAP-OPS-11 | ADR-014 / NOTIFICATION_DB / ACCOUNTING_DB | 通知送信（Critical 5 分以内）、ACK ポーリング（1 分間隔）、印刷ジョブの 60 秒 TIMEOUT 判定は日次枠外でも常時動く処理だが、ADR-014 は日次枠ジョブしか定義しない。常駐ループの置き場所が未定義。 | 仮定 → PREMISE.md A-56 |
| GAP-RPT-01 | reporting-and-print README §3「技術設計書なし」 | 日次・月次帳票バッチ、CSV 共通基盤、cold ランナー、印刷エージェントの処理詳細に TECH が無く、ADR-014・REPORT_DB・各 SPEC・API の記述から組み立てる必要がある。 | 仮定 → PREMISE.md A-57 |
| GAP-RPT-02 | SCR-048 A1「カタログ定義（RPT-01〜12）」 / REPORT_DB | 帳票カタログ（コード・名称・頻度・フィルタ軸・既定ロール可否）を持つ表が無い。 | 仮定 → PREMISE.md A-58 |
| GAP-RPT-03 | REPORT_DB 冒頭 Note「実行記録は業務日の会計年度でパーティション」 vs §4 表定義（PK id 単独）・DP-19（対象… | `report_run` 等をパーティションするかが文書内で矛盾。 | 設計修正 → PREMISE.md C-21 |
| GAP-RPT-04 | ADR-014 冪等性「report_run.version を +1」 vs REPORT_DB §4.1 | `report_run` に `version` 列が無い。版は新しい `batch_code` 行で表す設計。 | 仮定 → PREMISE.md A-59 |
| GAP-RPT-05 | ADR-014 日次ジョブ 4「PDF/CSV を S3」・容量「PDF 生成」 vs 回答 Q21・SCR-048 対象外・SCR-05… | ADR-014 は帳票 PDF 生成を前提に容量を見積るが、SPEC は 12 帳票を画面＋CSV のみ（RPT の印刷はブラウザ印刷）とする。 | 設計修正 → PREMISE.md C-22 |
| GAP-RPT-06 | SCR-051 A1「業務日の全行（引渡し完了ごとの行＋CORRECTION 行）」 vs ACCOUNTING_DB 抽出対象（D35:… | #320（RPT-05） が `settlement_daily.business_day_id` で集計すると、他日の訂正が反映日の #320（RPT-05） に、当日の訂正が反映日側に出て、#321（RPT-06）（元業務日で割当）と合計が一致しない。SCR-051 受入条件「#321（RPT-06） と合計が一致する」を満たせない。 | 確認 Issue 起票 #351（RPT-Q）（GAP-#321（RPT-06） を確認項目に追加、D-16） |
| GAP-RPT-07 | SCR-058 A3・integrations §4「印刷エージェントの技術設計が正」 | 参照先の印刷エージェント技術設計が specs に存在しない。エージェントを誰が作り誰が配布するかも README に無い（情報システム部門は IP 設定のみ）。 | 設計修正 → PREMISE.md C-23 |
| GAP-RPT-08 | SCR-058 A7 ブラウザ印刷 / RPT_CREATE_PRINT_JOB（printer_id 必須、print_mode=BRO… | ブラウザ印刷モードでも `print_job.printer_id` は NOT NULL だが、何を入れるか未定義。 | 仮定 → PREMISE.md A-60 |
| GAP-RPT-09 | SCR-058 Q1 / 第 2 回 Q7 / AS-033 | iPad で記録した引渡しの後追い印刷の運用が顧客確認待ち。否なら ⑤〜⑦ と RPT_LIST_PRINT_TARGETS の必要性が変わる。 | 確認 Issue 起票 #351（RPT-Q） |
| GAP-RPT-10 | SCR-051 Q2 / DL-13 | SCR-051 → SCR-058 の印刷遷移は画面一覧 CSV に無い追加導線。 | 確認 Issue 起票 #351（RPT-Q） |
| GAP-RPT-11 | SCR-048 Q1・SCR-054 Q3・SCR-055 Q4 / AS-183・AS-251 | 帳票別のロール可否が発注者未確認。 | 確認 Issue 起票 #351（RPT-Q） |
| GAP-RPT-12 | SCR-048 Q2・Q3 / REPORT_DB Q2・Q3 | 31 日上限・メタデータ末尾列・batch code 系列・保持 7 年が未確認。 | 確認 Issue 起票 #351（RPT-Q） |
| GAP-RPT-13 | SCR-049 Q1・Q2 | #316（RPT-01） 集計軸と #317（RPT-02） の属性調整内容が未確認。 | 確認 Issue 起票 #351（RPT-Q） |
| GAP-RPT-14 | SCR-050 Q1・Q2 / SCR-051 Q1 / AS-186 | 滞留・差異件数の定義、#318（RPT-03） の過去基準日が未確認。 | 確認 Issue 起票 #351（RPT-Q） |
| GAP-RPT-15 | SCR-052 Q1 / SCR-053 Q1〜Q3 / AS-187・AS-185 / 第 2 回 Q2 | 原本表示方式、#322（RPT-07） の毎日の解釈、期またぎの対象期、#323（RPT-08） の却下掲載が未確認。 | 確認 Issue 起票 #351（RPT-Q） |
| GAP-RPT-16 | SCR-054 Q1・Q2 / SCR-055 Q1〜Q3 / AS-250・AS-027・AS-252・AS-253 | コホート集計・営業日計算、FY2019〜20 の集計レベル表示（顧客確認待ち）、FY2021 せり積み上げ、暫定 CSV が未確認。 | 確認 Issue 起票 #351（RPT-Q） |
| GAP-RPT-17 | SCR-056 Q1〜Q3 / AS-254 | #327（RPT-12） の対象範囲・変更都度・事象範囲が未確認。 | 確認 Issue 起票 #351（RPT-Q） |
| GAP-RPT-18 | SCR-057 Q1〜Q3 / AS-048・AS-255 | 3 段アラートの通知先、再実行権限、遅延版の区別が未確認。 | 確認 Issue 起票 #351（RPT-Q） |
| GAP-RPT-19 | REPORT_DB §4.2 列 9 storage_tier COLD / RPT_GET_EXPORT_FILE E-COM-022「… | CSV ファイルの cold（2 年超）が S3 のどの階層か、署名付き URL を即時に出せるか（Glacier なら復元待ちが要る）が曖昧。添付（3 年で Glacier）と同じ扱いか不明。 | 仮定 → PREMISE.md A-61 |
| GAP-RPT-20 | API 設計書 §2.1 の注記（RPT_GET_DAILY_TRADE_SUMMARY・RPT_LIST_PARTICIPANT_VAL… | api-list の権限列と各 API 設計書（SPEC の P 表を正とした）が食い違ったまま。 | 仮定 → PREMISE.md A-62 |
| GAP-RPT-21 | SCR-056 A1「差戻しと適用開始は監査証跡から取る」 / INC の TECH | 差戻し・適用開始を `audit_log` から取るには INC 側が `p_action`・定型 reason 接頭辞を揃えて書く必要があるが、その規約が #327（RPT-12） 側から指定されていない。 | 仮定 → PREMISE.md A-63 |
| GAP-RPT-22 | REPORT_DB §4.1 run_kind ARCHIVE_QUERY の結果セット（export_file） | cold 照会の結果セットの保持期間・再取得の権限再評価後の扱いが記述されていない。 | 仮定 → PREMISE.md A-64 |
| GAP-RPT-23 | SCR-057 A2「10:15 業務日が OPEN のまま → ロック待ち注意」・「翌 02:00 → SCR-066 に警告」 | 10:15 と翌 02:00 の判定主体が SCR-057（帳票）か OPS（枠組み）か STL（業務日オープン）か分かれる。 | 仮定 → PREMISE.md A-65 |
| GAP-STL-01 | SCR-037 §未決 Q1／Q3、SETTLEMENT_DB §5 Q1、ADR-004 結果欄（AS-039 顧客確認待ち） | 50 万円しきい値の判定単位（1 依頼の差額か明細行か累計か）が第 2 回 Q3 未回答。小額に分割して 1 段で通す回避策も未定義。返品の締め前起票（AS-155）も未確認。 | 確認 Issue 起票 #408（STL-Q） |
| GAP-STL-02 | SCR-040 Q1、SCR-036 Q3、BIZDAY_DB §5 Q1、STL_BUSINESS_DAY_UNLOCK_TECH §5… | 「会計出力済」＝ACK `.ok` 受領は P1 決定 C1 の前提で、第 2 回 Q6（.ng／60 分未着）は未回答。遅着 ACK でウィンドウ即時終了（AS-283）も発注者未確認。 | 確認 Issue 起票 #408（STL-Q） |
| GAP-STL-03 | SCR-039 Q2／Q3、SCR-042 Q2／Q5、SCR-038 Q1／Q2、SCR-041 Q2、SCR-037 Q2 | 照合部門長は役職でロールに無く、1 段目代行・紛争終了権限・解決者≠終了者を表せない。起票者の自分依頼閲覧、担当者ロール、証憑閲覧の監査対象も未決。 | 確認 Issue 起票 #408（STL-Q） |
| GAP-STL-04 | SCR-066 Q1〜Q4、README §5（市場カレンダーの保守画面なし）、AS-054 | 休市日・臨時開場・遅延開場を変更する画面が無く運用手順のみ。定休パターンは暫定（日曜＋祝日）。手動オープンの当日固定、取消判定にロット受付を含めるかも未決。 | 確認 Issue 起票 #408（STL-Q） |
| GAP-STL-05 | SCR-040 Q2／Q4／Q7、BIZDAY_DB §5 Q2／Q3 | 3 営業日の起点と承認時再検査（AS-234）、影響レコードの入力方法・500 行上限（AS-235）、ウィンドウ 120 分（AS-084）、休市日の占位行（AS-083）が設計レビューの前提のまま。 | 確認 Issue 起票 #408（STL-Q） |
| GAP-STL-06 | SCR-042 Q1、SCR-041 Q3（AS-238・AS-239） | エスカレーション期限超過で状態を自動的に ESCALATED にするか通知だけか、手動エスカレーションの要否、一覧の既定条件が未決。 | 確認 Issue 起票 #408（STL-Q） |
| GAP-STL-07 | SCR-035 Q1〜Q3（AS-150、AS-027 顧客確認待ち） | 差異の定義（取引金額−精算済み−調整額）が照合事務の見方と合うか、FY2019〜20 を同一画面で集計表示するか、外部参加者向け照合結果の要否が未決。 | 確認 Issue 起票 #408（STL-Q） |
| GAP-STL-08 | SCR-036 Q1／Q2、STL_BUSINESS_DAY_LOCK_TECH §4.1 No.4（AS-152） | 未完了引渡し・未解決紛争でロックを止める運用にするか（現設計は警告のみ）、プレビュー件数の一致をサーバでも検査するかが未決。 | 確認 Issue 起票 #408（STL-Q） |
| GAP-STL-09 | STL_BUSINESS_DAY_UNLOCK_TECH §4.6 No.4・§5 Q2、NOTIFICATION_DB 種別表 | 遅着 ACK によるウィンドウ強制終了の通知種別が NOTIFICATION_DB に無く、alert_event＋画面バナーで暫定代替している。 | 確認 Issue 起票 #408（STL-Q） |
| GAP-STL-10 | STL_UNLOCK_MODE_WRITE_TECH §4.3 No.4・§5 未決、AUCTION_DB | せり結果修正→生成取引明細の同期がトリガー経由であることを前提にしているが、AUCTION_DB に同期トリガーが未定義。API 直接 UPDATE だと E-STL-038 になる。 | 確認 Issue 起票 #408（STL-Q） |
| GAP-STL-11 | SCR-039 A2（「BE-owned」）vs SETTLEMENT_DB 規則 13・14・P5 R2-05、STL_CORRECTI… | SPEC は承認者資格を BE-owned と書くが、DB 側は規則 13・14 を正本とし「SCR-039 の BE のみは DB＋BE に読み替える」と注記。SPEC 本文は未修正。 | 仮定 → PREMISE.md A-66 |
| GAP-STL-12 | PF-01 遷移 5（「訂正は承認済み correction_request の bypass のみ」E-STL-014／015）vs A… | PF-01 遷移 5 の文言はプロトタイプ（元業務日にバイパスで書く）のままで、本設計（差額行は反映業務日＝OPEN 日、バイパスは最終防衛線）と整合していない。 | 仮定 → PREMISE.md A-67 |
| GAP-STL-13 | SCR-042 A4、SETTLEMENT_DB §4.3 注記 (4)、ADR-014 日次ジョブ一覧、STL_BUSINESS_DAY… | 紛争 SLA 判定バッチには TECH 文書・API・job_code が無い。UNLOCK_EXPIRE・BUSINESS_DAY_OPEN・DISPUTE_SLA の job_code が ADR-014／REPORT_DB の一覧に登録されているか未確認。 | 設計修正 → PREMISE.md C-24 |
| GAP-STL-14 | SETTLEMENT_DB §4.3 列 2（`next_number('dispute')`「予約名に dispute を追加依頼」） | 紛争番号の採番は COMMON_DB `next_number` の予約名追加が前提だが、COMMON_DB 側で確定した記述が無い。 | 設計修正 → PREMISE.md C-25 |
| GAP-STL-15 | IAM_DB role_permission（CORRECTION_L2_APPROVE・UNLOCK_APPROVE）、NOTIFICA… | 本 feature が参照する権限コード 2 つ・通知種別 4 つ・アラートコード 1 つの seed は他 feature の DB issue に属し、本 feature からは依頼しかできない。 | 保留: #118（IAM-01）、#280（NTF-02）、#307（OPS-02） の seed issue に依頼。未登録なら #364（STL-05）・06・14・16・17 の結合テストが失敗。 |
| GAP-STL-16 | SCR-040 A8・㉛、PF-01 §4.1、STL_UNLOCK_MODE_WRITE §3（遷移先 SCR-016・019・022・… | 締め解除モードの UI（バナー・業務日固定・パラメタ付き API 呼出し）は 6 画面が属する 4 feature（LOT／TRD／DLV／AUC）側の SPEC 実装に依存し、本 feature は Guard と契約しか持てない。 | 保留: #372（STL-07-a） の組込み手順書を #233（LOT-03）／#256（TRD-02）／#85（DLV-01）／#23（AUC-01） へ提示。各 feature の該当画面 issue に「締め解除モード」サブタスクが必要。 |
| GAP-STL-17 | STL_SETTLEMENT_TAX §4.3（引渡し完了時の当回金額の按分は DELIVERY_DB §5 T3 で未決） | 税関数の入力となる精算行の金額按分（分割引渡し）が DELIVERY_DB 側で未決のため、精算行の税額テストは按分確定後にしか閉じない。 | 保留: #85（DLV-01）（DELIVERY_DB T3） |
| GAP-STL-18 | STL_SETTLEMENT_TAX §4.6（AS-291）、RFP Appendix C.3 DS-INC-EDGE-01 | DS-INC-EDGE-01 はケース名と期待規則だけで数値を持たず、テストベクターの数値は設計側の仮置き。#6（ACC-02） 厳格合格基準（REQ-002 Q18）として発注者の数値確認が無い。 | 仮定 → PREMISE.md A-68 |
| GAP-STL-19 | SETTLEMENT_DB §4.4（settlement_monthly_legacy は producta_migration ロール… | FY2019〜20 の集計表示は移行 W3-c の投入後にしかデータが無く、feature 単体のテスト環境では producta_migration ロールでの投入手順が必要。 | 保留: #74（MIG-04）（data-migration: W3-c の投入手順・テストデータ） |
| GAP-STL-20 | drift DP-05、error-codes §15.4、SCR-039 A6、SCR-066 E4〜E6 | CHECK・一意制約違反を 500 でなく 409＋E-code に写す共通変換（制約名→E-code 表）は横断基盤で、本 feature の E-STL-007／008／004／005／006 の表示はそれに依存する。 | 保留: #57（XC-03）（api-conventions §3.2 の変換ミドルウェア） |
| GAP-STL-21 | SCR-039 E18（E-COM-007 承認・却下以外の操作指定）vs STL_APPROVE_CORRECTION_API 注記（v… | SPEC のエラー表に v1 では発生しないコードが残っている。 | 仮定 → PREMISE.md A-69 |
| GAP-STL-22 | ADR-006 決定 3（7 表）vs STL_BUSINESS_DAY_LOCK §3（7 表＋delivery_exception I… | 締め後遮断の対象表の数が文書間で 7／9 と揺れている（ADR-006 が旧記載）。 | 仮定 → PREMISE.md A-70 |
