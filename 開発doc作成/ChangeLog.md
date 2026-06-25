# Changelog

このプロジェクトの注目すべき変更はすべてこのファイルに記載されます。

フォーマットは [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) に基づいており、
このプロジェクトは [Semantic Versioning](https://semver.org/lang/ja/) に準拠しています。

変更カテゴリ

Added — 新機能
Changed — 既存機能の変更
Deprecated — 非推奨になった機能
Removed — 削除された機能
Fixed — バグ修正
Security — セキュリティ関連の修正


## [0.11.0] - 2026-06-26

### Added
- **セッション間引き継ぎの自動化**(v0.11)
  - `output/_session_log.md`: セッション境界で Claude が追記する引き継ぎログの雛形を新設(出力時系列順、各エントリに「完了 / 進行中 / 次の開始点 / 意思決定メモ / 残 TBD / check.py 結果 / 関連コミット」を構造化)
  - `check.py --session-start` モード: `_session_log.md` 末尾の前セッションエントリを stdout に表示。セッション開始時に Claude が現在地を把握する補助
  - `check.py --session-end` モード: 新規エントリのテンプレ(日付・セッション番号・完了/進行中ドキュメント自動算出)を stdout に出力。セッション終了時にコピペして埋めて追記する
  - CLAUDE.md「起動時の挙動」末尾に「セッション境界の挙動」セクションを追加(開始時に `--session-start` を読む / 終了時に `--session-end` で追記する流れを明文化)
- **テンプレ DSL 化**(v0.11)
  - `harness/spec/templates.py`: 13 テンプレのメタ情報(`doc_id` / `phase_key` / `required_when_key` / `depends_on` / `mode_key` / 名称 / `section4_titles`)を一元管理する中央台帳。i18n 対応で複数言語の名称と節タイトルを保持
  - `harness/spec/i18n_labels.py`: 言語別のラベル辞書(phase / required_when / mode の本文表記、節見出し、scope / 上流 / 下流 / 改訂履歴 / レビュー状態 / 例 のラベル)
  - `harness/tools/gen-templates.py`: 3 つのモード
    - `--list [--lang LANG]`: 仕様に登録された全テンプレと言語パックの有無を表示
    - `--check --lang LANG`: 既存テンプレ(`templates/*.md` / `templates/{lang}/*.md`)の frontmatter を仕様と突合
    - `--stub DOC_ID --lang LANG`: 指定テンプレの雛形を stdout に出力(他言語版を起こすときに利用)
- **英語対応の第一歩**(v0.11)
  - 仕様の `R-1` / `R-9` / `R-13` に `en` 言語パックを追加(名称 + 節タイトル + i18n ラベル)
  - `harness/templates/en/R-1_business_requirements.md` / `R-9_nonfunctional_requirements.md` / `R-13_glossary.md` を同梱
  - 残り 10 本も `gen-templates.py --stub <id> --lang en` で雛形作成 → 手動加筆の流れで追加可能

### Changed
- 既存テンプレ B-1 / B-2 / B-6 の `required_when` を仕様(`spec/templates.py`)の canonical 表記に統一(v0.10 までは個別に微妙な表現があり、DSL の単一情報源原則と不整合だった)
  - B-1: `WF / ハイブリッド上流で必須 / アジャイル中規模以上で推奨` → `WF / ハイブリッド上流で必須(アジャイル単独運用では R-7 で代替可)`
  - B-2: `全規模・全手法で必須(アジャイル時は軽量版でOK、最初のスプリント前に作成)` → `全規模・全手法で必須`
  - B-6: `WF / ハイブリッド上流で必須(アジャイル時は R-7 ストーリーで代替可)` → `WF / ハイブリッド上流で必須(アジャイル単独運用では R-7 で代替可)`
- `harness/_files_overview.md` / `harness/templates/_index.md` を v0.11 の新ファイル(`spec/` / `tools/gen-templates.py` / `templates/en/`)に対応
- `.harness-source` のバージョン表記を `v0.10` → `v0.11` に
- ハーネスバージョン v0.10 → v0.11
- **後方互換**: 既存テンプレの本文(セクション 1〜7 配下)には触れず、frontmatter の `required_when` のみ canonical 化。`check.py` の 10 検査カテゴリは変更なし。fixtures(sample_ok 0件 / ng 6件 / orphan 3件 / v09 5件 / v10_glossary 1件 / v10_cycle 1件)と golden sample(0 件)は回帰なし


## [0.10.0] - 2026-06-26

### Added
- `check.py` に **用語整合検査**(R-13 用語集の「使用禁止語」が他ドキュメント本文に出現していないか確認)を追加(v0.10)。R-13 が存在しない案件、表の列構造が想定外の案件、禁止語列が空の案件はスキップ。1ファイル × 1禁止語 で 1 件のみ報告(過剰警告を抑制)
- `check.py` に **depends_on 循環検出**(全ドキュメントの frontmatter `depends_on` を DAG として集約し、DFS の三色塗りで循環参照を検出)を追加。同じ循環(開始点違いの並び替え)は重複排除して 1 件に集約して報告
- **golden sample 案件** `examples/sample_case/` を同梱(v0.10)。小規模アジャイル案件「経理 SaaS — 月次決算 売掛金集計の早期化」の最小完成版(R-1 / R-7 / R-9 / R-13 / B-2 / ADR-0001 + プロファイル / 計画 / 採番台帳 / レビューログ)。`python harness/tools/check.py examples/sample_case` で **緑** になることを確認可能
- `examples/README.md` を新規作成。golden sample の案件設定・含まれるドキュメント一覧・使い方を記載
- **ハーネス本体マーカー** `.harness-source` を追加(v0.10)。リポジトリ直下に置かれ「ここはハーネス本体(マスター)」を示す。案件コピー側には存在しない
- **新規案件コピースクリプト** `harness/tools/new-project.sh` を追加。`.harness-source` を持つディレクトリでのみ動作する安全装置付き。コピー時に `.harness-source` / `examples/` / `_tbd_dashboard.md` などを自動除外、案件コピー側に必要なものだけを残す
- 新規 fixture `harness/tools/fixtures/sample_v10_glossary/`(用語整合の異常系。1件検出)
- 新規 fixture `harness/tools/fixtures/sample_v10_cycle/`(3ノード循環 R-1 → R-2 → R-3 → R-1 の異常系。1件検出)

### Changed
- `CLAUDE.md` の「起動時の挙動」に **ハーネス本体ガード** を追加。`.harness-source` が存在する状態で案件作業を始めようとしたら、`new-project.sh` でコピー作成を案内する流れに(本体でテスト目的等で進めたい場合はユーザーが明示すれば通常フロー)
- `README.md` の「想定する使い方」に `new-project.sh` を推奨手順として追記、手動コピー時にも `.harness-source` / `examples/` の削除手順を併記
- `harness/tools/fixtures/sample_v09/02_要件定義/R-2_業務フロー.md` の `depends_on` を `[R-1]` から `[]` に変更(v0.10 で追加された循環検出が自己ループ R-1 → R-1 を捕捉する副作用を回避し、各 fixture が「意図する検査だけを発火させる」設計に整理)
- `harness/tools/check.py` の冒頭 docstring に検査項目 9 / 10 を追記し、検査総数を 10 カテゴリに更新
- ハーネスバージョン v0.9 → v0.10
- **後方互換**: `sample_ok` 0件 / `sample_ng` 6件 / `sample_orphan` 3件 / `sample_v09` 5件 は回帰なし。用語整合は R-13 不在時 / 表の列が想定外時 / 禁止語列空時にスキップし、循環検出は循環が無ければ無音(graph 構築のみ)で動作するため、既存案件への影響なし


## [0.9.0] - 2026-06-26

### Added
- `check.py` に **依存検証**(`depends_on` 機械検証)を追加。frontmatter `depends_on` の各IDが `_doc_plan` に存在し、本書が「進行中以上」のとき依存先が「承認済」相当(承認済 / 取り込み済 / ゲート2承認 / 蓄積中)になっているか確認。`harness/02_workflow.md` の Step B「依存関係確認」の機械化
- `check.py` に **ファイル名 ↔ doc_id 整合検証** を追加。ファイル名先頭(`R-1_xxx.md` → "R-1")と frontmatter `doc_id` の一致を確認。リネーム事故の検出
- `check.py` に **ADR 索引と ADR ファイル群の突合** を追加。`output/横断/ADR/_index.md` の表セルと `ADR-*.md` ファイル群を双方向に突合し、索引漏れ / 索引のゴースト / `status` 未記入を検出。ADR ディレクトリ自体が無い案件はスキップ
- **Phase 0 トリガを許可拡張子 allowlist 方式** に変更(`harness/00_intake.md` §0-1)。`.md` / `.txt` / `.docx` / `.pptx` / `.xlsx` / `.pdf` / `.png` / `.jpg` / `.jpeg` / `.gif` / `.svg` のみがトリガ。`.DS_Store` / `Thumbs.db` / `~$*.docx` / `*.tmp` 等の OS / エディタ生成ファイルでの誤発火を防止
- **pre-commit フック** を同梱(`harness/tools/hooks/pre-commit`)+ **導入スクリプト**(`harness/tools/install-hooks.sh`)。`output/` 配下のファイルが staging に含まれているコミットでのみ `check.py` を自動実行、整合性エラーがあればコミット中断。Windows でシンボリックリンクが使えない環境は自動的にコピーへフォールバック
- `harness/_files_overview.md` を新規作成。CLAUDE.md にあった「主要ファイル」表を分離して索引化
- フィクスチャ `harness/tools/fixtures/sample_v09/` を追加(v0.9 で増えた 3 検査をデモ: ファイル名整合 ×1 / 依存検証 ×1 / ADR 突合 ×3 = 5件検出)

### Changed
- **`CLAUDE.md` をスリム化**(205 → 約 140 行、約 30% 減)
  - 「主要ファイル」表(約 28 行)を `harness/_files_overview.md` に分離
  - 「開発手法による分岐」を WF / Agile / Hybrid 各 1 行に圧縮し、詳細手順は `harness/02_workflow.md` に委譲
  - 3ツール協調フローの冗長な解説文を削除し、表 + リンクに圧縮
  - 起動時の挙動の各箇条書きを 1〜2 行に圧縮
- `harness/01_selection_rules.md` の Phase 0 発動条件を新しい allowlist に合わせて更新
- `input/事前検討資料/README.md` の許可形式・対象外ファイルの説明を更新
- `harness/tools/README.md` を v0.9 の新検査(依存検証 / ファイル名整合 / ADR 突合)・pre-commit フック導入手順・新フィクスチャ `sample_v09` の説明に更新
- ハーネスバージョン v0.8 → v0.9
- **後方互換**: `sample_ok` 0件 / `sample_ng` 6件 / `sample_orphan` 3件 は回帰なし。新検査はそれぞれ「該当ドキュメントが無い案件はスキップ」(ADR は ADR ディレクトリ不在時、依存検証は plan 不在時、ファイル名整合は `_` を含まない名前は対象外)するため、既存案件の挙動を変えない


## [0.8.0] - 2026-06-26

### Added
- **必須テンプレ13本を事前同梱**(`harness/templates/`)。これまで案件ごとに Claude が `input/システム開発設計ドキュメント一覧.md` から派生生成していた主軸ドキュメントを、ハーネス側で事前生成しコピー段階で揃うようにした。再現性(同じ構造)と生成コストの両面で改善
  - 要件: R-1 業務要件定義書 / R-7 ユーザーストーリー / R-8 機能要件定義書(SRS) / R-9 非機能要件定義書 / R-13 用語集 / R-14 RTM
  - 基本設計: B-1 システム方式設計書 / B-2 ソフトウェアアーキテクチャ設計書 / B-6 機能一覧 / B-12 論理データモデル
  - 詳細設計: D-8 物理データモデル / D-9 テーブル定義書・インデックス設計書 / D-10 DDL
- `check.py` に **孤立検出**(R-14 RTM の表セルから登録済 `R-B-*` / `R-F-*` / `F-*` が出現するか確認)を追加。RTM 不在案件ではスキップ
- `check.py` に **AC/AT 網羅検出**(TS-1 が AT-* 定義済のとき、登録 `R-F-*` が TS-1 の表セルに参照されているか確認)を追加。TDD 不採用 or 骨子段階ではスキップ。Phase 3.5 ゲート1の完了基準の機械化
- `check.py` に **TBD 集約**(`--tbd` オプション)を追加。全ドキュメント本文 / 各 `## 7. レビュー状態` / `project_profile.md` の保留セクション を `output/_tbd_dashboard.md` に集約。完了判定前の取り残し確認用
- `check.py` を Windows CP932 端末でも ✅ / ❌ を出力できるよう stdout を UTF-8 にリコンフィグ(`sys.stdout.reconfigure`)
- フィクスチャ `harness/tools/fixtures/sample_orphan/` を追加(孤立検出 ×2 + AC/AT 網羅 ×1 = 3件検出する異常系)

### Changed
- **`WORKFLOW.md` と `harness/02_workflow.md` の役割を明確に分離**。両者で同じ手順を二重管理していた状態(改修のたびにズレが発生)を解消
  - `WORKFLOW.md` = 全体マップ・図(mermaid)・ディレクトリ仕様・依存図・ゲート完了基準 等の **「何を」を参照する**
  - `harness/02_workflow.md` = Claude が動かす **「どう実行するか」の手順** のみ
  - 各節の冒頭で対応関係を明示(本書の節 ↔ WORKFLOW.md の節 のマッピング表)
- `harness/templates/_index.md` を「事前同梱(✅)+ 遅延生成(⬜)のハイブリッド」方針に書き直し、生成記録に v0.8 の事前同梱13本を追記
- `harness/tools/README.md` を孤立検出 / AC/AT 網羅 / TBD ダッシュボード / 新フィクスチャ `sample_orphan` 対応に更新
- ハーネスバージョン v0.7 → v0.8
- **後方互換**: `sample_ok` 0件 / `sample_ng` 6件 は回帰なし。事前同梱テンプレは原典資料の項目と整合しており、既存案件の挙動を変えない。`check.py` の新検査は **R-14 / TS-1 不在時はスキップ** するため、RTM省略案件 / TDD不採用案件にも影響なし


## [0.7.0] - 2026-06-23

### Added
- **セッション分割の運用ガイド** を新設(`WORKFLOW.md` §9）。規模の大きい案件で1セッションに作業を詰め込むとコンテキストが肥大し、ツール(特にファイル書き込み)が不安定になる問題を、状態ファイル(`output/project_profile.md` / `output/_doc_plan.md` / `output/_id_registry.md`)駆動の再開性を活かして「セッション単位の分割」で回避する運用を明文化
  - §9.1 区切りの単位(目安はドキュメント2〜3本ごとに1セッション / フェーズ境界 Phase 1→2→3→3.5 では必ず分割 / 大型ドキュメントは単独セッション / 最初のセッションはインテーク → 選定 `_doc_plan.md` 確定に専念)
  - §9.2 セッション終了時の手順(着手ドキュメントを完了まで通す → 状態ファイル最新化 → `git commit`。**このコミットが次セッションの再開点**)
  - §9.3 セッション開始時の手順(CLAUDE.md「起動時の挙動」で現在地を自動判別。ユーザーは「続きをお願い」と伝えるだけでよい)
  - §9.4 セッション境界のイメージ(ウォーターフォール / 大規模の典型例と、セッション数の目安 `N ÷ 2.5 + フェーズ境界の本数`)

### Changed
- `output/project_profile.md` のハーネスバージョン表記を v0.7 に更新
- `CLAUDE.md` の「## バージョン」セクションを v0.7 に更新
- ハーネスバージョン v0.6 → v0.7
- **後方互換**: 運用ガイド(取説)の追加のみ。テンプレ・選定ルール(`01_selection_rules.md`)・`check.py`・ID体系・各ドキュメントの中身には変更がなく、既存案件の挙動・成果物に影響しない


## [0.6.0] - 2026-06-23

### Added
- **ADR(アーキテクチャ決定記録)** を新設(原典外・ハーネス拡張)。1決定1ファイルを `output/横断/ADR/` に蓄積し、MADR / Nygard 形式(ステータス / コンテキスト / 決定 / 検討した選択肢 / 影響)で記録。索引は `output/横断/ADR/_index.md`。テンプレ `harness/templates/ADR-NNNN_アーキテクチャ決定記録.md`(frontmatter は `adr_id`、`check.py` の標準検証対象外)
- **DDD ドメインモデル DM-1** を新設(原典外・ハーネス拡張)。集約・エンティティ・値オブジェクト・ドメインサービス・ドメインイベント・リポジトリ・ユビキタス言語・境界づけられたコンテキスト・不変条件を表現。テンプレ `harness/templates/DM-1_ドメインモデル.md`(標準セクション 1〜7 準拠)。R-4 概念データモデルを上流、B-12 / D-2 を下流とする結節点
- インスタンスID `AG-`(集約)・`VO-`(値オブジェクト)を ID 体系に追加(`check.py` の `INSTANCE_PREFIXES` に登録)。DDD のエンティティは原典の `E-` を流用
- 文書ID `DM-`(ドメインモデル)・`ADR-`(アーキテクチャ決定記録)を文書IDレイヤーに追加(インスタンスID採番と独立)
- `harness/templates/_format.md` に **「1文1行」改行規約**(地の文は句点ごとに改行 / 表・コード・引用ブロックは対象外)を追加
- `harness/01_selection_rules.md` に §8「ドメインモデル・ADR(原典外)」と状態値 `蓄積中`(ADR)を追加
- `harness/03_quality_checklist.md` に図形式(1-8)・1文1行(1-9)・DM-1 整合(2-4)・DM-1 / ADR レビュー観点を追加
- `harness/00_intake.md` / `output/project_profile.md` に「DDD 採用」項目を追加(DM-1 の発火スイッチ)
- `doc_harness.code-workspace` に VS Code 拡張「Draw.io Integration」(`hediet.vscode-drawio`)の推奨を追加

### Changed
- **図の方針を「Mermaid 推奨」→「`.drawio.svg` 正本」に変更**。レンダラー非対応の環境で Mermaid が表示されない問題を解消(SVG として全環境で表示でき、Draw.io 拡張で再編集可。Mermaid は補助として併記可)。対象は案件成果物の図で、ハーネス取説図(`WORKFLOW.md`)の Mermaid は対象外
- `harness/tools/check.py`: `INSTANCE_PREFIXES` に `AG` / `VO` を追加、`EXCLUDE_DIRS = {"ADR"}` で `output/横断/ADR/` 配下を標準検証(構造・状態突合)から除外
- `harness/02_workflow.md` に DM-1(R-4 の後)と ADR(随時の軽量フロー)を組み込み、完了判定に DM-1 / ADR を追加
- `CLAUDE.md` のID体系表・文書IDレイヤー解説・主要ファイル表・ルール5(テンプレ準拠と記述スタイル)・3ツールフロー表を更新
- `WORKFLOW.md` のフロー図・依存図・ディレクトリ図・引き渡し refs に DM-1 / ADR を反映
- 既存の原典外テンプレ(PR-1 / D-15 / TS-1)の地の文を1文1行規約に整形
- 全ファイルのバージョン表記を v0.6 に統一(`README.md` が v0.4 のままだったズレも是正)
- **後方互換**: `AG-` / `VO-` 追加と ADR 除外は既存案件のID・既存ドキュメントの挙動を変えない(regex 拡張は既存マッチを保存。fixtures `sample_ok` 0件 / `sample_ng` 6件 は回帰なし)。DM-1 / ADR / DDD はオプションで、DDD 非採用・ADR 不使用の案件は従来どおり
- ハーネスバージョン v0.5 → v0.6


## [0.5.0] - 2026-06-01

### Added
- **Phase 0「事前検討の取り込み」(任意)** を新設。要件定義の前段で「問題・原因・対応策」を検討した資料がある場合に発動する、3ツール協調フローの最上流オプションフェーズ
- 事前検討資料の投入先 `input/事前検討資料/`(ユーザーが資料を配置 / 形式自由)と説明 `README.md`
- PR-1 事前検討サマリ(原典外・ハーネス拡張)テンプレ `harness/templates/PR-1_事前検討サマリ.md`(「問題 → 原因 → 対応策 → 想定要件・制約・前提」に正規化、要件への追跡性を確保)。生成先は `output/00_事前検討/`
- 文書ID `PR-`(Pre-study)を文書IDレイヤーに追加(`TS-` 同様にインスタンスID採番と独立)
- `harness/01_selection_rules.md` に担当 `CC0`(Phase 0)と PR-1 の条件付き作成ルールを追加
- `harness/03_quality_checklist.md` に「Phase 0 → インテーク」移行チェックを追加

### Changed
- `harness/00_intake.md` に「0. 事前検討資料の確認」を質問1の前段として追加(資料があれば PR-1 を生成し、以降の質問を確認形式に切り替えてユーザー負担を軽減 / 無ければスキップ)
- `harness/02_workflow.md` に §0.5「事前検討の取り込み」手順、`CLAUDE.md` 起動時の挙動・3ツールフロー表、`WORKFLOW.md` の全体図(Phase 0 ノード)・役割表・ディレクトリ図を更新
- `harness/templates/_format.md` の phase 列挙に「事前検討」を追加、「T 系列テンプレ生成の例外規定」を「原典外ドキュメントの例外規定」に一般化し PR-1 を追記
- `output/project_profile.md` に「0. 事前検討資料」セクションを追加
- ハーネスバージョン v0.4 → v0.5
- **後方互換**: 事前検討資料が無い案件は Phase 0 をスキップし、従来どおりインテークから開始(既存の運用に影響なし)


## [0.4.0] - 2026-05-29

### Added
- 整合性検証スクリプト `harness/tools/check.py`(Python標準のみ・read-only)。構造チェック / ID整合 / 状態突合を機械検証
- `harness/tools/fixtures/`(正常系・異常系サンプル)と `harness/tools/README.md`
- `_id_registry.md` のフォーマットを CLAUDE.md「3. ID体系の一貫性」で正本定義(機械可読な表形式)

### Changed
- `CLAUDE.md` ルール6 / `harness/02_workflow.md` Step F・完了判定 / `harness/03_quality_checklist.md` を「機械チェック(自動)+ 観点チェック(手動)」の2層運用に再編
- ハーネスバージョン v0.3 → v0.4


## [0.3.0] - 2026-05-29

### Added
- Phase 3.5(テスト具体化 + 2段階レビューゲート)を新設。テスト戦略 = TDD の案件で発動するオプション運用
- TS-1 受け入れテスト仕様書テンプレ(原典外・ハーネス拡張)、D-15 単体テスト仕様書テンプレ
- `harness/templates/_test_code_convention.md`(テストコード生成規約・言語非依存)
- `output/_handoff_to_implementation/`(Phase 3.5 → Phase 4 引き渡しパッケージ、Red テスト)
- インテーク質問票に「テスト戦略(TDD / 通常 / 未定)」「テストフレームワーク」を追加(Phase 3.5 の発火スイッチ)
- ID体系にテストケースID(UT- 単体 / AT- 受け入れ)を追加
- `WORKFLOW.md` に §7.5「Phase 3.5 仕様」とテスト依存図を追加

### Changed
- D-15 単体テスト仕様書を「Phase 3 で骨子 → Phase 3.5 で最終化」に(TDD採用時)
- `harness/01_selection_rules.md` に担当 `CC1-P35` と状態値(ゲート1承認 / Red作成済 / ゲート2承認)を追加
- `harness/03_quality_checklist.md` に Phase 3.5 ゲート1 / ゲート2 のチェックを追加
- ハーネス本体の改修記録先を `ChangeLog.md`、案件中の微修正を `output/_review_log.md` と整理(CLAUDE.md)
- バージョン表記を全ファイルで統一(従来 CLAUDE/README=v0.2、profile=v0.1、ChangeLog=0.0.2 が混在 → 本版より SemVer `0.3.0` / ドキュメント表記 `v0.3` に一本化)
- 運用前提モデルIDを `claude-opus-4-7` → `claude-opus-4-8` に更新
- ハーネスバージョン v0.2 → v0.3


## [0.0.2] - 2026-04-30

### Added
- Claude Designによる画面設計
- 3ツール協調フロー(ClaudeCode → ClaudeDesign → ClaudeCode → 実装)に対応
- `WORKFLOW.md` を新設(Mermaid によるグラフィカルな全体図)
- `output/_handoff_to_claude_design/`(Phase 1 → Phase 2 引き渡しパッケージ用)
- `output/04_画面設計_from_ClaudeDesign/`(ClaudeDesign 成果物受け入れ)

### Changed
- `output/04_詳細設計/` → `output/05_詳細設計/` に繰り下げ(画面設計の場所を空けるため)
- `harness/01_selection_rules.md` に `担当`(CC1 / CC1-P3 / CD)・`画面影響` 列を追加
- `harness/02_workflow.md` を 4 フェーズ構成に再編
- `harness/03_quality_checklist.md` に Phase 1→2 引き渡し / Phase 2→3 取り込みチェックを追加
- `harness/templates/_index.md` で B-7, B-8 を「ClaudeDesign 委譲」マークに
- ハーネスバージョン v0.1 → v0.2


## [0.0.1] - 2026-04-01

### Added
- 初回リリース

[Unreleased]: https://github.com/username/project/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/username/project/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/username/project/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/username/project/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/username/project/releases/tag/v1.0.0