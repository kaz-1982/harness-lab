# ハーネス主要ファイル一覧

ハーネスを構成する主要ファイルの役割と改変ポリシーの参照表。
このファイル自体は索引であり、各ファイルの内容は実体ファイルに記載されている。

> CLAUDE.md からはこの一覧へリンクで参照する(以前は CLAUDE.md 本体に同じ表があったが、v0.9 でスリム化のため分離)。

## 原典 / 入力

| パス | 役割 | 改変可否 |
|---|---|---|
| `input/システム開発設計ドキュメント一覧.md` | ドキュメント定義の原典 | **改変禁止** |
| `input/事前検討資料/` | 事前検討資料の投入先(Phase 0 / 任意)。ユーザーが「問題・原因・対応策」資料を配置 | ユーザーが配置(許可拡張子のみ。`README.md` 参照) |

## ハーネス本体(`harness/`)

| パス | 役割 | 改変可否 |
|---|---|---|
| `harness/00_intake.md` | インテーク質問票(§0-1 に Phase 0 のトリガ allowlist) | ハーネス改善時のみ改変 |
| `harness/01_selection_rules.md` | プロファイル → 作成ドキュメント選定ルール | ハーネス改善時のみ改変 |
| `harness/02_workflow.md` | フェーズ進行手順(Claude の実行手順) | ハーネス改善時のみ改変 |
| `harness/03_quality_checklist.md` | 品質・整合性チェック観点(手動) | ハーネス改善時のみ改変 |
| `harness/_files_overview.md` | 主要ファイル一覧(本ファイル) | ハーネス改善時のみ改変 |

## テンプレート(`harness/templates/`)

| パス | 役割 | 改変可否 |
|---|---|---|
| `harness/templates/_format.md` | テンプレ共通フォーマット規約 | ハーネス改善時のみ改変 |
| `harness/templates/_index.md` | テンプレ一覧と生成方針(✅事前同梱 / ⬜遅延生成) | テンプレ追加時に更新 |
| `harness/templates/_test_code_convention.md` | テストコード生成規約(言語非依存 / TDD 時) | ハーネス改善時のみ改変 |
| `harness/templates/{doc_id}_*.md` | 各ドキュメントのテンプレ(原典準拠 + ハーネス拡張) | 必要時に input から生成 |
| `harness/templates/PR-1_事前検討サマリ.md` | 事前検討サマリのテンプレ(原典外・ハーネス拡張) | ハーネス改善時のみ改変 |
| `harness/templates/DM-1_ドメインモデル.md` | ドメインモデルのテンプレ(原典外・ハーネス拡張 / DDD) | ハーネス改善時のみ改変 |
| `harness/templates/ADR-NNNN_アーキテクチャ決定記録.md` | ADR のテンプレ(原典外・ハーネス拡張 / MADR 形式) | ハーネス改善時のみ改変 |

## ツール(`harness/tools/`)

| パス | 役割 | 改変可否 |
|---|---|---|
| `harness/tools/check.py` | 整合性検証スクリプト(構造 / ID / 状態 / 孤立 / AC-AT / ファイル名 / 依存 / ADR / TBD 集約) | ハーネス改善時のみ改変 |
| `harness/tools/README.md` | check.py の使用法 | ハーネス改善時のみ改変 |
| `harness/tools/fixtures/` | check.py の自己検証 fixture(sample_ok / sample_ng / sample_orphan / sample_v09 / sample_v10_glossary / sample_v10_cycle) | ハーネス改善時のみ改変 |
| `harness/tools/hooks/pre-commit` | Git pre-commit フックサンプル(v0.9〜) | ハーネス改善時のみ改変 |
| `harness/tools/install-hooks.sh` | `.git/hooks/` に pre-commit を導入(v0.9〜) | ハーネス改善時のみ改変 |
| `harness/tools/new-project.sh` | 新規案件用にハーネス本体をコピー(v0.10〜) | ハーネス改善時のみ改変 |

## 案件成果物(`output/`)

| パス | 役割 | 改変可否 |
|---|---|---|
| `output/project_profile.md` | 案件プロファイル(インテーク結果) | 案件中、随時更新 |
| `output/_doc_plan.md` | 作成計画と進捗(選定結果) | ドキュメント完了の都度更新 |
| `output/_id_registry.md` | ID採番台帳(`check.py` が parse する正本) | 新ID採番の都度更新 |
| `output/_review_log.md` | レビュー実施ログ | チェック実施の都度追記 |
| `output/_tbd_dashboard.md` | TBD ダッシュボード(`check.py --tbd` が自動生成) | 自動生成(手動編集禁止) |
| `output/00_事前検討/` | Phase 0 の成果物(PR-1)/ 資料投入時のみ | Phase 0 で生成 |
| `output/01_企画/` / `02_要件定義/` / `03_基本設計/` / `05_詳細設計/` | 成果物格納先 | 自由(テンプレ準拠) |
| `output/横断/` | 横断ドキュメント(R-13 用語集 / R-14 RTM / DM-1 ドメインモデル / R-15 ステークホルダー 等) | 自由(テンプレ準拠) |
| `output/横断/ADR/` | ADR(アーキテクチャ決定記録)格納先。索引は `_index.md` | 随時生成(意思決定のたび) |

## 引き渡しパッケージ(`output/_handoff_*`)

| パス | 役割 | 改変可否 |
|---|---|---|
| `output/_handoff_to_claude_design/` | Phase 2 への引き渡しパッケージ(仕様は [WORKFLOW.md §6](../WORKFLOW.md))| Phase 1 完了時に生成 |
| `output/04_画面設計_from_ClaudeDesign/` | ClaudeDesign の成果物受け取り(仕様は [WORKFLOW.md §7](../WORKFLOW.md))| ユーザーが配置 / Phase 3 で参照 |
| `output/_handoff_to_implementation/` | Phase 4 への引き渡しパッケージ(Red テスト + 設計参照)| Phase 3.5 完了時に生成(TDD採用時) |

## ルート / ドキュメント

| パス | 役割 | 改変可否 |
|---|---|---|
| `CLAUDE.md` | Claude 向け運用ルール(最重要) | ハーネス改善時のみ改変 |
| `README.md` | プロジェクト README(人間向け) | ハーネス改善時のみ改変 |
| `WORKFLOW.md` | 全体ワークフロー(図と仕様の参照) | ハーネス改善時のみ改変 |
| `ChangeLog.md` | ハーネス本体の改修履歴 | ハーネス改修時に追記 |
| `.harness-source` | ハーネス本体(マスター)を示すマーカー(v0.10〜)。案件コピーには存在しない | 編集禁止 |

## 学習用(`examples/`)

| パス | 役割 | 改変可否 |
|---|---|---|
| `examples/README.md` | golden sample の説明と使い方(v0.10〜) | ハーネス改善時のみ改変 |
| `examples/sample_case/` | 小規模アジャイル案件の最小完成版(v0.10〜)。`check.py` で **緑** | ハーネス改善時のみ改変 |
