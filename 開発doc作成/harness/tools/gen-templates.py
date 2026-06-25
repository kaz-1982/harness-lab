#!/usr/bin/env python3
"""
harness/tools/gen-templates.py — テンプレ DSL ジェネレータ(v0.11〜)

役割:
  1. `--list`   仕様(harness/spec/templates.py)に登録されたテンプレ一覧と
                各言語パックの有無を表示
  2. `--check`  既存の `harness/templates/{lang}/*.md`(または `templates/*.md`
                を ja として)を仕様と突合。frontmatter のメタ情報がズレていれば
                警告(構造変更時の取りこぼし検出)
  3. `--stub`  指定テンプレの雛形を stdout に出力(セクション7つの骨組みのみ)
                既存テンプレ(日本語版)は置き換えず、新言語版を起こすときに利用

使い方:
  python3 harness/tools/gen-templates.py --list
  python3 harness/tools/gen-templates.py --list --lang en
  python3 harness/tools/gen-templates.py --check
  python3 harness/tools/gen-templates.py --check --lang en
  python3 harness/tools/gen-templates.py --stub R-1 --lang en

設計方針(v0.11):
  - **既存テンプレを置き換えない**。本ツールは検証と雛形生成のみ。
  - 言語パックが無いテンプレは、その言語向けには何もしない(エラーにしない)。
  - stdlib のみで実装(yaml / toml 等の追加依存なし)。
"""

import os
import re
import sys

# Windows の cp932 環境でも記号類を出力できるよう stdout を UTF-8 化
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# spec/ をインポートパスに追加
HARNESS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HARNESS_DIR)

from spec.templates import TEMPLATES, list_templates  # noqa: E402
from spec.i18n_labels import get_labels  # noqa: E402


TEMPLATES_DIR = os.path.join(HARNESS_DIR, "templates")


# ---------------------------------------------------------------
# ファイル探索
# ---------------------------------------------------------------

def find_existing_template(doc_id, lang):
    """既存のテンプレファイルパスを返す。

    優先順:
      1. harness/templates/{lang}/{doc_id}_*.md
      2. lang == "ja" のときのみ、互換のため harness/templates/{doc_id}_*.md
    """
    lang_dir = os.path.join(TEMPLATES_DIR, lang)
    if os.path.isdir(lang_dir):
        for name in os.listdir(lang_dir):
            if name.startswith(f"{doc_id}_") and name.endswith(".md"):
                return os.path.join(lang_dir, name)
    if lang == "ja":
        # 互換: ja は templates/ 直下も探す(v0.10 以前の配置)
        for name in os.listdir(TEMPLATES_DIR):
            if name.startswith(f"{doc_id}_") and name.endswith(".md"):
                return os.path.join(TEMPLATES_DIR, name)
    return None


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm


# ---------------------------------------------------------------
# --list
# ---------------------------------------------------------------

def cmd_list(lang=None):
    print(f"テンプレ仕様の中央台帳(harness/spec/templates.py)")
    print(f"既存テンプレ配置: {TEMPLATES_DIR}/(ja は templates/ 直下 or templates/ja/)")
    print("")
    if lang:
        print(f"言語 '{lang}' に絞り込み:")
    print(f"{'ID':<6} {'phase':<18} {'mode':<8} {'ja':<4} {'en':<4} 名称(ja)")
    print("-" * 72)
    for doc_id in list_templates():
        t = TEMPLATES[doc_id]
        has_ja = "✓" if "ja" in t["names"] else "—"
        has_en = "✓" if "en" in t["names"] else "—"
        if lang and lang not in t["names"]:
            continue
        name_ja = t["names"].get("ja", "(no ja)")
        print(f"{doc_id:<6} {t['phase_key']:<18} {t['mode_key']:<8} {has_ja:<4} {has_en:<4} {name_ja}")


# ---------------------------------------------------------------
# --check
# ---------------------------------------------------------------

def cmd_check(lang):
    """仕様と既存テンプレの frontmatter を突合し、不一致を報告"""
    labels = get_labels(lang)
    issues = []
    checked = 0
    skipped = 0
    for doc_id, spec in TEMPLATES.items():
        if lang not in spec["names"]:
            skipped += 1
            continue
        path = find_existing_template(doc_id, lang)
        if path is None:
            issues.append(f"{doc_id}: 仕様には {lang} 版があるが、ファイルが見つからない")
            continue
        with open(path, encoding="utf-8") as f:
            text = f.read()
        fm = parse_frontmatter(text)
        if fm is None:
            issues.append(f"{doc_id} ({path}): frontmatter が無い")
            continue
        checked += 1
        # 突合
        expected = {
            "doc_id": doc_id,
            "doc_name": spec["names"][lang],
            "phase": labels["phase"][spec["phase_key"]],
            "required_when": labels["required_when"][spec["required_when_key"]],
            "depends_on": "[" + ", ".join(spec["depends_on"]) + "]",
            "mode": labels["mode"][spec["mode_key"]],
        }
        for key, exp in expected.items():
            actual = fm.get(key, "(missing)").strip()
            # depends_on は順序フリーで比較
            if key == "depends_on":
                actual_set = set(s.strip() for s in actual.strip("[] ").split(",") if s.strip())
                exp_set = set(spec["depends_on"])
                if actual_set != exp_set:
                    issues.append(f"{doc_id} ({path}): frontmatter {key} = {actual!r}, spec = {exp!r}")
            elif actual != exp:
                issues.append(f"{doc_id} ({path}): frontmatter {key} = {actual!r}, spec = {exp!r}")

    print(f"--check lang={lang}: 検証 {checked} 件、仕様に {lang} 版なしのためスキップ {skipped} 件")
    if not issues:
        print("✅ 仕様と既存テンプレ frontmatter は一致")
        return 0
    print(f"❌ {len(issues)} 件の不一致を検出")
    for msg in issues:
        print("   " + msg)
    return 1


# ---------------------------------------------------------------
# --stub
# ---------------------------------------------------------------

def render_stub(doc_id, lang):
    """テンプレの雛形を文字列として返す(stdout 用)"""
    if doc_id not in TEMPLATES:
        return None
    spec = TEMPLATES[doc_id]
    if lang not in spec["names"]:
        return None
    labels = get_labels(lang)

    out = []
    # frontmatter
    out.append("---")
    out.append(f"doc_id: {doc_id}")
    out.append(f"doc_name: {spec['names'][lang]}")
    out.append(f"phase: {labels['phase'][spec['phase_key']]}")
    out.append(f"required_when: {labels['required_when'][spec['required_when_key']]}")
    out.append(f"depends_on: [" + ", ".join(spec["depends_on"]) + "]")
    out.append(f"mode: {labels['mode'][spec['mode_key']]}")
    out.append("---")
    out.append("")
    out.append(f"# {labels['title_prefix']} - {spec['names'][lang]}")
    out.append("")
    # 1. Purpose
    out.append(labels["section1"])
    out.append(labels["tbd_placeholder"])
    out.append("")
    # 2. Scope
    out.append(labels["section2"])
    out.append(labels["scope_includes"])
    out.append(labels["scope_excludes"])
    out.append("")
    # 3. Prereqs
    out.append(labels["section3"])
    out.append(labels["prereqs_refs"])
    out.append(labels["prereqs_ids"])
    out.append("")
    # 4. Body — section4_titles
    out.append(labels["section4"])
    out.append("")
    for title in spec["section4_titles"].get(lang, []):
        out.append(f"### {title}")
        out.append(labels["tbd_placeholder"])
        out.append("")
    # 5. Traceability
    out.append(labels["section5"])
    out.append(labels["trace_upstream"])
    out.append(f"  - {labels['tbd_placeholder']}")
    out.append(labels["trace_downstream"])
    out.append(f"  - {labels['tbd_placeholder']}")
    out.append("")
    # 6. Revision history
    out.append(labels["section6"])
    out.append(labels["changelog_header"])
    out.append(labels["changelog_sep"])
    out.append(labels["changelog_first_row"])
    out.append("")
    # 7. Review state
    out.append(labels["section7"])
    for line in labels["review_state_lines"]:
        out.append(line)

    return "\n".join(out) + "\n"


def cmd_stub(doc_id, lang):
    text = render_stub(doc_id, lang)
    if text is None:
        spec = TEMPLATES.get(doc_id)
        if spec is None:
            print(f"ERROR: 仕様に '{doc_id}' が存在しません。--list で一覧を確認してください。", file=sys.stderr)
        else:
            print(f"ERROR: '{doc_id}' は '{lang}' 版を仕様に持ちません。", file=sys.stderr)
            available = [l for l in spec["names"]]
            print(f"       利用可能な言語: {available}", file=sys.stderr)
        return 1
    print(text)
    return 0


# ---------------------------------------------------------------
# main
# ---------------------------------------------------------------

def main():
    if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) == 1:
        print(__doc__)
        return 0

    # --lang
    lang = "ja"
    if "--lang" in sys.argv:
        idx = sys.argv.index("--lang")
        if idx + 1 < len(sys.argv):
            lang = sys.argv[idx + 1]

    if "--list" in sys.argv:
        cmd_list(lang if "--lang" in sys.argv else None)
        return 0
    if "--check" in sys.argv:
        return cmd_check(lang)
    if "--stub" in sys.argv:
        idx = sys.argv.index("--stub")
        if idx + 1 >= len(sys.argv) or sys.argv[idx + 1].startswith("--"):
            print("ERROR: --stub <doc_id> を指定してください(例: --stub R-1)", file=sys.stderr)
            return 1
        return cmd_stub(sys.argv[idx + 1], lang)

    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
