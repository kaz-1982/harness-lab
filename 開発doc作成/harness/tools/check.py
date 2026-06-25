#!/usr/bin/env python3
"""
ハーネス整合性検証スクリプト(Phase: 自動チェック)

機械的に検証できる項目だけを扱う。意味の妥当性(要件が業務的に正しいか、
期待結果が妥当か等)は検証しない —— それは AI / 人のレビュー範囲。

検証項目:
  1. 構造チェック     — frontmatter 必須キー + セクション 1〜7 の存在(_format.md 準拠)
  2. ID整合           — 本文のインスタンスID参照が _id_registry に登録済か / 重複 / プレフィクス規則
  3. 状態突合         — 各ドキュメントの doc_id が _doc_plan に存在するか
  4. 孤立検出         — R-14 RTM があるとき、登録 R-B-* / R-F-* / F-* が RTM に出現するか
  5. AC/AT 網羅(TDD) — TS-1 があるとき、登録 R-F-* が TS-1 に参照されているか

オプション:
  --tbd               TBD を _tbd_dashboard.md に集約出力(これだけが書き込みを行う)

使い方:
  python3 harness/tools/check.py [OUTPUT_DIR]                 # 検証のみ。既定は ./output
  python3 harness/tools/check.py --tbd [OUTPUT_DIR]           # 検証 + TBD ダッシュボード生成
  python3 harness/tools/check.py --help

検証は read-only(--tbd 指定時のみ _tbd_dashboard.md に書き込む)。
問題があれば終了コード 1、なければ 0(ディレクトリ不在は 2)。
"""

import os
import re
import sys
import glob
from collections import defaultdict
from datetime import datetime, timezone, timedelta

# Windows の cp932 環境でも ✅ / ❌ を出力できるように stdout を UTF-8 化
# (Python 3.7+ で sys.stdout.reconfigure が利用可能)
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# 既知のインスタンスIDプレフィクス(CLAUDE.md「3. ID体系の一貫性」準拠)
# AG(集約)/ VO(値オブジェクト)は DDD ドメインモデル(DM-1)で採番するインスタンスID。
INSTANCE_PREFIXES = ["R-B", "R-F", "R-NF", "UT", "AT", "BT", "RP", "AG", "VO", "F", "S", "A", "E", "T"]
# 長いプレフィクスを先に並べて誤マッチを防ぐ(R-NF > R-B > UT > T の順)
_ALT = "|".join(sorted(INSTANCE_PREFIXES, key=len, reverse=True))
ID_PATTERN = re.compile(r"\b(?:" + _ALT + r")-\d{3,}\b")

# 各ドキュメントに必須のセクション見出し(_format.md の標準構造 1〜7)
REQUIRED_SECTIONS = ["## 1.", "## 2.", "## 3.", "## 4.", "## 5.", "## 6.", "## 7."]
REQUIRED_FRONTMATTER = ["doc_id", "phase", "depends_on", "mode"]

# 検証対象外の管理ファイル(設計ドキュメントではない)
EXCLUDE_NAMES = {"README.md", "project_profile.md"}
# 標準構造(frontmatter + セクション1〜7)を持たない原典外ドキュメント群のディレクトリ。
# ADR(アーキテクチャ決定記録)は MADR 形式で1決定1ファイルを蓄積するため標準検証の対象外。
# 索引は output/横断/ADR/_index.md(_ 始まりで自動除外)で管理する。
EXCLUDE_DIRS = {"ADR"}


class Issue:
    def __init__(self, kind, path, message):
        self.kind = kind
        self.path = path
        self.message = message

    def __str__(self):
        return f"    {self.path}: {self.message}"


# ===================================================================
# 共通パーサ
# ===================================================================

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


def find_doc(output_dir, doc_id_prefix):
    """{doc_id_prefix}_*.md を output 配下から探し、最初に見つかったパスを返す(なければ None)。"""
    pattern = os.path.join(output_dir, "**", f"{doc_id_prefix}_*.md")
    hits = glob.glob(pattern, recursive=True)
    return hits[0] if hits else None


def read_text(path):
    if path is None or not os.path.exists(path):
        return ""
    with open(path, encoding="utf-8") as f:
        return f.read()


# ===================================================================
# 検証ロジック
# ===================================================================

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


def _extract_ids_from_tables(path):
    """ドキュメント内の全マークダウン表のセルから ID を抽出(本文の地の文は無視)。

    地の文(コメントや解説)に ID が偶然出ても誤検知しないよう、表セル限定で判定する。
    フロントマターや改訂履歴の表も含むが、それらは ID を含まないので無害。
    """
    ids = set()
    rows = parse_markdown_table(path)
    if len(rows) <= 1:
        return ids  # 表が雛形のみのとき
    for cells in rows[1:]:  # ヘッダ行を除く
        for cell in cells:
            for rid in ID_PATTERN.findall(cell):
                ids.add(rid)
    return ids


def check_orphans(output_dir, registry_ids):
    """R-14 RTM があるとき、登録された R-B-* / R-F-* / F-* が RTM の **表セル** に出現するか確認。

    RTM が無い案件(小規模・省略時)では本検査をスキップ(RTM 不在自体は問題ではない)。
    出現しない場合は「孤立要件 / 孤立機能の可能性」として警告する。
    """
    issues = []
    rtm_path = find_doc(output_dir, "R-14")
    if rtm_path is None:
        return issues  # RTM 省略時はスキップ
    rtm_ids = _extract_ids_from_tables(rtm_path)
    if not rtm_ids:
        return issues  # 雛形のみで未記入のときはスキップ(誤検出を避ける)
    for rid in registry_ids:
        if rid.startswith(("R-B-", "R-F-")) and rid not in rtm_ids:
            issues.append(Issue("孤立検出", rtm_path,
                                f"要件 '{rid}' が R-14 RTM の表に出現しない(孤立要件の可能性)"))
        elif rid.startswith("F-") and not rid.startswith("R-F") and rid not in rtm_ids:
            # "F-" は機能ID。R-F- は上の分岐で扱うので除外
            issues.append(Issue("孤立検出", rtm_path,
                                f"機能 '{rid}' が R-14 RTM の表に出現しない(孤立機能の可能性)"))
    return issues


def check_tdd_coverage(output_dir, registry_ids):
    """TS-1(受け入れテスト仕様書)があるとき、登録 R-F-* が TS-1 の **表セル** に出現するか確認。

    TS-1 が無い案件(TDD 不採用)、または TS-1 に AT-* がまだ無い(骨子段階)では本検査をスキップ。
    本文の地の文ではなく **表セル限定** で判定する(誤検出を避けるため)。
    """
    issues = []
    ts1_path = find_doc(output_dir, "TS-1")
    if ts1_path is None:
        return issues
    ts1_text = read_text(ts1_path)
    at_ids = set(re.findall(r"\bAT-\d{3,}\b", ts1_text))
    if not at_ids:
        return issues  # 骨子段階。Phase 3.5 ゲート1未実施として警告しない
    ts1_ids = _extract_ids_from_tables(ts1_path)
    for rid in registry_ids:
        if rid.startswith("R-F-") and rid not in ts1_ids:
            issues.append(Issue("AC/AT 網羅", ts1_path,
                                f"機能要件 '{rid}' に対応する AT-* が TS-1 の表に見つからない(トレース欄に未記入の可能性)"))
    return issues


# ===================================================================
# TBD 集約(--tbd オプション時のみ)
# ===================================================================

def aggregate_tbd(output_dir, docs):
    """全ドキュメントから TBD 行を集約。

    収集対象:
      - 各ドキュメントの本文中の "TBD" を含む行
      - 「## 7. レビュー状態」セクションの未確認事項
      - project_profile.md の「TBD / 保留中の項目」セクション

    収集対象外:
      - "TBD" を見出しのみとする行(`### TBD`)
      - "(なし)" のみの行
    """
    entries = []  # {path, line, where, text}

    def collect_from_file(path, special_section_name=None):
        """special_section_name が指定されたとき、そのセクション内のみを収集"""
        if not os.path.exists(path):
            return
        with open(path, encoding="utf-8") as f:
            lines = f.read().splitlines()
        in_review = False
        in_special = False
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            # セクション境界の判定
            if stripped.startswith("## 7."):
                in_review = True
                in_special = False
                continue
            if special_section_name and special_section_name in stripped and stripped.startswith("##"):
                in_special = True
                in_review = False
                continue
            if stripped.startswith("## "):
                # 新セクション開始でリセット(7.以外の見出し)
                if not stripped.startswith("## 7."):
                    in_review = False
                    in_special = False
            # TBD 検出
            if "TBD" in stripped and not stripped.startswith("#"):
                where = "レビュー状態" if in_review else ("プロファイル保留" if in_special else "本文")
                entries.append({
                    "path": os.path.relpath(path, output_dir).replace(os.sep, "/"),
                    "line": i,
                    "where": where,
                    "text": stripped[:200],
                })
            elif in_special and stripped.startswith("- ") and stripped not in ("- (なし)", "- (なし、または箇条書き)"):
                # プロファイルの保留セクションは TBD という文字が無くても項目として収集
                entries.append({
                    "path": os.path.relpath(path, output_dir).replace(os.sep, "/"),
                    "line": i,
                    "where": "プロファイル保留",
                    "text": stripped[:200],
                })

    # 各ドキュメント
    for path in docs:
        collect_from_file(path)
    # project_profile の「TBD / 保留中の項目」も特別に拾う
    pp = os.path.join(output_dir, "project_profile.md")
    collect_from_file(pp, special_section_name="TBD / 保留中の項目")

    return entries


def write_tbd_dashboard(output_dir, entries):
    """_tbd_dashboard.md を生成。read-only の原則を破る唯一の出力。"""
    out_path = os.path.join(output_dir, "_tbd_dashboard.md")
    jst = timezone(timedelta(hours=9))
    now = datetime.now(jst).strftime("%Y-%m-%d %H:%M JST")

    lines = []
    lines.append("# TBD ダッシュボード(自動生成)\n")
    lines.append(f"> このファイルは `harness/tools/check.py --tbd` が自動生成します。手動編集しないでください。\n")
    lines.append(f"> 最終生成: {now}\n")
    lines.append("")
    lines.append(f"## サマリ\n")
    lines.append(f"- 検出件数: **{len(entries)} 件**\n")
    if not entries:
        lines.append("\n現時点で TBD はありません。完了判定前にもう一度実行することを推奨します。\n")
    else:
        # ドキュメント別に集計
        by_path = defaultdict(list)
        for e in entries:
            by_path[e["path"]].append(e)
        lines.append("\n## ドキュメント別\n")
        lines.append("| ドキュメント | 件数 | 内訳 |\n|---|---|---|\n")
        for path in sorted(by_path):
            es = by_path[path]
            where_counts = defaultdict(int)
            for e in es:
                where_counts[e["where"]] += 1
            breakdown = " / ".join(f"{k}:{v}" for k, v in sorted(where_counts.items()))
            lines.append(f"| `{path}` | {len(es)} | {breakdown} |\n")

        lines.append("\n## 全件一覧\n")
        lines.append("| ドキュメント | 行 | 区分 | 内容 |\n|---|---|---|---|\n")
        for e in entries:
            text = e["text"].replace("|", "\\|")
            lines.append(f"| `{e['path']}` | L{e['line']} | {e['where']} | {text} |\n")

    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
    return out_path


# ===================================================================
# メイン
# ===================================================================

def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0

    do_tbd = "--tbd" in sys.argv
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

    # 横断: 孤立検出(R-14 RTM があるとき) / AC/AT 網羅(TS-1 があるとき)
    issues += check_orphans(output_dir, registry_ids)
    issues += check_tdd_coverage(output_dir, registry_ids)

    # TBD 集約(オプション)
    tbd_path = None
    tbd_count = 0
    if do_tbd:
        tbd_entries = aggregate_tbd(output_dir, docs)
        tbd_count = len(tbd_entries)
        tbd_path = write_tbd_dashboard(output_dir, tbd_entries)

    # ---- 出力 ----
    print("=" * 64)
    print(f"ハーネス整合性チェック: {output_dir}")
    print("=" * 64)
    print(f"  検証対象ドキュメント : {len(docs)} 件")
    print(f"  _id_registry.md      : {'あり' if reg_exists else '未作成'} / 登録ID {len(registry_ids)} 件")
    print(f"  _doc_plan.md         : {'あり' if plan_exists else '未作成(状態突合はスキップ)'}")
    if do_tbd:
        print(f"  TBD ダッシュボード   : {tbd_count} 件 → {tbd_path}")
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
