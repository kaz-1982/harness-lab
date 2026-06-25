# harness/tools — 検証スクリプト

ハーネスの整合性を機械的に検証するツール群。**read-only**(`--tbd` 指定時のみ `_tbd_dashboard.md` を生成)。

## check.py — 整合性チェック

### 使い方
```sh
python3 harness/tools/check.py [OUTPUT_DIR]              # 検証のみ。既定: ./output
python3 harness/tools/check.py --tbd [OUTPUT_DIR]        # 検証 + TBD ダッシュボードを _tbd_dashboard.md に出力
python3 harness/tools/check.py --help
```
- 問題があれば終了コード 1、なければ 0(ディレクトリ不在は 2)。CI やコミット前フックにも組み込める。
- Python 3 標準ライブラリのみ(追加インストール不要)。
- Windows でも CP932 端末で ✅ / ❌ を正しく表示する(stdout を UTF-8 にリコンフィグ)。

### 検証する項目(自動)
| 種別 | 内容 |
|---|---|
| 構造 | 各ドキュメントの frontmatter 必須キー(doc_id/phase/depends_on/mode)+ セクション 1〜7(`templates/_format.md` 準拠) |
| ID整合 | 本文のインスタンスID参照(`F-001` / `AG-001` 集約 / `VO-001` 値オブジェクト 等)が `_id_registry.md` に登録済か / 重複 / プレフィクス・桁数規則 |
| 状態突合 | 各ドキュメントの doc_id が `_doc_plan.md` に存在するか |
| 孤立検出 | R-14 RTM が存在するとき、登録済 `R-B-*` / `R-F-*` / `F-*` が RTM の **表セル** に出現するか。出現しないものは孤立要件 / 孤立機能の可能性として警告(v0.8〜) |
| AC/AT 網羅 | TS-1 受け入れテスト仕様書が存在しかつ `AT-*` が定義されているとき、登録 `R-F-*` が TS-1 の **表セル** で参照されているか。未参照は AT-* 漏れの可能性(v0.8〜) |
| ファイル名整合 | ファイル名先頭の doc_id(`R-1_xxx.md` → "R-1")と frontmatter `doc_id` の一致(v0.9〜)。リネーム事故の検出 |
| 依存検証 | frontmatter `depends_on` の各IDが `_doc_plan.md` に存在し、本書が「進行中以上」のとき依存先が「承認済」相当(承認済 / 取り込み済 / ゲート2承認 / 蓄積中)になっているか(v0.9〜)。Step B「依存関係確認」の機械化 |
| ADR 突合 | `output/横断/ADR/` が存在する案件で、ADR ファイル群と `_index.md` の突合(索引漏れ / 索引のゴースト / `status` 未記入を検出 / v0.9〜) |

> **対象外**: `output/横断/ADR/` 配下(ADR アーキテクチャ決定記録)は MADR 形式で標準構造(セクション 1〜7)を持たないため、構造・状態突合の検証対象外(`EXCLUDE_DIRS` で除外)。`_` 始まりの管理ファイル・README・project_profile も従来どおり対象外。
>
> **誤検出回避**: 孤立検出 / AC/AT 網羅 は本文の地の文ではなく **表セル限定** で ID を抽出する(コメント・解説文に偶然 ID が出ても誤検出しない)。R-14 / TS-1 そのものが無い案件ではスキップ(RTM 省略・TDD 不採用は問題ではない)。

### TBD ダッシュボード(`--tbd` 指定時)
- 全ドキュメント本文・各 `## 7. レビュー状態` セクション・`project_profile.md` の「TBD / 保留中の項目」を集約
- 出力先: `OUTPUT_DIR/_tbd_dashboard.md`(自動生成、手動編集禁止)
- 検証は失敗しない(あくまで集約。問題の検出ではない)
- 完了判定前に実行し、取り残しの TBD が無いことを確認する用途

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
python3 harness/tools/check.py harness/tools/fixtures/sample_ok       # → ✅ 緑 / exit 0
python3 harness/tools/check.py harness/tools/fixtures/sample_ng       # → ❌ 6件検出 / exit 1
python3 harness/tools/check.py harness/tools/fixtures/sample_orphan   # → ❌ 3件検出(孤立検出×2 + AC/AT網羅×1)/ exit 1
python3 harness/tools/check.py harness/tools/fixtures/sample_v09      # → ❌ 5件検出(ファイル名×1 + 依存×1 + ADR×3)/ exit 1
```
- `sample_ng`: 未登録ID参照 / ID重複 / frontmatter キー欠落 / セクション欠落 / doc_plan 未登録 を意図的に仕込んだ異常系(構造・ID整合・状態突合)
- `sample_orphan`: R-14 RTM の表に `R-F-002` / `F-001` を載せず、TS-1 の表に `R-F-002` を載せない異常系(孤立検出 / AC/AT 網羅 / v0.8〜)
- `sample_v09`: R-2_*.md の frontmatter doc_id を R-1 にずらし、R-7(進行中)が R-13(未着手)に depends_on、ADR-0001 の status 未記入 / ADR-0099 ゴースト / ADR-0003 索引漏れ を仕込んだ異常系(ファイル名整合 / 依存検証 / ADR 突合 / v0.9〜)

### Git pre-commit フック(v0.9〜)

コミット前に check.py を自動実行し、整合性エラーがあればコミットを中断する仕組みを同梱。

```sh
bash harness/tools/install-hooks.sh    # .git/hooks/pre-commit に導入(初回のみ)
```

導入後の挙動:

- `output/` 配下のファイルが staging に含まれているコミットでのみ check.py を実行(ハーネス本体のみの変更時はスキップ)
- 整合性エラーがあればコミット中断、緑なら通過
- 一時バイパス: `git commit --no-verify`(推奨しない)
- 既存のフックがある場合は `.bak.YYYYMMDD...` として退避する

実体は `harness/tools/hooks/pre-commit`。シンボリックリンクが使えない環境(Windows 等)では `install-hooks.sh` が自動的にコピーへフォールバックする。

### 拡張方針(今後の候補)
- 用語整合(`R-13` 用語集の登録語の表記揺れ検出)
- DM-1 の集約(`AG-`)・値オブジェクト(`VO-`)・エンティティ(`E-`)と B-12 / B-13 の整合
- `_handoff_to_implementation/_test_manifest.md` と TS-1 / D-15 の `UT-` / `AT-` 突合(Phase 3.5 ゲート2の補強)
- depends_on の循環検出(現状は直接参照のみチェック)
