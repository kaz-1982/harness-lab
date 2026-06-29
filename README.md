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
| [**実装vsDoc整合確認**](実装vsDoc整合確認/README.md) | 先に動いている実装（コード）を正として、古くなった設計ドキュメントの乖離（ドリフト）を解消する。「開発doc作成」の後工程 | ドリフト検出レポート（ID単位の差分表）・コードに追従修正した設計doc | [README](実装vsDoc整合確認/README.md) ／ [ChangeLog](実装vsDoc整合確認/ChangeLog.md) |

> 各ハーネスは独立して完結しています。**問題解決FW** と **開発doc作成** はフォルダ単位でコピーして使い、**実装vsDoc整合確認** は実装/設計の 2 ディレクトリを指定して回します（下記「使い方」参照）。

---

## 共通コンセプト

- **コピーして使う** — ハーネス本体は直接編集せず、案件・テーマごとにフォルダを複製してワークスペースにする（実装vsDoc整合確認 は例外。コピーせず、対象の 2 ディレクトリを `input/config.md` か会話で指定する）。
- **対話・プロファイル駆動** — 最初に Claude が質問（インテーク）し、その回答に基づいて作るものを機械的に決める。
- **成果物は所定フォルダに集約** — 生成物は `output/`（問題解決FW・開発doc作成）または `runs/`（実装vsDoc整合確認）配下に保存される。
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

**実装vsDoc整合確認** はコピーせず、このハーネスのフォルダで Claude を起動して使います。

```sh
# 1. 実装と設計の 2 ディレクトリを input/config.md に記入（APP_DIR / DOC_DIR を絶対パスで）
#    または起動後に会話で「APP_DIR=… / DOC_DIR=… の整合を取って」と伝える
cd 実装vsDoc整合確認/
claude --model claude-opus-4-8

# 2. トリガーを伝える →「整合を取って（コードを正に）」
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
├── 開発doc作成/         # ハーネス②：開発ドキュメント生成
│   ├── CLAUDE.md        #   Claude 向け運用ルール
│   ├── README.md
│   ├── harness/         #   手順書・テンプレート・整合性チェック（tools/check.py）
│   ├── input/  output/  #   原典・事前検討資料 / 成果物
│   └── WORKFLOW.md      #   3ツール協調フロー図
└── 実装vsDoc整合確認/    # ハーネス③：実装↔設計doc の整合（コードを正に逆同期）
    ├── CLAUDE.md        #   Claude 向け運用ルール
    ├── README.md
    ├── harness/         #   手順書・並行サブエージェント定義・テンプレート
    ├── input/config.md  #   ★ APP_DIR / DOC_DIR を指定する設定ファイル
    └── runs/            #   ドリフト検出レポート等の成果物
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
