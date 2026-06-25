"""
harness/spec/i18n_labels.py — 言語別ラベル(v0.11〜)

テンプレ全体で共通的に使う見出し・ラベル・フレーズの翻訳辞書。
各テンプレ固有の本文(section 4 配下の content)は本ファイルには持たず、
spec/templates.py の section4_titles と、生成後の手動加筆で対応する。
"""

LABELS = {
    "ja": {
        # frontmatter 表記
        "phase": {
            "pre_study": "事前検討",
            "planning": "企画",
            "requirements": "要件定義",
            "basic_design": "基本設計",
            "detailed_design": "詳細設計",
            "testing": "テスト",
            "crosscut": "横断",
        },
        "required_when": {
            "all_scales_all_methods": "全規模・全手法で必須",
            "wf_or_hybrid_upstream_required": "WF / ハイブリッド上流で必須(アジャイル単独運用では R-7 で代替可)",
            "agile_required": "アジャイル開発で必須(WF採用時は R-8 を主入口とする)",
            "crosscut_required": "横断で必須",
            "agile_recommended": "アジャイルで推奨",
            "wf_required_agile_lightweight": "WF / ハイブリッド上流で必須 / アジャイルで軽量版",
            "mid_scale_recommended": "中規模以上で推奨 / 金融・医療・公共では小規模でも必須 / TDD採用時はテストID列を充填",
            "bpr_required": "BPR時必須",
        },
        "mode": {
            "both": "両対応",
            "wf": "WF",
            "agile": "Agile",
        },
        # 共通の節見出し
        "section1": "## 1. 目的",
        "section2": "## 2. 適用範囲・スコープ",
        "section3": "## 3. 前提・依存",
        "section4": "## 4. 本文",
        "section5": "## 5. 関連トレーサビリティ",
        "section6": "## 6. 改訂履歴",
        "section7": "## 7. レビュー状態",
        # 共通プレースホルダ
        "title_prefix": "{{案件名}}",
        "scope_includes": "- 含むもの: {{...}}",
        "scope_excludes": "- 含まないもの: {{...}}",
        "prereqs_refs": "- 参照ドキュメント: {{depends_on のID と名称}}",
        "prereqs_ids": "- 採番済ID: {{利用する機能ID、エンティティID等を列挙}}",
        "trace_upstream": "- 上流(本書の根拠となる要求・要件):",
        "trace_downstream": "- 下流(本書を参照する設計・テスト):",
        "changelog_header": "| 版 | 日付 | 変更者 | 変更内容 |",
        "changelog_sep": "|---|---|---|---|",
        "changelog_first_row": "| 0.1 | YYYY-MM-DD | | 初版作成 |",
        "review_state_lines": [
            "- 単体品質チェック: 未 / 実施済(YYYY-MM-DD)",
            "- 整合性チェック: 未 / 実施済(YYYY-MM-DD)",
            "- TBD / 残課題:",
            "  - (なし、または箇条書き)",
            "- 承認: 未 / 承認(承認者、日付)",
        ],
        "example_label": "### 補足: 記入例(参考)",
        "tbd_placeholder": "{{TBD: ユーザーと内容を確認して埋める}}",
    },
    "en": {
        # frontmatter labels
        "phase": {
            "pre_study": "Pre-study",
            "planning": "Planning",
            "requirements": "Requirements",
            "basic_design": "Basic Design",
            "detailed_design": "Detailed Design",
            "testing": "Testing",
            "crosscut": "Cross-cutting",
        },
        "required_when": {
            "all_scales_all_methods": "Required for all scales and methodologies",
            "wf_or_hybrid_upstream_required": "Required for WF / hybrid upstream (replaceable by R-7 in pure Agile)",
            "agile_required": "Required for Agile (use R-8 as primary entry in WF)",
            "crosscut_required": "Required (cross-cutting)",
            "agile_recommended": "Recommended for Agile",
            "wf_required_agile_lightweight": "Required for WF; lightweight version OK for Agile",
            "mid_scale_recommended": "Recommended for mid-scale or larger; required for finance/healthcare/public sector even at small scale; fill test ID column when TDD is used",
            "bpr_required": "Required when BPR is involved",
        },
        "mode": {
            "both": "Both",
            "wf": "WF",
            "agile": "Agile",
        },
        # Common section headings
        "section1": "## 1. Purpose",
        "section2": "## 2. Scope",
        "section3": "## 3. Prerequisites & Dependencies",
        "section4": "## 4. Body",
        "section5": "## 5. Traceability",
        "section6": "## 6. Revision History",
        "section7": "## 7. Review Status",
        # Common placeholders
        "title_prefix": "{{Project Name}}",
        "scope_includes": "- In scope: {{...}}",
        "scope_excludes": "- Out of scope: {{...}}",
        "prereqs_refs": "- Reference documents: {{IDs and names listed in depends_on}}",
        "prereqs_ids": "- Already-issued IDs: {{Enumerate function IDs, entity IDs, etc. used in this document}}",
        "trace_upstream": "- Upstream (basis of this document):",
        "trace_downstream": "- Downstream (designs / tests that reference this document):",
        "changelog_header": "| Rev | Date | Author | Changes |",
        "changelog_sep": "|---|---|---|---|",
        "changelog_first_row": "| 0.1 | YYYY-MM-DD | | Initial draft |",
        "review_state_lines": [
            "- Single-document quality check: Not done / Done (YYYY-MM-DD)",
            "- Consistency check: Not done / Done (YYYY-MM-DD)",
            "- TBD / Open items:",
            "  - (none, or bullet list)",
            "- Approval: Not approved / Approved (approver, date)",
        ],
        "example_label": "### Appendix: Example (for reference)",
        "tbd_placeholder": "{{TBD: confirm with user before filling}}",
    },
}


def get_labels(lang):
    """指定言語のラベル辞書を取得。未対応言語なら ja を返す。"""
    return LABELS.get(lang, LABELS["ja"])
