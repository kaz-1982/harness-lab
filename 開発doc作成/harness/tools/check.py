#!/usr/bin/env python3
"""
ハーネス整合性検証スクリプト(Phase: 自動チェック)

機械的に検証できる項目だけを扱う。意味の妥当性(要件が業務的に正しいか、
期待結果が妥当か等)は検証しない —— それは AI / 人のレビュー範囲。

検証項目:
  1. 構造チェック         — frontmatter 必須キー + セクション 1〜7 の存在(_format.md 準拠)
  2. ID整合               — 本文のインスタンスID参照が _id_registry に登録済か / 重複 / プレフィクス規則
  3. 状態突合             — 各ドキュメントの doc_id が _doc_plan に存在するか
  4. 孤立検出             — R-14 RTM があるとき、登録 R-B-* / R-F-* / F-* が RTM に出現するか
  5. AC/AT 網羅(TDD)     — TS-1 があるとき、登録 R-F-* が TS-1 に参照されているか
  6. ファイル名整合(v0.9) — ファイル名先頭の doc_id と frontmatter doc_id の一致
  7. 依存検証(v0.9)       — frontmatter depends_on が _doc_plan に存在し、本書が進行中以上なら依存先も承認済か
  8. ADR 突合(v0.9)       — output/横断/ADR/ がある案件で、ADR ファイル群と _index.md の対応・status 記入
  9. 用語整合(v0.10)      — R-13 用語集の「使用禁止語」が他ドキュメント本文に出現していないか
 10. 循環検出(v0.10)      — 全ドキュメントの depends_on を DAG として集約し循環参照を検出
 11. テストマニフェスト突合(v0.13)
                         — _handoff_to_implementation/_test_manifest.md と D-15 / TS-1 の
                            UT-* / AT-* を突合(掲載漏れ / ゴーストを検出。Phase 3.5 ゲート2の補強)

オプション:
  --tbd               TBD を _tbd_dashboard.md に集約出力(これだけが書き込みを行う)
  --json              検証結果を機械可読な JSON で stdout に出力(CI 連携用。人間向けの囲み出力は抑制)
  --color             重大度ごとに ANSI カラーで色分け(error=赤 / warning=黄)。exit code は不変
  --session-start     直近セッションのログ末尾エントリを stdout に表示(セッション再開時に Claude が読む)
  --session-end       新規セッションエントリのテンプレを stdout に出力(セッション終了時にコピペして使う)

使い方:
  python3 harness/tools/check.py [OUTPUT_DIR]                 # 検証のみ。既定は ./output
  python3 harness/tools/check.py --tbd [OUTPUT_DIR]           # 検証 + TBD ダッシュボード生成
  python3 harness/tools/check.py --json [OUTPUT_DIR]          # 検証結果を JSON で出力
  python3 harness/tools/check.py --color [OUTPUT_DIR]         # 重大度を色分けして出力
  python3 harness/tools/check.py --session-start [OUTPUT_DIR] # 末尾セッションログを表示
  python3 harness/tools/check.py --session-end [OUTPUT_DIR]   # 新規エントリのテンプレを表示
  python3 harness/tools/check.py --help

検証は read-only(--tbd 指定時のみ _tbd_dashboard.md に書き込む / --json --color --session-* は stdout のみ)。
問題があれば終了コード 1、なければ 0(ディレクトリ不在は 2)。重大度(severity)は表示・JSON 上の分類で、
warning であっても 1 件でも検出があれば終了コードは 1(網羅性を落とさないため)。
"""

import os
import re
import sys
import glob
import json
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


# 検査種別ごとの重大度(v0.13)。色分け・JSON 上の分類にのみ使用し、終了コードは変えない。
# error   = 形式・参照・整合の崩れ(放置すると後工程が壊れる)
# warning = 取りこぼし・前後関係の疑い(意味レビューで判断する余地がある)
SEVERITY_BY_KIND = {
    "構造": "error",
    "ID整合": "error",
    "状態突合": "error",
    "ファイル名整合": "error",
    "循環検出": "error",
    "ADR 突合": "error",
    "依存検証": "warning",
    "孤立検出": "warning",
    "AC/AT 網羅": "warning",
    "用語整合": "warning",
    "テストマニフェスト": "warning",
}


class Issue:
    def __init__(self, kind, path, message, line=None):
        self.kind = kind
        self.path = path
        self.message = message
        self.line = line  # 1始まりの行番号(分かる検査のみ。不明なら None)

    @property
    def severity(self):
        return SEVERITY_BY_KIND.get(self.kind, "error")

    def __str__(self):
        loc = f"{self.path}:L{self.line}" if self.line else self.path
        return f"    {loc}: {self.message}"


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
    lines = text.splitlines()

    def first_line_of(rid):
        for i, line in enumerate(lines, 1):
            if rid in line:
                return i
        return None

    for rid in sorted(set(ID_PATTERN.findall(text))):
        if rid not in registry_set:
            issues.append(Issue("ID整合", path,
                                f"参照ID '{rid}' が _id_registry に未登録",
                                line=first_line_of(rid)))
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


def check_filename_vs_doc_id(path, fm):
    """ファイル名先頭の doc_id と frontmatter doc_id が一致するか確認(v0.9〜)。

    規約: ファイル名は `{doc_id}_{ドキュメント名}.md`(harness/templates/_format.md)。
    フロントマターを後から書き換えた / ファイルをリネームしたときの不整合事故を検出する。
    `_` を含まないファイル名(規約外)は検証対象外。
    """
    issues = []
    if fm is None or "doc_id" not in fm:
        return issues
    fm_doc_id = fm["doc_id"].strip()
    base = os.path.basename(path)
    # 拡張子を除いてアンダースコアで分割
    name_no_ext = base[:-3] if base.endswith(".md") else base
    if "_" not in name_no_ext:
        return issues  # 規約外のファイル名(検証対象外)
    name_doc_id = name_no_ext.split("_", 1)[0]
    if name_doc_id != fm_doc_id:
        issues.append(Issue("ファイル名整合", path,
                            f"ファイル名先頭の '{name_doc_id}' と frontmatter doc_id '{fm_doc_id}' が不一致"))
    return issues


# 「承認済み相当」とみなす状態(harness/01_selection_rules.md 末尾の状態値表より)
# 蓄積中(ADR)は常に「使える」状態として扱う。
APPROVED_STATUSES = {"承認済", "取り込み済", "ゲート2承認", "蓄積中"}

# 本書の状態がこれらのときは、依存先の承認状態を問わない(まだ未着手 / 省略 / 委譲のため)
SELF_NOT_STARTED_STATUSES = {"未着手", "省略", "委譲", ""}


def _parse_depends_on(fm):
    """frontmatter の depends_on 値('[R-1, R-13]' / '[]' / 'R-1' 等)をID列に正規化。"""
    if not fm or "depends_on" not in fm:
        return []
    raw = fm["depends_on"].strip()
    if raw.startswith("[") and raw.endswith("]"):
        raw = raw[1:-1]
    return [x.strip() for x in raw.split(",") if x.strip()]


def check_depends_on(path, fm, plan, plan_exists):
    """frontmatter depends_on の妥当性を確認(v0.9〜)。

    1. depends_on に列挙されたIDが _doc_plan.md に存在するか(誤記検出)
    2. 本書の状態が「進行中 / 作成済 / レビュー中 / 承認済」のとき、
       依存先が「承認済 / 取り込み済 / ゲート2承認 / 蓄積中」のいずれかになっているか
       (= Step B「依存関係確認」の機械化)

    本書が「未着手 / 省略 / 委譲」のときは依存先の承認状態を問わない。
    plan が無い案件(初期状態)では本検査をスキップ。
    """
    issues = []
    if not plan_exists or fm is None or "doc_id" not in fm:
        return issues
    doc_id = fm["doc_id"].strip()
    self_status = plan.get(doc_id, "")
    deps = _parse_depends_on(fm)
    for dep in deps:
        if dep not in plan:
            issues.append(Issue("依存検証", path,
                                f"depends_on の '{dep}' が _doc_plan に存在しない(誤記の可能性)"))
            continue
        if self_status in SELF_NOT_STARTED_STATUSES:
            continue  # 本書が未着手のときは依存先の承認状態を問わない
        dep_status = plan[dep]
        if dep_status not in APPROVED_STATUSES:
            issues.append(Issue("依存検証", path,
                                f"depends_on の '{dep}' が未承認(現状: '{dep_status}')。本書は '{self_status}' のため、前提が揃う前に下流に進んでいる可能性"))
    return issues


def check_adr_index(output_dir):
    """output/横断/ADR/ がある案件で、ADR ファイル群と _index.md の整合を確認(v0.9〜)。

    検出する不整合:
      - ADR ファイルが存在するのに _index.md が無い
      - _index.md に載っている ADR-NNNN に対応するファイルが無い(索引のゴースト)
      - ADR ファイルが _index.md に未掲載(索引漏れ)
      - ADR ファイルの frontmatter `status` が未記入

    ADR ディレクトリ自体が無い案件(ADR 未使用)では本検査をスキップ。
    """
    issues = []
    adr_dir = os.path.join(output_dir, "横断", "ADR")
    if not os.path.isdir(adr_dir):
        return issues
    index_path = os.path.join(adr_dir, "_index.md")
    adr_files = sorted(glob.glob(os.path.join(adr_dir, "ADR-*_*.md")))
    # frontmatter status を取りつつ、ADR-NNNN を抽出
    adr_in_files = {}
    for f in adr_files:
        base = os.path.basename(f)
        m = re.match(r"(ADR-\d{4})_", base)
        if not m:
            continue
        text = read_text(f)
        fm = parse_frontmatter(text)
        status = (fm.get("status", "").strip() if fm else "")
        adr_in_files[m.group(1)] = (f, status)
    # _index.md 解析
    if not os.path.exists(index_path):
        if adr_files:
            issues.append(Issue("ADR 突合", adr_dir,
                                f"ADR ファイルが {len(adr_files)} 件あるが _index.md が無い"))
        return issues
    # _index.md は索引「表」を一次情報とする。説明文や凡例の地の文中に
    # 偶然 ADR-NNNN が出ても誤検出しないよう、表セル限定で抽出する。
    adr_in_index = set()
    for cells in parse_markdown_table(index_path)[1:]:  # ヘッダ行除く
        for cell in cells:
            for hit in re.findall(r"\bADR-\d{4}\b", cell):
                adr_in_index.add(hit)
    # ファイル → 索引の方向
    for adr_id, (f, status) in adr_in_files.items():
        if adr_id not in adr_in_index:
            issues.append(Issue("ADR 突合", f,
                                f"'{adr_id}' が _index.md に未掲載(索引漏れ)"))
        if not status:
            issues.append(Issue("ADR 突合", f,
                                f"'{adr_id}' の frontmatter `status` が未記入"))
    # 索引 → ファイルの方向
    for adr_id in adr_in_index:
        if adr_id not in adr_in_files:
            issues.append(Issue("ADR 突合", index_path,
                                f"_index.md に '{adr_id}' の記載があるが対応する ADR ファイルが無い"))
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
# テストマニフェスト突合(v0.13・Phase 3.5 ゲート2の補強)
# ===================================================================

def check_test_manifest(output_dir):
    """_handoff_to_implementation/_test_manifest.md と D-15 / TS-1 の UT-* / AT-* を突合(v0.13〜)。

    Phase 3.5 ゲート2(Red コード引き渡し)で生成される `_test_manifest.md` が、
    テスト仕様(D-15 の UT-* / TS-1 の AT-*)と過不足なく対応しているかを確認する。

    検出する不整合:
      - 掲載漏れ : D-15 / TS-1 で定義された UT-* / AT-* が _test_manifest に載っていない
      - ゴースト : _test_manifest に載っている UT-* / AT-* が D-15 / TS-1 に定義されていない

    スキップ条件:
      - _test_manifest.md が無い(TDD 不採用 / ゲート2前)案件
      - _test_manifest に UT-* / AT-* がまだ無い(雛形のみ / プレースホルダ段階)
      - 突合する側の仕様(UT は D-15、AT は TS-1)が存在しない方向は判定しない
    """
    issues = []
    manifest_path = os.path.join(output_dir, "_handoff_to_implementation", "_test_manifest.md")
    if not os.path.exists(manifest_path):
        return issues

    # マニフェストの表セルから UT-* / AT-* を抽出(地の文の誤検出を避けるため表セル限定)
    manifest_ids = set()
    for cells in parse_markdown_table(manifest_path)[1:]:  # ヘッダ行除く
        for cell in cells:
            if "{{" in cell:
                continue  # テンプレのプレースホルダ行
            for hit in re.findall(r"\b(?:UT|AT)-\d{3,}\b", cell):
                manifest_ids.add(hit)
    manifest_ut = {x for x in manifest_ids if x.startswith("UT-")}
    manifest_at = {x for x in manifest_ids if x.startswith("AT-")}
    if not manifest_ids:
        return issues  # 雛形のみ。ゲート2未実施として警告しない

    # 定義側: D-15 の UT-* / TS-1 の AT-*(本文全体から拾う。TS-1 の AT 収集に倣う)
    d15_path = find_doc(output_dir, "D-15")
    ts1_path = find_doc(output_dir, "TS-1")
    ut_defined = set(re.findall(r"\bUT-\d{3,}\b", read_text(d15_path))) if d15_path else None
    at_defined = set(re.findall(r"\bAT-\d{3,}\b", read_text(ts1_path))) if ts1_path else None

    # 掲載漏れ(定義 → マニフェスト)
    if ut_defined is not None:
        for uid in sorted(ut_defined - manifest_ut):
            issues.append(Issue("テストマニフェスト", manifest_path,
                                f"D-15 で定義された '{uid}' が _test_manifest に未掲載(引き渡し漏れの可能性)"))
    if at_defined is not None:
        for aid in sorted(at_defined - manifest_at):
            issues.append(Issue("テストマニフェスト", manifest_path,
                                f"TS-1 で定義された '{aid}' が _test_manifest に未掲載(引き渡し漏れの可能性)"))

    # ゴースト(マニフェスト → 定義)。突合先が存在する方向のみ判定する
    if ut_defined is not None:
        for uid in sorted(manifest_ut - ut_defined):
            issues.append(Issue("テストマニフェスト", manifest_path,
                                f"_test_manifest の '{uid}' が D-15 に定義されていない(ゴースト)"))
    if at_defined is not None:
        for aid in sorted(manifest_at - at_defined):
            issues.append(Issue("テストマニフェスト", manifest_path,
                                f"_test_manifest の '{aid}' が TS-1 に定義されていない(ゴースト)"))
    return issues


# ===================================================================
# 用語整合(v0.10)
# ===================================================================

def check_glossary(output_dir, docs):
    """R-13 用語集の「使用禁止語」が他ドキュメント本文に出現していないか確認(v0.10〜)。

    R-13 の表から「用語」と「使用禁止語」の対応を抽出し、
    使用禁止語を含むドキュメント(R-13 自身を除く)を警告する。
    1ファイル × 1禁止語につき最大1件の指摘(過剰な警告を避ける)。

    R-13 が存在しない案件 / 表の列構造が想定外の案件 / 禁止語列が空の案件はスキップ。
    プレースホルダ行(`{{` を含む)も除外。
    """
    issues = []
    r13_path = find_doc(output_dir, "R-13")
    if r13_path is None:
        return issues
    rows = parse_markdown_table(r13_path)
    if len(rows) <= 1:
        return issues
    header = rows[0]

    def col_idx(*needles):
        for i, h in enumerate(header):
            if any(n in h for n in needles):
                return i
        return None

    term_col = col_idx("用語")
    forbidden_col = col_idx("使用禁止")
    if term_col is None or forbidden_col is None:
        return issues  # 表構造が想定と違う(v0.10 列規約: 用語 / 使用禁止語 / ...)

    forbidden_map = {}  # forbidden_word -> canonical_term
    for cells in rows[1:]:
        if len(cells) <= max(term_col, forbidden_col):
            continue
        term = cells[term_col].strip()
        forbidden_raw = cells[forbidden_col].strip()
        if "{{" in term or "{{" in forbidden_raw:
            continue  # テンプレのプレースホルダ
        if not term or not forbidden_raw or forbidden_raw in ("—", "-", "", "なし"):
            continue
        # "注文(本書では受注に統一)" や "注文(本書では受注に統一)" から主語のみ抽出
        main = re.split(r"[（(]", forbidden_raw, 1)[0].strip()
        if main:
            forbidden_map[main] = term

    if not forbidden_map:
        return issues

    for path in docs:
        if path == r13_path:
            continue
        try:
            with open(path, encoding="utf-8") as f:
                lines = f.read().splitlines()
        except OSError:
            continue
        for forbidden_word, canonical in forbidden_map.items():
            for i, line in enumerate(lines, 1):
                stripped = line.strip()
                # 見出し・frontmatter区切り・コメント風の行は除外
                if stripped.startswith("#") or stripped.startswith("---") or stripped.startswith(">"):
                    continue
                if forbidden_word in line:
                    issues.append(Issue("用語整合", path,
                                        f"使用禁止語 '{forbidden_word}' が出現(R-13 で '{canonical}' に統一)",
                                        line=i))
                    break  # 1ファイル × 1禁止語 で1件のみ
    return issues


# ===================================================================
# 循環検出(v0.10)
# ===================================================================

def check_circular_deps(docs):
    """全ドキュメントの frontmatter depends_on を集約し循環参照を検出(v0.10〜)。

    DFS で WHITE/GRAY/BLACK 三色塗りし、GRAY ノードへの後退辺で循環を検出。
    検出した循環は正規化(集合化)して重複報告を抑制。
    検出された循環ごとに、起点ドキュメントのパスに対して 1 件の指摘を出す。
    """
    issues = []
    graph = {}  # doc_id -> [dep_id, ...]
    doc_id_to_path = {}
    for path in docs:
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except OSError:
            continue
        fm = parse_frontmatter(text)
        if fm is None or "doc_id" not in fm:
            continue
        doc_id = fm["doc_id"].strip()
        graph[doc_id] = _parse_depends_on(fm)
        doc_id_to_path[doc_id] = path

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {n: WHITE for n in graph}
    found_cycles = []

    def dfs(node, stack):
        color[node] = GRAY
        stack.append(node)
        for dep in graph.get(node, []):
            if dep not in graph:
                continue  # 外部参照(本書として未登場のID)はスキップ
            c = color.get(dep, WHITE)
            if c == GRAY:
                # 循環: stack 中の dep 出現位置から閉路を切り出す
                idx = stack.index(dep)
                found_cycles.append(stack[idx:] + [dep])
            elif c == WHITE:
                dfs(dep, stack)
        stack.pop()
        color[node] = BLACK

    for n in list(graph.keys()):
        if color[n] == WHITE:
            dfs(n, [])

    # 同じ循環(開始点違いの並び替え)を重複排除
    seen = set()
    for cyc in found_cycles:
        key = tuple(sorted(set(cyc)))
        if key in seen:
            continue
        seen.add(key)
        arrow = " → ".join(cyc)
        # 起点ドキュメントのパスを指す(無ければ最初のノード)
        ref_path = doc_id_to_path.get(cyc[0], "(complex)")
        issues.append(Issue("循環検出", ref_path,
                            f"depends_on に循環参照: {arrow}"))
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
# セッションログ補助(v0.11)
# ===================================================================

def cmd_session_start(output_dir):
    """直近セッションのログ末尾エントリを stdout に出力。

    output/_session_log.md を読み、最後の `## YYYY-MM-DD Session N ...` 見出し以降を表示する。
    エントリが無い(初回セッション)場合はその旨を案内する。
    """
    log_path = os.path.join(output_dir, "_session_log.md")
    if not os.path.exists(log_path):
        print("# セッションログ未作成")
        print("")
        print(f"{log_path} がありません。初回セッションのときは作業終了時に")
        print("`python harness/tools/check.py --session-end` でテンプレを取得して追記してください。")
        return 0
    with open(log_path, encoding="utf-8") as f:
        lines = f.read().splitlines()
    # 最後の "## YYYY-MM-DD Session" 見出しを探す
    last_idx = None
    for i, line in enumerate(lines):
        if re.match(r"^## \d{4}-\d{2}-\d{2} Session\b", line.strip()):
            last_idx = i
    if last_idx is None:
        print("# セッションエントリ未記入")
        print("")
        print(f"{log_path} にまだセッションエントリがありません(雛形のみ)。")
        print("初回セッションとして扱ってください。`--session-end` でテンプレ取得。")
        return 0
    # 末尾エントリを最後まで(次の "## " かファイル末尾まで)出力
    end_idx = len(lines)
    for j in range(last_idx + 1, len(lines)):
        if lines[j].startswith("## ") and not lines[j].startswith("## " + lines[last_idx][3:13]):
            end_idx = j
            break
    print("# 直近セッションログ(末尾エントリ)")
    print("")
    for line in lines[last_idx:end_idx]:
        print(line)
    return 0


def cmd_session_end(output_dir):
    """新規セッションエントリのテンプレを stdout に出力。

    自動算出: 日付 / セッション番号 / check.py の現在結果 / _doc_plan から完了済 / 進行中 のリスト。
    残りはユーザー / Claude が手で埋めてから _session_log.md に追記する。
    """
    # 日付(JST)
    jst = timezone(timedelta(hours=9))
    today = datetime.now(jst).strftime("%Y-%m-%d")

    # セッション番号: 既存ログから推定
    log_path = os.path.join(output_dir, "_session_log.md")
    next_n = 1
    if os.path.exists(log_path):
        with open(log_path, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"^## \d{4}-\d{2}-\d{2} Session (\d+)\b", line.strip())
                if m:
                    next_n = max(next_n, int(m.group(1)) + 1)

    # _doc_plan から「承認済」と「進行中」のリストを抽出
    plan, plan_exists = load_doc_plan(output_dir)
    done = []
    in_progress = []
    if plan_exists:
        for did, status in plan.items():
            if status == "承認済":
                done.append(did)
            elif status in ("進行中", "レビュー中", "作成済", "ゲート1承認", "Red作成済"):
                in_progress.append(did)

    # check.py 結果のサマリ(別プロセスを呼ばずに簡易計算)
    # ここでは「最終結果の数値」までは出さず、ユーザーに "実行して埋めて" と案内
    print(f"## {today} Session {next_n} (タイトル: 何を進めたか1行で書く)")
    print(f"- 完了: " + (", ".join(sorted(done)) if done else "(なし)"))
    print(f"- 進行中: " + (", ".join(sorted(in_progress)) if in_progress else "(なし — 次セッション着手分)"))
    print(f"- 次の開始点: (どのドキュメントから着手するか)")
    print(f"- 意思決定メモ:")
    print(f"  - (ADR を切るほどではない設計判断・スコープ変更・小さな合意 を記録)")
    print(f"- 残 TBD: (`python harness/tools/check.py --tbd` で `_tbd_dashboard.md` を更新して内容を確認)")
    print(f"- check.py: (`python harness/tools/check.py {output_dir}` の最終行をコピー)")
    print(f"- 関連コミット: (このセッションをまとめる commit のハッシュ)")
    print("")
    print("# ↑ 上記をコピーし、必要箇所を埋めて `output/_session_log.md` の末尾に追記してください。")
    return 0


# ===================================================================
# メイン
# ===================================================================

def main():
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0

    do_tbd = "--tbd" in sys.argv
    do_json = "--json" in sys.argv
    do_color = "--color" in sys.argv
    do_session_start = "--session-start" in sys.argv
    do_session_end = "--session-end" in sys.argv
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    output_dir = args[0] if args else "output"
    if not os.path.isdir(output_dir):
        if do_json:
            print(json.dumps({"output_dir": output_dir, "error": "directory_not_found",
                              "ok": False, "issues": [], "total": 0},
                             ensure_ascii=False, indent=2))
        else:
            print(f"ERROR: ディレクトリが見つかりません: {output_dir}")
        return 2

    # セッション補助モードは検証を行わず単独で動作
    if do_session_start:
        return cmd_session_start(output_dir)
    if do_session_end:
        return cmd_session_end(output_dir)

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
        issues += check_filename_vs_doc_id(path, fm)
        issues += check_depends_on(path, fm, plan, plan_exists)

    # 横断: 孤立検出(R-14 RTM があるとき) / AC/AT 網羅(TS-1 があるとき) / ADR 突合 /
    #       用語整合(R-13 があるとき)/ 循環検出
    issues += check_orphans(output_dir, registry_ids)
    issues += check_tdd_coverage(output_dir, registry_ids)
    issues += check_test_manifest(output_dir)
    issues += check_adr_index(output_dir)
    issues += check_glossary(output_dir, docs)
    issues += check_circular_deps(docs)

    # TBD 集約(オプション)
    tbd_path = None
    tbd_count = 0
    if do_tbd:
        tbd_entries = aggregate_tbd(output_dir, docs)
        tbd_count = len(tbd_entries)
        tbd_path = write_tbd_dashboard(output_dir, tbd_entries)

    # ---- 出力 ----
    if do_json:
        return render_json(output_dir, docs, registry_ids, reg_exists,
                           plan_exists, issues, do_tbd, tbd_count, tbd_path)
    return render_text(output_dir, docs, registry_ids, reg_exists,
                       plan_exists, issues, do_tbd, tbd_count, tbd_path, do_color)


# ===================================================================
# 出力レンダラ(v0.13: テキスト / JSON / カラー)
# ===================================================================

# ANSI カラーコード(--color 指定時のみ使用)
_ANSI = {
    "error": "\033[31m",    # 赤
    "warning": "\033[33m",  # 黄
    "ok": "\033[32m",       # 緑
    "dim": "\033[2m",
    "reset": "\033[0m",
}


def _paint(text, key, enable):
    if not enable:
        return text
    return f"{_ANSI.get(key, '')}{text}{_ANSI['reset']}"


def render_text(output_dir, docs, registry_ids, reg_exists,
                plan_exists, issues, do_tbd, tbd_count, tbd_path, do_color):
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
        print("  " + _paint("✅ 機械チェックは問題なし", "ok", do_color))
        print("-" * 64)
        print("  注意: 検証したのは形式・参照・整合のみ。")
        print("  意味の妥当性(要件の正しさ・期待結果の妥当性)は別途レビューが必要です。")
        return 0

    n_error = sum(1 for i in issues if i.severity == "error")
    n_warning = len(issues) - n_error

    by_kind = {}
    for iss in issues:
        by_kind.setdefault(iss.kind, []).append(iss)
    for kind in sorted(by_kind, key=lambda k: (SEVERITY_BY_KIND.get(k, "error") != "error", k)):
        sev = SEVERITY_BY_KIND.get(kind, "error")
        head = f"  ● [{sev}] {kind}: {len(by_kind[kind])} 件"
        print(_paint(head, sev, do_color))
        for iss in by_kind[kind]:
            print(_paint(str(iss), sev, do_color))
        print()
    print("-" * 64)
    summary = f"  ❌ 合計 {len(issues)} 件の問題を検出(error {n_error} / warning {n_warning}・意味の妥当性は別途レビュー)"
    print(_paint(summary, "error" if n_error else "warning", do_color))
    return 1


def render_json(output_dir, docs, registry_ids, reg_exists,
                plan_exists, issues, do_tbd, tbd_count, tbd_path):
    """検証結果を機械可読な JSON で stdout に出力(CI 連携用)。"""
    n_error = sum(1 for i in issues if i.severity == "error")
    n_warning = len(issues) - n_error
    by_kind = defaultdict(int)
    for iss in issues:
        by_kind[iss.kind] += 1
    payload = {
        "output_dir": output_dir,
        "ok": not issues,
        "summary": {
            "docs": len(docs),
            "registry_ids": len(registry_ids),
            "registry_exists": reg_exists,
            "plan_exists": plan_exists,
            "total": len(issues),
            "error": n_error,
            "warning": n_warning,
            "by_kind": dict(by_kind),
        },
        "issues": [
            {
                "kind": iss.kind,
                "severity": iss.severity,
                "path": iss.path.replace(os.sep, "/"),
                "line": iss.line,
                "message": iss.message,
            }
            for iss in issues
        ],
    }
    if do_tbd:
        payload["tbd"] = {"count": tbd_count,
                          "path": (tbd_path.replace(os.sep, "/") if tbd_path else None)}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not issues else 1


if __name__ == "__main__":
    sys.exit(main())
