# Changelog

このハーネス自身の改修記録。フォーマットは [Keep a Changelog](https://keepachangelog.com/ja/1.1.0/) 準拠。

変更カテゴリ: Added(新機能) / Changed(変更) / Deprecated / Removed / Fixed / Security

## [0.3.0] - 2026-06-27

### Added
- **入力設定ファイル `input/config.md`** を新設。APP_DIR / DOC_DIR(+ 案件名 / SCOPE / OUT / CANONICAL / メモ)を記入しておけば、起動時に Claude が読んで入力を確定する。リポジトリに残るので**再現性**がある(同じ案件の再実行が容易)。
- 入力の**優先順**を明文化(`CLAUDE.md` 起動時の挙動 / `harness/00_inputs.md`): ①会話での明示指定 > ②`input/config.md` > ③質問。

## [0.2.0] - 2026-06-27

### Added
- **並行サブエージェント方式**を正式採用。`harness/agents/` に役割定義を新設:
  - `code-inventory` / `doc-inventory`(読み取り専用の棚卸し)
  - `drift-detector`(**ID種別ごと**にファンアウトする検出。A-/T-/F-/UT- 等)
  - `doc-reconciler`(**担当docごと**に並列で追従修正)
  - `agents/README.md` にロスターと「暴走防止の3制約」(書き込み1ファイル1オーナー / 自己完結プロンプト / 検証は親で集約)。
- `harness/02_workflow.md` の **R2 に「ID種別ファンアウト」**、**R4 に「doc単位ファンアウト」** のレシピを追記(並列の境界・書き込みオーナー・新規ID採番の順序)。
- 各役割は Claude Code のカスタムエージェント定義(frontmatter `name`/`description`/`tools`)としてそのまま `.claude/agents/` に置ける形式。案件固有(APP_DIR/DOC_DIR/担当ID)はプロンプト引数で注入する設計。

## [0.1.0] - 2026-06-27

### Added
- 初版。**実装↔ドキュメント整合(逆同期)ハーネス**を新設。先に動いている実装と設計ドキュメントの乖離を、**コードを正**として解消する案件非依存の後工程ハーネス。
- **2ディレクトリ入力**(APP_DIR=実装 / DOC_DIR=設計doc)で起動する契約(`harness/00_inputs.md`)。ID体系を持つ生成ハーネス成果物・素のドキュメント群の双方に対応。
- 手順 `harness/02_workflow.md`(R0 入力確定 → R1 トリアージ → R2 ドリフト検出 → R3 影響波及 → R4 修正 → R5 検証)。
- ドキュメント区分マトリクス `harness/01_triage.md`(据え置き=要件・方式アーキ / 要確認=機能一覧・論理データ・セキュリティ / 修正必須=詳細設計のロジック・IF / スキーマ突合=物理データ・DDL / 変わった分=シーケンス・状態遷移 / 追従=テスト)。乖離種別(追加/変更/削除/方式差/逆未実装)。
- 手動観点 `harness/03_quality_checklist.md`、ドリフトレポート雛形 `harness/templates/_drift_report.md`。

### 背景
- DietSupport 案件(`007_DietSupport`)で、実装後の改善(記録の全削除追加・uuidフォールバック・間食追加・サーバーの汎用同期ストア化・認証トークン実体)により設計docが乖離。当初は生成ハーネスの案件コピー内に Phase 5 として手順を埋め込んだが、**「実装dirと設計dirの2つを入力に整合を取る独立ツール」**として切り出すべきと判断し、本ハーネスを新設。生成ハーネス側に入れた手順ファイルは撤去した。
