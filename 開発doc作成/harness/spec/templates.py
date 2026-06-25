"""
harness/spec/templates.py — テンプレ仕様の中央台帳(v0.11〜)

このモジュールは、`harness/templates/{lang}/{doc_id}_*.md` 群が満たすべき
メタ情報を一元的に保持する。`harness/tools/gen-templates.py` が本ファイルを
参照して整合性検証(--check)や新言語版の雛形生成(--stub)を行う。

設計方針:
  - **既存の `harness/templates/*.md`(日本語版・原典)は本ファイルが置き換えない**。
    DSL の役割は「仕様の単一情報源」+「機械検証」+「他言語版の雛形生成」に絞る。
  - 各テンプレは `id` をキーとし、frontmatter のメタ情報(phase / depends_on / mode /
    required_when)と、本文の section 4 タイトル列を言語別に持つ。
  - 言語パックの抜けは許可する(例: en が無いテンプレは英語版を生成しない)。

i18n の対象:
  - メタ情報(phase / required_when / mode の本文表記、ドキュメント名)
  - section 4 の節タイトル
  - 共通の節見出し・ラベルは `harness/spec/i18n_labels.py` に分離
"""

# ---------------------------------------------------------------
# 共通キー(言語非依存)
# ---------------------------------------------------------------

# phase_key, required_when_key, mode_key の有効値(i18n_labels との対応用)
PHASE_KEYS = ("pre_study", "planning", "requirements", "basic_design",
              "detailed_design", "testing", "crosscut")

REQUIRED_WHEN_KEYS = (
    "all_scales_all_methods",          # 全規模・全手法で必須
    "wf_or_hybrid_upstream_required",  # WF / ハイブリッド上流で必須
    "agile_required",                  # アジャイル開発で必須
    "crosscut_required",               # 横断・全規模で必須
    "agile_recommended",               # アジャイルで推奨
    "wf_required_agile_lightweight",   # WF必須 / Agile軽量
    "mid_scale_recommended",           # 中規模以上で推奨
    "bpr_required",                    # BPR時必須
)

MODE_KEYS = ("both", "wf", "agile")


# ---------------------------------------------------------------
# テンプレ仕様(13 本)
# ---------------------------------------------------------------

TEMPLATES = {
    "R-1": {
        "phase_key": "requirements",
        "required_when_key": "all_scales_all_methods",
        "depends_on": ["PR-1"],
        "mode_key": "both",
        "names": {
            "ja": "業務要件定義書",
            "en": "Business Requirements Definition",
        },
        "section4_titles": {
            "ja": [
                "4.1 業務の目的・背景",
                "4.2 対象業務の範囲",
                "4.3 業務プロセスの概要",
                "4.4 業務ルール",
                "4.5 業務上のKPI・成功基準(業務要件ID R-B-*)",
                "4.6 ステークホルダー",
            ],
            "en": [
                "4.1 Business Purpose & Background",
                "4.2 Target Business Scope",
                "4.3 Business Process Overview",
                "4.4 Business Rules",
                "4.5 Business KPIs & Success Criteria (Business Requirement IDs R-B-*)",
                "4.6 Stakeholders",
            ],
        },
    },
    "R-7": {
        "phase_key": "requirements",
        "required_when_key": "agile_required",
        "depends_on": ["R-1", "R-13"],
        "mode_key": "agile",
        "names": {
            "ja": "ユーザーストーリー",
        },
        "section4_titles": {
            "ja": [
                "4.1 ストーリー一覧",
                "4.2 各ストーリーの受け入れ基準(AC)",
                "4.3 スプリント割付(任意)",
            ],
        },
    },
    "R-8": {
        "phase_key": "requirements",
        "required_when_key": "wf_or_hybrid_upstream_required",
        "depends_on": ["R-1", "R-5", "R-6", "R-13"],
        "mode_key": "wf",
        "names": {
            "ja": "機能要件定義書(SRS)",
        },
        "section4_titles": {
            "ja": [
                "4.1 機能一覧",
                "4.2 機能要件詳細(R-F-* / IEEE 830 様式)",
                "4.3 機能間の関係",
                "4.4 業務ルール(横断)",
            ],
        },
    },
    "R-9": {
        "phase_key": "requirements",
        "required_when_key": "all_scales_all_methods",
        "depends_on": ["R-1"],
        "mode_key": "both",
        "names": {
            "ja": "非機能要件定義書",
            "en": "Non-Functional Requirements Definition",
        },
        "section4_titles": {
            "ja": [
                "4.1 機能適合性(Functional Suitability)",
                "4.2 性能効率性(Performance Efficiency)",
                "4.3 互換性(Compatibility)",
                "4.4 使用性(Usability)",
                "4.5 信頼性(Reliability)",
                "4.6 セキュリティ(Security)",
                "4.7 保守性(Maintainability)",
                "4.8 移植性(Portability)",
            ],
            "en": [
                "4.1 Functional Suitability",
                "4.2 Performance Efficiency",
                "4.3 Compatibility",
                "4.4 Usability",
                "4.5 Reliability",
                "4.6 Security",
                "4.7 Maintainability",
                "4.8 Portability",
            ],
        },
    },
    "R-13": {
        "phase_key": "crosscut",
        "required_when_key": "all_scales_all_methods",
        "depends_on": [],
        "mode_key": "both",
        "names": {
            "ja": "用語集",
            "en": "Glossary",
        },
        "section4_titles": {
            "ja": [
                "4.1 用語一覧",
                "4.2 略語一覧",
                "4.3 表記ルール",
            ],
            "en": [
                "4.1 Terms",
                "4.2 Abbreviations",
                "4.3 Notation Rules",
            ],
        },
    },
    "R-14": {
        "phase_key": "crosscut",
        "required_when_key": "mid_scale_recommended",
        "depends_on": ["R-1", "R-8"],
        "mode_key": "both",
        "names": {
            "ja": "要求トレーサビリティマトリクス(RTM)",
        },
        "section4_titles": {
            "ja": [
                "4.1 トレーサビリティマトリクス",
                "4.2 孤立要件・孤立設計のチェック",
                "4.3 RTM の更新タイミング",
            ],
        },
    },
    "B-1": {
        "phase_key": "basic_design",
        "required_when_key": "wf_or_hybrid_upstream_required",
        "depends_on": ["R-8", "R-9", "R-12"],
        "mode_key": "both",
        "names": {
            "ja": "システム方式設計書",
        },
        "section4_titles": {
            "ja": [
                "4.1 システム全体構成",
                "4.2 機能の実現方式",
                "4.3 ハードウェア構成",
                "4.4 ソフトウェア構成",
                "4.5 冗長化・可用性方式",
                "4.6 認証・認可方式",
                "4.7 ログ・監視方式",
                "4.8 バックアップ・リストア方式",
                "4.9 採用しなかった選択肢(該当時 ADR で詳述)",
            ],
        },
    },
    "B-2": {
        "phase_key": "basic_design",
        "required_when_key": "all_scales_all_methods",
        "depends_on": ["B-1", "R-9"],
        "mode_key": "both",
        "names": {
            "ja": "ソフトウェアアーキテクチャ設計書",
        },
        "section4_titles": {
            "ja": [
                "4.1 アーキテクチャスタイル",
                "4.2 アーキテクチャ図",
                "4.3 レイヤ / モジュール分割と依存ルール",
                "4.4 技術スタックの詳細",
                "4.5 主要パターン",
                "4.6 非機能観点の実現方法",
                "4.7 開発規約",
                "4.8 採用しなかった選択肢(該当時 ADR で詳述)",
            ],
        },
    },
    "B-6": {
        "phase_key": "basic_design",
        "required_when_key": "wf_or_hybrid_upstream_required",
        "depends_on": ["R-8"],
        "mode_key": "both",
        "names": {
            "ja": "機能一覧",
        },
        "section4_titles": {
            "ja": [
                "4.1 機能一覧",
                "4.2 機能分類(任意)",
                "4.3 画面起点でない機能(バッチ / API / 帳票)",
                "4.4 Phase 3 で再確定する項目",
            ],
        },
    },
    "B-12": {
        "phase_key": "basic_design",
        "required_when_key": "all_scales_all_methods",
        "depends_on": ["R-4", "R-13"],
        "mode_key": "both",
        "names": {
            "ja": "論理データモデル(論理ER図)",
        },
        "section4_titles": {
            "ja": [
                "4.1 論理ER図",
                "4.2 エンティティ一覧",
                "4.3 属性定義",
                "4.4 リレーション",
                "4.5 正規化状態",
            ],
        },
    },
    "D-8": {
        "phase_key": "detailed_design",
        "required_when_key": "all_scales_all_methods",
        "depends_on": ["B-12"],
        "mode_key": "both",
        "names": {
            "ja": "物理データモデル(物理ER図)",
        },
        "section4_titles": {
            "ja": [
                "4.1 物理ER図",
                "4.2 論理 → 物理対応表",
                "4.3 非正規化判断",
                "4.4 パーティション / シャーディング",
                "4.5 ストレージ見積もり",
                "4.6 DB 製品固有の判断",
            ],
        },
    },
    "D-9": {
        "phase_key": "detailed_design",
        "required_when_key": "all_scales_all_methods",
        "depends_on": ["D-8"],
        "mode_key": "both",
        "names": {
            "ja": "テーブル定義書・インデックス設計書",
        },
        "section4_titles": {
            "ja": [
                "4.1 テーブル定義",
                "4.2 共通カラム規約",
                "4.3 インデックス設計の方針",
            ],
        },
    },
    "D-10": {
        "phase_key": "detailed_design",
        "required_when_key": "all_scales_all_methods",
        "depends_on": ["D-9"],
        "mode_key": "both",
        "names": {
            "ja": "DDL",
        },
        "section4_titles": {
            "ja": [
                "4.1 採用 DB と DDL 方言",
                "4.2 DDL 本体",
                "4.3 適用順序",
                "4.4 ロールバック方針",
                "4.5 初期マスタ(別ファイル参照)",
            ],
        },
    },
}


def get_template(doc_id):
    """spec から単一テンプレを取得。存在しなければ None。"""
    return TEMPLATES.get(doc_id)


def list_templates(lang=None):
    """全テンプレIDを返す。lang を指定するとそのうち言語パックがあるものに絞る。"""
    if lang is None:
        return list(TEMPLATES.keys())
    return [tid for tid, t in TEMPLATES.items() if lang in t["names"]]
