# 成果物ディレクトリ

`harness/01_selection_rules.md` で選定されたドキュメントが、フェーズ別にここに格納されます。

3ツール協調フローの全体像は [../WORKFLOW.md](../WORKFLOW.md) を参照。

---

## ファイル

| ファイル | 役割 | 作成タイミング |
|---|---|---|
| `project_profile.md` | 案件プロファイル(インテーク結果) | 起動直後のインテークで作成 |
| `_doc_plan.md` | 作成対象ドキュメントの計画と進捗 | プロファイル確定後に生成 |
| `_id_registry.md` | ID採番台帳(機能・画面・API・エンティティ等)。書式は CLAUDE.md「3. ID体系の一貫性」参照 | 最初のID採番時に作成 |
| `_review_log.md` | レビュー実施ログ | 最初のレビュー時に作成 |

## サブディレクトリ

| ディレクトリ | 格納するもの | フェーズ |
|---|---|---|
| `00_事前検討/` | PR-1 事前検討サマリ(`input/事前検討資料/` に資料がある案件のみ) | Phase 0(任意) |
| `01_企画/` | P-1〜P-3 | Phase 1 |
| `02_要件定義/` | R-1〜R-12, R-14, R-15 | Phase 1 |
| `03_基本設計/` | B-1〜B-19(B-7, B-8 を除く) | Phase 1 + Phase 3 |
| `_handoff_to_claude_design/` | ClaudeDesign 向け引き渡しパッケージ | Phase 1 完了時に生成 |
| `04_画面設計_from_ClaudeDesign/` | ClaudeDesign 成果物(B-7, B-8, モック) | Phase 2 完了時にユーザーが配置 |
| `05_詳細設計/` | D-1〜D-15 + TS-1 受け入れテスト仕様(TDD採用時) | Phase 3 + Phase 3.5 |
| `_handoff_to_implementation/` | 実装向け引き渡し(Red テスト + マニフェスト) | Phase 3.5 完了時に生成(TDD採用時) |
| `横断/` | R-13 用語集、R-14 RTM、R-15 ステークホルダー一覧、DM-1 ドメインモデル(DDD採用時) | 全 Phase |
| `横断/ADR/` | ADR アーキテクチャ決定記録(随時蓄積)+ `_index.md` 索引 | 全 Phase(意思決定のたび) |
| `sprint_NN/` | (アジャイル運用時のみ)スプリントごとの増分成果物 | 全 Phase |

---

## 命名規約

- ドキュメントファイル名は `harness/templates/_index.md` の「ファイル名(予定)」列に準拠
- アンダースコア区切り、日本語可
- 例: `02_要件定義/R-1_業務要件定義書.md`

---

## 案件着手前の状態

骨組みコピー直後は、このディレクトリには以下があります:
- `project_profile.md`(空テンプレ)
- `README.md`(このファイル)
- `_handoff_to_claude_design/README.md`(引き渡しパッケージ仕様)
- `04_画面設計_from_ClaudeDesign/README.md`(取り込み仕様)
- `_handoff_to_implementation/README.md`(実装引き渡し仕様 / TDD採用時に使用)

なお、要件定義の前に「問題・原因・対応策」を検討した資料がある案件では、`input/事前検討資料/` に資料を投入しておくと、インテーク前の Phase 0 でそれを読み込み `00_事前検討/PR-1_事前検討サマリ.md` を生成します(資料が無い案件はスキップ)。

インテーク完了後、Claude が必要なファイルとサブディレクトリを順次作成していきます。Phase 1 完了時に `_handoff_to_claude_design/` 配下が生成され、Phase 2 完了時にユーザーが `04_画面設計_from_ClaudeDesign/` に成果物を配置します。テスト戦略 = TDD の案件では、Phase 3.5 完了時に `_handoff_to_implementation/` 配下(Red テスト)が生成されます。
