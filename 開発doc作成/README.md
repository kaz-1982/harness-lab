# システム開発ドキュメント生成ハーネス

システム開発で必要となる設計ドキュメントを **「毎回同じ品質」** で生成するための、\
Claude Code 用ハーネスです

ウォーターフォール / アジャイル / ハイブリッドの3形態に対応し、\
案件特性に応じて作成すべきドキュメントを自動選定します。

---

## 3ツール協調フロー

このハーネスは \
**(任意)事前検討 → 要件・設計 → 画面設計 → 詳細設計 →(TDD採用時)テスト具体化 → 実装** のフェーズを 3ツールで分担して進めます(全体図: [WORKFLOW.md](WORKFLOW.md))\
Phase 0(事前検討の取り込み)は `input/事前検討資料/` に資料が投入された案件でのみ、\
Phase 3.5(テスト具体化 + レビューゲート)は「テスト戦略 = TDD」の案件でのみ発動します。

| Phase | 担当 | 主成果物 |
|---|---|---|
| 0. 事前検討の取り込み(任意 / 資料投入時のみ) | **ClaudeCode (このハーネス)** | PR-1 事前検討サマリ |
| 1. 要件定義 + 基本設計(画面以外) | **ClaudeCode (このハーネス)** | R-*, B-* (B-7, B-8 を除く), DM-1(DDD採用時), ADR(随時) |
| 2. 画面設計 | **ClaudeDesign** | B-7, B-8 + 画面モック |
| 3. 詳細設計 + 画面影響B-*の確定 | **ClaudeCode (このハーネス)** | D-*, B-6/B-11/B-14/B-19 更新 |
| 3.5. テスト具体化 + レビューゲート(TDD採用時) | **ClaudeCode (このハーネス)** | D-15 最終化, TS-1, Red テストコード |
| 4. 実装 | **ClaudeCode (実装、別リポジトリ)** | アプリケーションコード(テストを Green 化) |

---

## 想定する使い方

1. **案件ごとにこのディレクトリ全体をコピー** して、案件ワークスペースを作る

   v0.10〜 は専用スクリプトを推奨(`examples/` 等を自動除外):

   ```sh
   bash harness/tools/new-project.sh ~/projects/案件A
   cd ~/projects/案件A/
   ```

   従来通り手動でコピーしても可:

   ```sh
   cp -r doc_harness/ projects/案件A/
   cd projects/案件A/
   rm -f .harness-source        # 案件側ではマーカーを削除
   rm -rf examples              # 案件には学習用 examples/ は不要
   ```

2. **(任意)事前検討資料があれば `input/事前検討資料/` に投入する**

   「問題 → 原因 → 対応策」を検討した資料(議事録、メモ、スライド、画像、PDF等、形式自由)を1つ以上配置すると、Phase 0 が発動し、要件定義に入る前にハーネスがその資料を読み込み・正規化して `output/00_事前検討/PR-1_事前検討サマリ.md` を生成します。\
   資料が無い案件ではこの手順をスキップしてください(そのままインテークから始まります)。

3. ワークスペース内で `claude` を起動

   ```sh
   claude
   ```

4. 「インテーク開始」 と伝える\
   (何も指定せず会話を始めても、Claude が `input/事前検討資料/` の中身と `output/project_profile.md` の状態を見て自動的に Phase 0 or インテークを促します)

5. 質問に順番に答えていくと、案件特性に応じたドキュメントが順次生成されます

---

## ディレクトリ構成

```
.
├── CLAUDE.md                                 # Claude 向け運用ルール(最重要)
├── README.md                                 # このファイル
├── WORKFLOW.md                               # 3ツール協調フローの全体図(Mermaid)
├── ChangeLog.md                              # ハーネス本体の改修履歴
├── input/
│   ├── システム開発設計ドキュメント一覧.md   # 原典(改変禁止)
│   └── 事前検討資料/                         # Phase 0 の入力(任意 / ユーザーが資料を投入)
├── harness/
│   ├── 00_intake.md                          # インテーク質問票
│   ├── 01_selection_rules.md                 # ドキュメント選定ルール
│   ├── 02_workflow.md                        # フェーズ進行手順
│   ├── 03_quality_checklist.md               # 品質・整合性チェック(手動観点)
│   ├── tools/
│   │   ├── check.py                          # 整合性検証スクリプト(構造/ID/状態)
│   │   └── fixtures/                         # check.py の自己検証用サンプル
│   └── templates/
│       ├── _format.md                        # テンプレ共通フォーマット規約
│       ├── _index.md                         # テンプレ一覧と生成方針
│       ├── _test_code_convention.md          # テストコード生成規約(Phase 3.5 / TDD時)
│       ├── PR-1_事前検討サマリ.md            # Phase 0(事前検討の正規化 / ハーネス拡張)
│       ├── DM-1_ドメインモデル.md            # DDD採用時(ハーネス拡張)
│       ├── ADR-NNNN_アーキテクチャ決定記録.md # ADR(MADR形式 / ハーネス拡張)
│       └── {doc_id}_*.md                     # 各ドキュメントのテンプレ(必要時に生成)
└── output/                                   # 案件ごとの成果物
    ├── README.md
    ├── project_profile.md                    # 案件プロファイル(インテーク結果)
    ├── _doc_plan.md                          # 作成計画と進捗
    ├── _id_registry.md                       # ID採番台帳
    ├── _review_log.md                        # レビュー実施ログ
    ├── 00_事前検討/                          # Phase 0 (PR-1) / 資料投入時のみ
    ├── 01_企画/                              # Phase 1 (P-*)
    ├── 02_要件定義/                          # Phase 1 (R-*)
    ├── 03_基本設計/                          # Phase 1 + Phase 3 (B-* 画面以外)
    ├── _handoff_to_claude_design/            # Phase 1 → 2 引き渡しパッケージ
    ├── 04_画面設計_from_ClaudeDesign/        # Phase 2 成果物 (B-7, B-8)
    ├── 05_詳細設計/                          # Phase 3 (D-*) + Phase 3.5 (D-15最終化, TS-1)
    ├── _handoff_to_implementation/           # Phase 3.5 → 4 引き渡し(Red テスト / TDD時)
    └── 横断/                                  # 用語集、RTM、ステークホルダー一覧、DM-1 ドメインモデル
        └── ADR/                              # アーキテクチャ決定記録(随時蓄積)+ _index.md
```

---

## 設計思想

| 原則 | 内容 |
|---|---|
| プロファイル駆動 | 案件特性を最初に固定し、そこから作るドキュメントを機械的に決める |
| 事前検討の正規化(任意) | `input/事前検討資料/` に投入された雑多な検討資料を、要件定義に入る前に「問題 → 原因 → 対応策」の構造化サマリ(PR-1)に正規化する |
| テンプレ準拠 | 全ドキュメントが共通フォーマットに従う(`_format.md`) |
| ID・用語の一元化 | 採番台帳と用語集をハーネス側で強制 |
| 2層の整合性チェック | `check.py` で構造・ID・状態の **形式整合を自動検証**、`03_quality_checklist.md` で **意味の妥当性を手動検証** |
| 意思決定の記録 | 設計上の意思決定が発生するたびに ADR(MADR形式)を `output/横断/ADR/` に随時蓄積 |
| Just Enough | アジャイル運用時は必要最小限のドキュメントのみ |
| テスト先行(オプション) | テスト戦略 = TDD の案件では、Phase 3.5 で設計からテストを先に作り、2段階レビューゲートで承認してから実装に渡す |

---

## ハーネスを使う前提

- Claude Code が利用可能であること
- このディレクトリのルートで `claude` を起動すること(`CLAUDE.md` を Claude が読み込むため)
- 案件ごとに**コピーして**使うこと(ハーネス本体を直接編集して案件作業をしない)
- **モデルは Opus(`claude-opus-4-8`)で運用すること**
  - 起動時に `/model opus` で切り替えるか、`claude --model claude-opus-4-8` で起動
  - 上流の業務要件・非機能要件・設計判断の品質が下流まで波及するため、フェーズを問わず Opus 一択で運用する方針です
  - Sonnet / Haiku への切り替えは、簡易な定形作業に限定する場合のみ自己責任で
- **図は `.drawio.svg` 形式を正本**とする(成果物の図を表示・編集するため)
  - VS Code 利用時は拡張「Draw.io Integration」(`hediet.vscode-drawio`)の導入を推奨
  - `.drawio.svg` はそのまま GUI で編集でき、Markdown プレビューや GitHub では画像として表示されます(Mermaid のように環境依存で表示されない問題を避けられます)

---

## ハーネスのバージョン

v0.12 (2026-06 設計 repo ↔ 実装 repo 同期支援: ① `harness/tools/sync-to-impl.sh`(設計成果物を実装 repo の `docs/design/` へコピー)、\
② 実装 repo 向けスケルトン `harness/templates/impl_repo/`(`CLAUDE_impl.md` / `docs/design/README.md` / 読取専用 pre-commit ガード)、\
③ ADR テンプレに `origin`(設計フェーズ発 / 実装フェーズ発)、④ 同期台帳 `_handoff_to_implementation/_sync_log.md`、\
⑤ `WORKFLOW.md §8` に submodule セットアップ手順(Win/mac)・影響レベル分類・ADR 同期キー運用を追記)

ハーネス自体の改善要望や不備の報告は、案件作業を進める中で気づいた時点でユーザー → Claude へ伝えてください。\
`harness/` 配下を改修し、ハーネス本体の変更は `ChangeLog.md` に、\
案件中の局所的な微修正は `output/_review_log.md` に「ハーネス改修」として記録します。
