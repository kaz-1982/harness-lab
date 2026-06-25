# harness-lab

**Claude Code 用の「ハーネス」を集めたリポジトリ**です。

ここでいう **ハーネス** とは、`CLAUDE.md`（運用ルール）＋ `harness/`（手順書）＋ `templates/`（雛形）をひとまとめにし、\
特定の知的作業を Claude Code に **「毎回同じ品質で」** 実行させるための仕組みを指します \
案件・テーマごとにフォルダをコピーして使い、対話しながら成果物を `output/` に生成します

---

## 収録ハーネス

| ハーネス | 目的 | 主な成果物 | 詳細 |
|---|---|---|---|
| [**問題解決FW**](問題解決FW/README.md) | 抱えている問題を、原因（Why）と対応策（How）に MECE で整理する | 問題定義・原因ツリー・対応策ツリー・アクションプラン（Markdown ＋ drawio 図） | [README](問題解決FW/README.md) ／ [ChangeLog](問題解決FW/ChangeLog.md) |
| [**開発doc作成**](開発doc作成/README.md) | システム開発の設計ドキュメントを案件特性に応じて選定・生成する（WF / アジャイル / ハイブリッド対応） | 要件定義・基本設計・詳細設計・テスト仕様 等（テンプレ準拠 ＋ 整合性チェック） | [README](開発doc作成/README.md) ／ [ChangeLog](開発doc作成/ChangeLog.md) |

> 各ハーネスは独立して完結しています。使うときは、そのハーネスのフォルダ単位でコピーして利用してください。

---

## 共通コンセプト

- **コピーして使う** — ハーネス本体は直接編集せず、案件・テーマごとにフォルダを複製してワークスペースにする。
- **対話・プロファイル駆動** — 最初に Claude が質問（インテーク）し、その回答に基づいて作るものを機械的に決める。
- **成果物は `output/` に集約** — 生成物は必ず `output/` 配下に保存される。
- **図は drawio** — ロジックツリーや設計図は `.drawio` / `.drawio.svg` を正本とし、Markdown から参照する。
- **Opus 運用前提** — 推論品質が成果物の質に直結するため、`claude-opus-4-8`（Opus）での利用を推奨。

---

## 使い方（共通の流れ）

```sh
# 1. 使いたいハーネスのフォルダをコピーして、案件ワークスペースにする
cp -r 問題解決FW/ ~/work/離職率の問題/      # 例：問題解決FW
#   または
cp -r 開発doc作成/ ~/work/案件A/             # 例：開発doc作成

# 2. そのフォルダで Claude Code を起動（Opus 推奨）
cd ~/work/案件A/
claude --model claude-opus-4-8

# 3. トリガーを伝える
#   問題解決FW   →「問題解決プロセスを始めて」
#   開発doc作成  →「インテーク開始」
```

あとは Claude の質問に答え、生成されたドキュメント／図にコメントしながら進めます。
詳しい流れは各ハーネスの README を参照してください。

---

## リポジトリ構成

```
harness-lab/
├── README.md            # このファイル
├── .gitignore
├── 問題解決FW/          # ハーネス①：問題解決（Why/How ロジックツリー）
│   ├── CLAUDE.md        #   Claude 向け運用ルール
│   ├── README.md
│   ├── harness/         #   手順書・テンプレート
│   ├── input/  output/  #   入力資料 / 成果物
│   └── WORKFLOW.*       #   全体フロー図
└── 開発doc作成/         # ハーネス②：開発ドキュメント生成
    ├── CLAUDE.md        #   Claude 向け運用ルール
    ├── README.md
    ├── harness/         #   手順書・テンプレート・整合性チェック（tools/check.py）
    ├── input/  output/  #   原典・事前検討資料 / 成果物
    └── WORKFLOW.md      #   3ツール協調フロー図
```

---

## 動作前提

- [Claude Code](https://www.claude.com/product/claude-code) が利用可能であること
- 各ハーネスのフォルダのルートで `claude` を起動すること（`CLAUDE.md` を読み込ませるため）
- モデルは **Opus（`claude-opus-4-8`）** を推奨
- drawio 図を編集・表示する場合は [draw.io デスクトップ](https://www.drawio.com/) ／ [diagrams.net](https://app.diagrams.net/) ／ VS Code 拡張「Draw.io Integration」のいずれか

---

## ライセンス / 利用について

個人の作業用ハーネスとして管理しているリポジトリです。
（公開・再利用の方針が決まり次第、`LICENSE` を追加してください。）
