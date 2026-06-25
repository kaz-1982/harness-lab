#!/usr/bin/env bash
# ----------------------------------------------------------------------
# ハーネスを新規案件用にコピーするスクリプト(v0.10〜)
#
# このスクリプトは「ハーネス本体(マスター)」のディレクトリで実行する。
# `.harness-source` マーカーが無いディレクトリでは実行できない(安全装置)。
#
# 使い方:
#   $ bash harness/tools/new-project.sh <案件ディレクトリ>
#   $ bash harness/tools/new-project.sh ~/projects/case-A
#   $ bash harness/tools/new-project.sh ../案件A
#
# コピー対象: ハーネス本体一式(harness/, input/, CLAUDE.md, README.md,
#             WORKFLOW.md, ChangeLog.md, output/ の雛形)。
# コピー除外:
#   - .harness-source(マーカー / 本体のみ存在)
#   - examples/(学習用 / 案件には不要)
#   - .git, .gitignore は残す(案件側で git init し直すかは自由)
#   - output/_tbd_dashboard.md(check.py --tbd の生成物)
#   - output/_handoff_*/(以前の案件の引き渡しパッケージ。最初の案件で
#     不要だが、コピー段階では雛形だけ残してOK — README.md があれば残す)
# ----------------------------------------------------------------------
set -euo pipefail

if [ $# -lt 1 ]; then
    cat >&2 <<EOF
Usage: $0 <案件ディレクトリのパス>

例:
  $0 ~/projects/case-A
  $0 ../案件A
  $0 /tmp/test-case
EOF
    exit 1
fi

DEST="$1"
SOURCE="$(pwd)"

# 安全装置: 本体マーカーが存在するディレクトリでのみ実行可能
if [ ! -f "${SOURCE}/.harness-source" ]; then
    echo "ERROR: 現在のディレクトリにハーネス本体マーカー (.harness-source) がありません。" >&2
    echo "       ハーネス本体(CLAUDE.md / harness/ がある場所)で実行してください。" >&2
    exit 1
fi

if [ ! -f "${SOURCE}/CLAUDE.md" ] || [ ! -d "${SOURCE}/harness" ]; then
    echo "ERROR: CLAUDE.md または harness/ が見当たりません。ハーネス本体で実行してください。" >&2
    exit 1
fi

# コピー先が既存ならエラー(上書き事故防止)
if [ -e "${DEST}" ]; then
    echo "ERROR: コピー先 ${DEST} が既に存在します。別のパスを指定してください。" >&2
    exit 1
fi

# コピー先の親ディレクトリを作成
DEST_PARENT="$(dirname "${DEST}")"
mkdir -p "${DEST_PARENT}"

echo "ハーネス本体をコピー中..."
echo "  source: ${SOURCE}"
echo "  dest:   ${DEST}"

# cp -r でディレクトリごとコピー(隠しファイル含む)
# 末尾の "/." で「ディレクトリの中身」を意味する(GNU cp / BSD cp 両対応)
mkdir -p "${DEST}"
cp -a "${SOURCE}/." "${DEST}/"

# 案件側で削除するもの
echo "案件側で不要なファイルを掃除..."

# 本体マーカーは案件側では不要
rm -f "${DEST}/.harness-source"

# 学習用 examples/ は案件には不要
rm -rf "${DEST}/examples"

# check.py --tbd の生成物
rm -f "${DEST}/output/_tbd_dashboard.md"

# 念のため hooks のインストール跡(あれば)
rm -f "${DEST}/.git/hooks/pre-commit"

echo ""
echo "✅ 完了: ${DEST}"
echo ""
echo "次のステップ:"
echo "  cd ${DEST}"
echo "  claude              # ハーネスが立ち上がる(インテーク or 続きから)"
echo ""
echo "推奨(任意):"
echo "  bash harness/tools/install-hooks.sh    # pre-commit フックを有効化"
echo "  git init && git add -A && git commit -m 'initial: copy from harness'"
echo "                                        # 案件固有の git 履歴を始める"
