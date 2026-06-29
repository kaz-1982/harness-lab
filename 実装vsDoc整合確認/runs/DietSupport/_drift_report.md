---
doc_id: _drift_report
title: ドリフトレポート(実装↔設計 乖離一覧)
phase: Phase 5 / 実装整合(リバース同期)
depends_on: [_id_registry, _doc_plan]
---

# ドリフトレポート — DietSupport

> Phase 5「実装整合(リバース同期)」Step R2 成果物。実装(`../DietSupport_app/`)を正として設計docとの乖離をID単位で洗い出す。手順は [harness/04_reconciliation.md](../harness/04_reconciliation.md)。

- 生成日: 2026-06-27
- 正の原則: **コードを正(逆同期)**
- 入力ソース: ①`DietSupport_app/src`・`server`・`dietsupport.db`(sqlite `.schema` 確認済)・`tests`・`e2e` ②`DietSupport_app/DESIGN_DIGEST.md` ③app `git log`(全5件) + doc `ChangeLog.md` ④`output/_id_registry.md`

## 1. サマリ

- 検出乖離: **9件**(追加 2 / 変更 4 / 方式差 1 / 軽微差 2)
- 修正対象doc(暫定): **D-8, D-9, D-10, D-13, D-14, D-12, D-6, B-6, B-19, B-16, TS-1, D-15, B-12(注記)**
- 整合確認のみ(修正不要): **D-12(評価/集計/ストリーク/競合の各式), D-2, D-4, D-7, B-1, B-2, B-3, R-*(要件)**
- **要ユーザー判断: 2件**(§4。①物理データモデルの扱い ②全削除機能のID化)

## 2. 乖離一覧(ID差分表)

| # | 種別 | ID/対象 | doc上の記述 | 実装の現状(出典) | 影響doc | 対応方針 | 状態 |
|---|---|---|---|---|---|---|---|
| D-01 | **方式差** | 物理データモデル | T-001〜T-012 の業務テーブルを個別物理化(CHECK制約/FK/idx_sync_*) | サーバーは業務テーブルを物理化せず **`account` + `sync_record`(account_id,tbl,id,updated_at,deleted,payload JSON) の2テーブル汎用同期ストア**。業務データは payload JSON。業務テーブル単位の表現は**クライアント IndexedDB ストア**側のみ(`server/app/sync_server.py:133-154`, `src/infrastructure/idb.ts:5-23`) | D-8, D-9, D-10, B-12(注記) | **要判断(§4-①)**。論理ER(B-12/E-*)は維持可 | 未 |
| D-02 | 追加 | 記録の全削除 | 該当機能・モジュール・テストなし | 「記録をすべて削除」= 日々の記録4ストア(weight/meal/workout/daily_achievement)を一括 tombstone→即同期で復活防止。`repository.clearStore`(未削除行を tombstone・件数返却) / `store.clearRecords` / Settings 確認ダイアログ(commit 7121bc7) | B-6(F-018?), D-12, D-6, TS-1/D-15, D-14(確認文言) | **要判断(§4-②)** 後、新ID採番+各docへ追記 | 未 |
| D-03 | 変更 | A-001〜003 / 認証トークン | D-13「Bearer、方式は実装で確定」/ D-6③ logout=セッション無効化 / D-14 AUT-003 期限切れ | **自作 HMAC-SHA256 署名トークン(JWT風・stdlib)・サーバー無保存・TTL30日**。logout はクライアント破棄のみ(サーバー失効なし)。PW=PBKDF2 100k(`sync_server.py:79-115,222-223`) | D-13, D-6, B-19, D-14 | コードを正に確定記述。logout 遷移を「クライアント側破棄」に明記 | 未 |
| D-04 | 変更 | A-002 レート制限 | D-13「例:5回/分/IP」/ UT-053「例:6回/分」/ B-19 | **プロセス内メモリで揮発(再起動でリセット)・5回/60秒窓**。コードが「永続化は残課題」と明記(`sync_server.py:27-31,207-217`) | D-13, B-19, D-14(AUT-002) | 実値(5回/60秒)で確定。揮発性=残課題を B-19 に明記 | 未 |
| D-05 | 変更 | uuid 生成 | `crypto.randomUUID` 前提(暗黙) | **非セキュアコンテキスト対応 `uuid()` ヘルパ**(randomUUID 不可時 getRandomValues フォールバック / RFC4122v4)。iPhone を LAN http で実機利用するための対応(commit 1ff3384, `app/uuid.ts`) | D-12, B-16 or B-19 | D-12 にモジュール追記、運用前提(LAN http 実機)を B-16/B-19 に注記 | 未 |
| D-06 | 変更 | HTTP ステータス | D-13: logout 204 / signup 201 | **logout=200 `{ok:true}` / signup=200 `{token,account_id}`**(204/201でない。FastAPI 既定200)(`main.py:97-123` 確認済) | D-13 | 実装(200)に訂正 | 未 |
| D-07 | **追加** | 食事区分 snack(間食) | 食事区分=朝/昼/夕の3種(DDL CHECK=`morning/noon/night`) | **4種目に間食 `snack` を追加**。`MealType='morning'\|'noon'\|'night'\|'snack'`、ラベル「間食」、間食専用UI(スキップ導線なし)、シードメニュー有(`src/app/date.ts:35-51`, `Meal.tsx:187`, `seed.ts:17-19`) | D-9(CHECK), B-12(E-002), D-14, B-6(F-002概要) | 4値に拡張、間食の評価/UI差を注記 | 未 |
| D-08 | 追加(軽微) | `GET /api/v1/health` | 記載なし | ヘルスチェック `{status:ok}`(`main.py:91-93`) | D-13 | 補助エンドポイントとして追記 | 未 |
| D-09 | 確認要 | シード/秘密鍵 | 記載なし | dev シードアカウント `me@example.com`/`correct-horse`、dev JWT secret、同期テストレコード `w1` がハードコード(`sync_server.py:37-43,157-182`) | B-17 or B-19(注記) | 本番除去前提を運用設計に注記(コード側課題の可能性) | 未 |

## 3. doc別 修正方針

| doc | 区分(R1) | 方針 | 触る箇所 |
|---|---|---|---|
| D-8/D-9/D-10 | スキーマ突合 | §4-① の決定に従う。論理(B-12)は維持、物理は実装方式を反映 | 物理ER・テーブル定義・DDL 全体 + meal_type 表記 |
| D-13 | 修正必須 | A-001〜005 のトークン方式・レート制限・ステータス・/health を実装に合わせ確定 | §認証・§共通・各API |
| D-14 | 修正必須 | AUT-002/003 の発火条件を実装に整合 | メッセージ一覧 |
| D-12 | 修正必須 | uuid モジュール追記、clearStore/clearRecords モジュール追加(§4-②後) | モジュール一覧 |
| D-6 | 変わった分 | ③認証 logout=クライアント破棄、(全削除を入れるなら)④日次記録の一括削除遷移 | 状態遷移表 |
| B-6 | 要確認 | 全削除機能の位置づけ(F-018 or F-015拡張) | 機能一覧 |
| B-19 | 要確認 | トークン方式・レート制限揮発性・LAN http 実機運用・dev秘密鍵 | セキュリティ方針 |
| B-16 | 据え置き→注記 | uuid フォールバックの共通方式注記(必要時のみ) | 方式共通 |
| TS-1/D-15 | 挙動追従 | 全削除の受け入れ/単体ケース追加(§4-②後) | テストケース |
| B-12 | 注記 | 「論理エンティティはクライアントで実現、サーバーは汎用同期ストアで永続化」の注記 | 巻末注記 |

## 4. 要ユーザー判断事項

| # | 論点 | 選択肢 | 推奨 |
|---|---|---|---|
| 1 | **物理データモデル(D-8/D-9/D-10)の扱い**。サーバーが業務テーブルを物理化せず汎用 `sync_record`(JSON payload)で永続化している | (a) 実装に合わせ全面改訂(業務テーブル定義を捨て、汎用同期ストア構造で書き直す) / (b) **論理スキーマ(業務テーブル定義)はクライアント論理として保持し、「サーバーは汎用 sync_record で永続化する」方式注記を加える** / (c) 両方併記 | **(b)**。論理ER(B-12)とクライアント IndexedDB が業務テーブルを実体化しており、定義を捨てると情報損失。方式差を注記で吸収するのが最小改修で最も忠実 |
| 2 | **「記録をすべて削除」のID化** | (a) **新機能 F-018 として採番**(削除=独立した利用シーン) / (b) F-015(バックアップ・データ管理)配下の機能として吸収 | **(a)**。利用者視点で独立した操作・確認導線があり、トレーサビリティ上も独立IDが明快 |

## 5. 整合確認済(修正不要 — 直さなかった記録)

実装とドキュメントが一致しており、逆同期で**変更しなかった**設計:

- **D-12 / D-15 評価ロジック**: `evaluateMeal` の `◎=(kcal≤目標)∧(P≥目標)∧(F≤目標)∧(C≤目標)`、目標未設定→○、空→なし(`src/domain/evaluation.ts` = 仕様一致)
- **ストリーク**: `calcStreak` 当日未記録は非中断、遡り連続(`src/domain/streak.ts` = D-12/UT 一致)
- **LWW 競合解決**: `resolveConflict` 同値は local 優先(`>=`)、削除伝播(`src/domain/conflict.ts` = UT-032 一致)
- **PFC集計**: `aggregate` deleted 除外・qty 反映(`src/domain/aggregate.ts` 一致)
- **抜け検知**: `detectGap` 履歴ゼロでは gap 出さない(`src/domain/gap.ts` 一致)
- **エラーメッセージ体系**: VAL/PER/SYN/AUT/SYS 区分・やさしい文言(`application/errors.ts` 一致、※AUT-002/003 の条件のみ D-03/D-04 で要調整)
- **基本アーキ**: ローカルファースト+サーバー同期、レイヤード+DI(B-1/B-2/B-3 = 実装の `src` 層構成と一致)
- **要件(R-*)**: スコープ・Won't(消費カロリー算出/AIアドバイス/写真記録/複数ユーザー)は実装と一致

## 6. 状態

- [ ] §4 のユーザー判断(①②)
- [ ] Step R3 影響波及トレースで修正スコープ確定
- [ ] Step R4 1docずつ修正(D-13 → D-14 → D-8/9/10 → D-12 → D-6 → B-6/B-19 → TS-1/D-15 の順を推奨)
- [ ] Step R5 check.py 緑 + DESIGN_DIGEST 再生成
