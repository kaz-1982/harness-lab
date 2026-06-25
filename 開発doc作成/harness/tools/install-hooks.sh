#!/usr/bin/env bash
# ----------------------------------------------------------------------
# ハーネス Git フック導入スクリプト(v0.9〜)
#
# .git/hooks/pre-commit に harness/tools/hooks/pre-commit へのシンボリック
# リンク(または無理なときはコピー)を設置する。
#
# 使い方:
#   $ bash harness/tools/install-hooks.sh
#   $ git commit ...      # 以降、output/ への変更時に check.py が自動実行される
#
# 既存のフックがある場合は .bak を作って退避する。
# ----------------------------------------------------------------------
set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel)"
SRC="${REPO_ROOT}/harness/tools/hooks/pre-commit"
DEST_DIR="${REPO_ROOT}/.git/hooks"
DEST="${DEST_DIR}/pre-commit"

if [ ! -f "${SRC}" ]; then
    echo "ERROR: 元ファイルが見つかりません: ${SRC}" >&2
    exit 1
fi

if [ ! -d "${DEST_DIR}" ]; then
    echo "ERROR: ${DEST_DIR} が見つかりません(このディレクトリは git リポジトリ内ですか?)" >&2
    exit 1
fi

# 既存フックを退避
if [ -e "${DEST}" ] || [ -L "${DEST}" ]; then
    BAK="${DEST}.bak.$(date +%Y%m%d%H%M%S)"
    mv "${DEST}" "${BAK}"
    echo "既存の pre-commit を ${BAK} に退避しました"
fi

# シンボリックリンクを試み、失敗したらコピー
if ln -s "${SRC}" "${DEST}" 2>/dev/null; then
    echo "✅ シンボリックリンクを作成: ${DEST} → ${SRC}"
else
    cp "${SRC}" "${DEST}"
    echo "✅ ファイルをコピー: ${DEST}(Windows 等でシンボリックリンクが使えないため)"
fi

chmod +x "${DEST}" 2>/dev/null || true

echo ""
echo "次のコミットから harness/tools/check.py が自動実行されます。"
echo "テスト: 何か output/ 配下のファイルを編集 → git add → git commit"
echo "バイパス: git commit --no-verify(推奨しない)"
