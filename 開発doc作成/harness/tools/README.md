# harness/tools — 検証スクリプト

ハーネスの整合性を機械的に検証するツール群。**read-only**(ファイルを修正しない)。

## check.py — 整合性チェック(最小版)

### 使い方
```sh
python3 harness/tools/check.py [OUTPUT_DIR]   # 既定: ./output
python3 harness/tools/check.py --help
```
- 問題があれば終了コード 1、なければ 0(ディレクトリ不在は 2)。CI やコミット前フックにも組み込める。
- Python 3 標準ライブラリのみ(追加インストール不要)。

### 検証する項目(自動)
| 種別 | 内容 |
|---|---|
| 構造 | 各ドキュメントの frontmatter 必須キー(doc_id/phase/depends_on/mode)+ セクション 1〜7(`templates/_format.md` 準拠) |
| ID整合 | 本文のインスタンスID参照(`F-001` / `AG-001` 集約 / `VO-001` 値オブジェクト 等)が `_id_registry.md` に登録済か / 重複 / プレフィクス・桁数規則 |
| 状態突合 | 各ドキュメントの doc_id が `_doc_plan.md` に存在するか |

> **対象外**: `output/横断/ADR/` 配下(ADR アーキテクチャ決定記録)は MADR 形式で標準構造(セクション 1〜7)を持たないため、構造・状態突合の検証対象外(`EXCLUDE_DIRS` で除外)。`_` 始まりの管理ファイル・README・project_profile も従来どおり対象外。

### 検証しない項目(手動レビュー)
- 要件が業務的に正しいか、期待結果が妥当かなどの **意味の妥当性**
- → `harness/03_quality_checklist.md` の手動観点で人/AI が確認する

**機械チェックが緑でも「意味的に正しい」ことは保証されません。** 自動(check.py)+ 手動(checklist)の2層で運用してください。

### 前提となるファイル形式
- `_id_registry.md`: CLAUDE.md「3. ID体系の一貫性」の表形式
- `_doc_plan.md`: `01_selection_rules.md` の出力フォーマット(表)
- 各ドキュメント: `templates/_format.md` の標準構造(frontmatter + セクション 1〜7)

### 自己検証(フィクスチャ)
```sh
python3 harness/tools/check.py harness/tools/fixtures/sample_ok   # → ✅ 緑 / exit 0
python3 harness/tools/check.py harness/tools/fixtures/sample_ng   # → ❌ 6件検出 / exit 1
```
`sample_ng` には「未登録ID参照 / ID重複 / frontmatter キー欠落 / セクション欠落 / doc_plan 未登録」を意図的に仕込んである。

### 拡張方針(今後の候補)
- 孤立検出(RTM / トレーサビリティ欄から「設計のない要件」「要件のない機能」)
- Phase 3.5: `UT-`/`AT-` ↔ `_handoff_to_implementation/_test_manifest.md` の突合、全 AC に受け入れケースがあるか
- 用語整合(`R-13` 用語集の登録語の表記揺れ検出)
- ADR 索引(`output/横断/ADR/_index.md`)と ADR ファイル群の突合(索引漏れ・status 未記入の検出)
- DM-1 の集約(`AG-`)・値オブジェクト(`VO-`)・エンティティ(`E-`)と B-12 / B-13 の整合
