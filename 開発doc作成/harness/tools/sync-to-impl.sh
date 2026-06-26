#!/usr/bin/env bash
# ----------------------------------------------------------------------
# 設計 repo → 実装 repo 同期スクリプト(v0.12〜)
#
# このハーネス(設計 repo)の output/ 成果物を、別の実装リポジトリの
# docs/design/ に「スナップショットとしてコピー」する支援スクリプト。
# git submodule を使わない単純コピー運用のための道具。
# (submodule 運用の場合はこのスクリプトは不要 — WORKFLOW.md §8 参照)
#
# Windows(Git Bash)/ macOS / Linux 両対応。rsync があれば使い、無ければ
# cp にフォールバックする。
#
# 使い方:
#   $ bash harness/tools/sync-to-impl.sh <実装リポジトリのパス>
#   $ bash harness/tools/sync-to-impl.sh ~/projects/impl-app
#   $ bash harness/tools/sync-to-impl.sh ../impl-app
#
# コピーされるもの(実装の入力 / WORKFLOW.md §8 と一致):
#   output/02_要件定義/ 03_基本設計/ 04_画面設計_from_ClaudeDesign/
#   05_詳細設計/ 横断/ 00_事前検討/(あれば)
#   output/_handoff_to_implementation/(TDD採用時の Red テスト等)
#   → すべて <実装repo>/docs/design/ 配下に配置
#
# あわせて <実装repo>/docs/design/README.md を「設計 repo <URL> の
# commit <hash> 時点のスナップショット」マーカーとして生成する。
# ----------------------------------------------------------------------
set -euo pipefail

if [ $# -lt 1 ]; then
    cat >&2 <<EOF
Usage: $0 <実装リポジトリのパス>

例:
  $0 ~/projects/impl-app
  $0 ../impl-app
EOF
    exit 1
fi

IMPL_REPO="$1"
SOURCE="$(pwd)"
OUTPUT_DIR="${SOURCE}/output"

# このディレクトリが設計 repo(output/ を持つ)か簡易チェック
if [ ! -d "${OUTPUT_DIR}" ]; then
    echo "ERROR: ${OUTPUT_DIR} がありません。設計 repo のルート(CLAUDE.md がある場所)で実行してください。" >&2
    exit 1
fi

if [ ! -d "${IMPL_REPO}" ]; then
    echo "ERROR: 実装リポジトリ ${IMPL_REPO} が見つかりません。先に作成/クローンしてください。" >&2
    exit 1
fi

DEST="${IMPL_REPO%/}/docs/design"
mkdir -p "${DEST}"

# 設計 repo の現在の commit / remote を取得(README マーカー用)
DESIGN_HASH="$(git -C "${SOURCE}" rev-parse --short HEAD 2>/dev/null || echo 'unknown')"
DESIGN_URL="$(git -C "${SOURCE}" remote get-url origin 2>/dev/null || echo '(remote 未設定 / ローカルパス運用)')"
SYNC_DATE="$(date +%Y-%m-%d)"

# コピー対象ディレクトリ(存在するものだけ)
TARGETS=(
    "00_事前検討"
    "02_要件定義"
    "03_基本設計"
    "04_画面設計_from_ClaudeDesign"
    "05_詳細設計"
    "横断"
    "_handoff_to_implementation"
)

# rsync があれば --delete で鏡映同期、無ければ cp -a
copy_dir() {
    local src="$1" dst="$2"
    if command -v rsync >/dev/null 2>&1; then
        rsync -a --delete "${src}/" "${dst}/"
    else
        rm -rf "${dst}"
        mkdir -p "${dst}"
        cp -a "${src}/." "${dst}/"
    fi
}

echo "設計 repo → 実装 repo 同期中..."
echo "  source: ${OUTPUT_DIR}"
echo "  dest:   ${DEST}"
echo ""

for t in "${TARGETS[@]}"; do
    if [ -d "${OUTPUT_DIR}/${t}" ]; then
        copy_dir "${OUTPUT_DIR}/${t}" "${DEST}/${t}"
        echo "  ✅ ${t}/"
    fi
done

# 状態ファイルも参考に同梱(読み取り専用の前提知識として有用)
for f in "project_profile.md" "_doc_plan.md" "_id_registry.md"; do
    if [ -f "${OUTPUT_DIR}/${f}" ]; then
        cp -a "${OUTPUT_DIR}/${f}" "${DEST}/${f}"
        echo "  ✅ ${f}"
    fi
done

# スナップショットマーカー README を生成
cat > "${DEST}/README.md" <<EOF
# docs/design — 設計 repo スナップショット(読み取り専用)

このディレクトリは **設計 repo のスナップショット**です。実装 repo 側では **編集しないでください**。

| 項目 | 値 |
|---|---|
| 設計 repo | ${DESIGN_URL} |
| スナップショット commit | \`${DESIGN_HASH}\` |
| 同期日 | ${SYNC_DATE} |
| 同期方式 | 単純コピー(sync-to-impl.sh) |

## ルール

- このディレクトリの中身は設計 repo が原本です。**ここを直接編集しても次回同期で上書き**されます。
- 実装中に設計を変えたくなったら、**ADR を切って**(\`origin: implementation\`)記録し、設計 repo に逆同期してから D-* / B-* を更新します(影響レベルの判断は設計 repo の WORKFLOW.md §8 を参照)。
- 再同期: 設計 repo 側で \`bash harness/tools/sync-to-impl.sh <この実装repoパス>\` を再実行します。

## 影響レベル(設計変更が生じたとき)

- **小** = 設計影響なし → 実装 repo のみで対応
- **中** = 設計影響あり → ADR を切る → 後で設計 repo の D-* / B-* を更新
- **大** = 要件レベル → 実装を一時停止し設計 repo に戻る
EOF
echo "  ✅ docs/design/README.md(スナップショットマーカー)"

echo ""
echo "✅ 同期完了: ${DEST}"
echo ""
echo "次のステップ(実装 repo 側):"
echo "  1. docs/design/ は読み取り専用として扱う(編集しない)"
echo "  2. 設計変更が生じたら ADR を切る(origin: implementation)"
echo "  3. 同期記録を設計 repo の output/_handoff_to_implementation/_sync_log.md に残す"
