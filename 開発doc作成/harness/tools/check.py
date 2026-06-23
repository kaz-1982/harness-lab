#!/usr/bin/env python3
"""
ハーネス整合性検証スクリプト(最小版 / Phase: 自動チェック)

機械的に検証できる項目だけを扱う。意味の妥当性(要件が業務的に正しいか、
期待結果が妥当か等)は検証しない —— それは AI / 人のレビュー範囲。

検証項目:
  1. 構造チェック   — frontmatter 必須キー + セクション 1〜7 の存在(_format.md 準拠)
  2. ID整合         — 本文のインスタンスID参照が _id_registry に登録済か / 重複 / プレフィクス規則
  3. 状態突合       — 各ドキュメントの doc_id が _doc_plan に存在するか

使い方:
  python3 harness/tools/check.py [OUTPUT_DIR]   # 既定は ./output
  python3 harness/tools/check.py --help

read-only。問題があれば終了コード 1、なければ 0(ディレクトリ不在は 2)。
"""

import os
import re
import sys
import glob

# 既知のインスタンスIDプレフィクス(CLAUDE.md「3. ID体系の一貫性」準拠)
# AG(集約)/ VO(値オブジェクト)は DDD ドメインモデル(DM-1)で採番するインスタンスID。
INSTANCE_PREFIXES = ["R-B", "R-F", "R-NF", "UT", "AT", "BT", "RP", "AG", "VO", "F", "S", "A", "E", "T"]
# 長いプレフィクスを先に並べて誤マッチを防ぐ(R-NF > R-B > UT > T の順)
_ALT = "|".join(sorted(INSTANCE_PREFIXES, key=len, reverse=True))
ID_PATTERN = re.compile(r"\b(?:" + _ALT + r")-\d{3,}\b")

# 各ドキュメントに必須のセクション見出し(_format.md の標準構造 1〜7)
REQUIRED_SECTIONS = ["## 1.", "## 2.", "## 3.", "## 4.", "## 5.", "## 6.", "## 7."]
REQUIRED_FRONTMATTER = ["doc_id", "phase", "depends_on", "mode"]


class Issue:
    def __init__(self, kind, path, message):
        self.kind = kind
        self.path = path
        self.message = message

    def __str__(self):
        return f"    {self.path}: {self.message}"


def parse_markdown_table(path):
    """マークダウン表を行(セルのリスト)のリストとして返す。区切り行(---)は除く。"""
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line.startswith("|"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all((set(c) <= set("-: ")) and c for c in cells):
                continue  # |---|---| の区切り行
            rows.append(cells)
    return rows


def load_registry(output_dir):
    """_id_registry.md から登録IDのリスト(重複検出のため list)と存在フラグを返す。"""
    path = os.path.join(output_dir, "_id_registry.md")
    ids = []
    for cells in parse_markdown_table(path):
        if not cells:
            continue
        first = cells[0]
        if first.upper() == "ID" or first == "":
            continue  # ヘッダ行
        if re.match(r"^[A-Z]", first):
            ids.append(first)
    return ids, os.path.exists(path)


def load_doc_plan(output_dir):
    """_doc_plan.md から {doc_id: 状態} と存在フラグを返す。"""
    path = os.path.join(output_dir, "_doc_plan.md")
    plan = {}
    rows = parse_markdown_table(path)
    if not rows:
        return plan, os.path.exists(path)
    header = rows[0]

    def col_index(names):
        for i, h in enumerate(header):
            if any(n in h for n in names):
                return i
        return None

    id_col = col_index(["ID"])
    st_col = col_index(["状態"])
    if id_col is None:
        return plan, os.path.exists(path)
    for cells in rows[1:]:
        if id_col >= len(cells):
            continue
        doc_id = cells[id_col].strip().strip("*").strip()
        if not doc_id or doc_id == "...":
            continue
        status = cells[st_col].strip() if (st_col is not None and st_col < len(cells)) else ""
        plan[doc_id] = status
    return plan, os.path.exists(path)


def parse_frontmatter(text):
    """先頭の --- ... --- を dict で返す。無ければ None。"""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


# 検証対象外の管理ファイル(設計ドキュメントではない)
EXCLUDE_NAMES = {"README.md", "project_profile.md"}
# 標準構造(frontmatter + セクション1〜7)を持たない原典外ドキュメント群のディレクトリ。
# ADR(アーキテクチャ決定記録)は MADR 形式で1決定1ファイルを蓄積するため標準検証の対象外。
# 索引は output/横断/ADR/_index.md(_ 始まりで自動除外)で管理する。
EXCLUDE_DIRS = {"ADR"}


def iter_doc_files(output_dir):
    """検証対象のドキュメント(*.md)を列挙。管理ファイル(_*)・README・プロファイル・EXCLUDE_DIRS 配下は除外。"""
    docs = []
    for path in glob.glob(os.path.join(output_dir, "**", "*.md"), recursive=True):
        base = os.path.basename(path)
        if base.startswith("_") or base in EXCLUDE_NAMES:
            continue
        parts = os.path.normpath(path).split(os.sep)
        if any(d in EXCLUDE_DIRS for d in parts):
            continue  # ADR 等、標準構造を持たない原典外ドキュメントのディレクトリ
        docs.append(path)
    return sorted(docs)


def check_structure(path, text, fm):
    issues = []
    if fm is None:
        issues.append(Issue("構造", path, "frontmatter(--- ブロック)が無い"))
    else:
        for key in REQUIRED_FRONTMATTER:
            if key not in fm:
                issues.append(Issue("構造", path, f"frontmatter に必須キー '{key}' が無い"))
    for sec in REQUIRED_SECTIONS:
        if sec not in text:
            issues.append(Issue("構造", path, f"必須セクション '{sec}' が無い"))
    return issues


def check_ids(path, text, registry_set):
    issues = []
    for rid in sorted(set(ID_PATTERN.findall(text))):
        if rid not in registry_set:
            issues.append(Issue("ID整合", path, f"参照ID '{rid}' が _id_registry に未登録"))
    return issues


def check_status(path, fm, plan, plan_exists):
    issues = []
    if not plan_exists or fm is None or "doc_id" not in fm:
        return issues
    doc_id = fm["doc_id"]
    if doc_id not in plan:
        issues.append(Issue("状態突合", path, f"doc_id '{doc_id}' が _doc_plan に存在しない"))
    return issues


def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    output_dir = args[0] if args else "output"
    if not os.path.isdir(output_dir):
        print(f"ERROR: ディレクトリが見つかりません: {output_dir}")
        return 2

    registry_ids, reg_exists = load_registry(output_dir)
    registry_set = set(registry_ids)
    plan, plan_exists = load_doc_plan(output_dir)
    docs = iter_doc_files(output_dir)

    issues = []

    # _id_registry 内の重複
    for d in sorted({x for x in registry_ids if registry_ids.count(x) > 1}):
        issues.append(Issue("ID整合", os.path.join(output_dir, "_id_registry.md"),
                            f"ID '{d}' が重複登録されている"))
    # _id_registry 内のプレフィクス/桁数規則
    for rid in registry_ids:
        if not ID_PATTERN.fullmatch(rid):
            issues.append(Issue("ID整合", os.path.join(output_dir, "_id_registry.md"),
                                f"登録ID '{rid}' がプレフィクス/桁数規則に合わない"))

    # 各ドキュメント
    for path in docs:
        with open(path, encoding="utf-8") as f:
            text = f.read()
        fm = parse_frontmatter(text)
        issues += check_structure(path, text, fm)
        issues += check_ids(path, text, registry_set)
        issues += check_status(path, fm, plan, plan_exists)

    # ---- 出力 ----
    print("=" * 64)
    print(f"ハーネス整合性チェック: {output_dir}")
    print("=" * 64)
    print(f"  検証対象ドキュメント : {len(docs)} 件")
    print(f"  _id_registry.md      : {'あり' if reg_exists else '未作成'} / 登録ID {len(registry_ids)} 件")
    print(f"  _doc_plan.md         : {'あり' if plan_exists else '未作成(状態突合はスキップ)'}")
    print("-" * 64)

    if not issues:
        print("  ✅ 機械チェックは問題なし")
        print("-" * 64)
        print("  注意: 検証したのは形式・参照・整合のみ。")
        print("  意味の妥当性(要件の正しさ・期待結果の妥当性)は別途レビューが必要です。")
        return 0

    by_kind = {}
    for iss in issues:
        by_kind.setdefault(iss.kind, []).append(iss)
    for kind in sorted(by_kind):
        print(f"  ● {kind}: {len(by_kind[kind])} 件")
        for iss in by_kind[kind]:
            print(str(iss))
        print()
    print("-" * 64)
    print(f"  ❌ 合計 {len(issues)} 件の問題を検出(意味の妥当性は別途レビュー)")
    return 1


if __name__ == "__main__":
    sys.exit(main())
