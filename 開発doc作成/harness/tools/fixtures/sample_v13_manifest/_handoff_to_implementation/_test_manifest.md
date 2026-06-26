# テストマニフェスト(サンプル・突合検査 / v0.13)

> 意図的に UT-002 を載せず(掲載漏れ)、AT-999 を載せる(ゴースト)。

## 2. 単体テスト(UT-* / D-15 由来)

| テストID | テストファイル | 対象モジュール | 対応要件/設計 | 状態 |
|---|---|---|---|---|
| UT-001 | tests/unit/test_register.py::test_ok | UserService.register | R-F-001 | Red |

## 3. 受け入れテスト(AT-* / TS-1 由来)

| テストID | テストファイル | シナリオ | 対応要件/AC | 状態 |
|---|---|---|---|---|
| AT-001 | tests/acceptance/test_csv.py::test_ok | CSV 出力 | R-F-001 | Red |
| AT-999 | tests/acceptance/test_ghost.py::test_x | 定義のないテスト | R-F-001 | Red |
