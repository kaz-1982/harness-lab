# impl_repo/ — 実装リポジトリ向けスケルトン集(v0.12〜)

このディレクトリは、**実装リポジトリ(Phase 4・別リポジトリ)側に置くファイルのスケルトン**です。
設計 repo(このハーネス)と実装 repo を分けて運用するとき、実装 repo 側にコピーして使います。
全体方針は [../../../WORKFLOW.md](../../../WORKFLOW.md) §8 を参照。

## 中身

| ファイル | 実装 repo 側での置き先 | 用途 |
|---|---|---|
| `CLAUDE_impl.md` | `CLAUDE.md`(ルート) | 実装 repo 用の Claude 運用ルール。`docs/design/` 読取専用 / 設計変更は ADR / 同期方式 を明文化 |
| `docs_design_README.md` | `docs/design/README.md` | **submodule 運用時**のスナップショットマーカー(単純コピー運用では `sync-to-impl.sh` が自動生成するため不要) |
| `pre-commit` | `.git/hooks/pre-commit` | `docs/design/` の変更を staging で検知して止める軽量ガード |

## 使い方(実装 repo 側)

```bash
# 1. 運用ルールを設置(既存 CLAUDE.md があれば連携セクションを追記)
cp <設計repo>/harness/templates/impl_repo/CLAUDE_impl.md ./CLAUDE.md

# 2-a. submodule 運用の場合(設計 repo をネスト)
git submodule add <設計repoのパス/URL> docs/design
cp <設計repo>/harness/templates/impl_repo/docs_design_README.md docs/design/../design/README.md  # 必要に応じ手動配置

# 2-b. 単純コピー運用の場合(設計 repo 側で実行)
#   bash harness/tools/sync-to-impl.sh <この実装repoパス>
#   → docs/design/ にスナップショット + README.md が自動生成される

# 3. 読み取り専用ガードを設置
cp <設計repo>/harness/templates/impl_repo/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

詳細な submodule セットアップ手順(Windows / macOS 両対応)は [../../../WORKFLOW.md](../../../WORKFLOW.md) §8 を参照してください。
