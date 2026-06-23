# テストコード生成規約(Phase 3.5 / TDD採用時)

Phase 3.5-② で生成する **Red テストコード** の言語非依存の規約。テスト戦略 = TDD の案件でのみ使用する。全体フローは [../../WORKFLOW.md](../../WORKFLOW.md) §7.5、手順は [../02_workflow.md](../02_workflow.md) §9.5 を参照。

---

## 1. 入口ガード(必須)

テストコードを生成する前に、以下を満たすこと。満たさなければ生成せず、ユーザーに確認する(CLAUDE.md ルール7「推測で埋めない」):

- [ ] `output/project_profile.md` の「テスト戦略 = TDD」
- [ ] 技術スタック(言語)とテストフレームワークが `project_profile.md` で確定(TBD 不可)
- [ ] ゲート1(D-15 / TS-1 のテスト仕様)が承認済

**技術スタックを推測してコードを書いてはならない。** 未確定なら確認が先。

---

## 2. 技術スタック → テストフレームワーク対応(既定候補)

`project_profile.md` の指定を最優先。指定が「言語のみ」の場合の既定候補:

| 言語 | 単体テスト | 受け入れ / E2E |
|---|---|---|
| Java / Kotlin | JUnit5 + Mockito | Cucumber-JVM / REST Assured |
| TypeScript / JS | Vitest / Jest | Playwright / Cypress |
| Python | pytest | behave / Playwright(python) |
| Ruby | RSpec | RSpec feature / Capybara |
| Go | testing + testify | — |
| C# | xUnit + Moq | SpecFlow |

候補はあくまで既定。プロファイルに明示があればそれに従う。

---

## 3. 配置先とディレクトリ構成

```
output/_handoff_to_implementation/
├── README.md           # 実装リポジトリ向け Green 化手順
├── tests/
│   ├── unit/           # D-15 由来。UT-* に対応
│   └── acceptance/     # TS-1 由来。AT-* に対応
└── _test_manifest.md   # UT/AT ↔ テストファイル ↔ 要件 の対応表
```

実装は別リポジトリで行うため、テストコードは「実装リポジトリへの引き渡し物」として上記に置く。ハーネスの `output/` に実装コードは置かない。

---

## 4. 命名規則(テストID ↔ コードの対応)

テストケースID(`UT-*` / `AT-*`)とテストコードを **機械的に対応** させる:

- ファイル名 or テストケース名に ID を含める。例:
  - 単体: `test_UT_001_amount_calc_normal()` / `describe('UT-001 金額計算 正常系')`
  - 受け入れ: `AT-001: CSV出力 正常系`(Gherkin の Scenario 名等)
- 1つの `UT-*` / `AT-*` に対し最低1つのテスト関数。`_test_manifest.md` に対応を記録。

---

## 5. Red 状態の定義(重要)

Phase 3.5-② で生成するテストは **必ず Red(失敗)** であること:

- **コンパイル / 解釈は通る**(構文エラーで落ちるのは Red ではない)
- 対象実装が未存在なら、**期待結果のアサーションで fail** する状態にする(未実装スタブを呼ぶ、または明示的に `fail("not implemented")`)
- 全テストを実行し、**Red であることを確認した実行ログ**を `output/_review_log.md` に添付(ゲート2の完了基準)
- skip / pending で「緑に見せかける」ことは禁止。未実装は fail として可視化する

---

## 6. Phase 4(実装)への引き継ぎ

- 実装リポジトリは `tests/` を取り込み、**テストを Green にする形で実装**する(テストを後から都合よく書き換えない)
- テスト変更が必要な場合(仕様変更・テスト誤り)は、ハーネスに戻って D-15 / TS-1 を改訂し、ゲートを再通過させる
- `_test_manifest.md` を更新し、要件 ⇄ テスト ⇄ 実装のトレーサビリティを保つ

---

## 7. `_test_manifest.md` のフォーマット

```markdown
# テストマニフェスト(UT/AT ↔ ファイル ↔ 要件)

| テストID | テストファイル | テスト名 | 対応要件/設計 | 種別 | Red確認 |
|---|---|---|---|---|---|
| UT-001 | tests/unit/amount_calc_test.xx | UT_001_normal | D-12 金額計算 / F-010 | 単体 | ✅ |
| AT-001 | tests/acceptance/csv_export.feature | AT-001 CSV出力 正常系 | R-7 US-03 の AC / F-010 | 受け入れ | ✅ |
```
