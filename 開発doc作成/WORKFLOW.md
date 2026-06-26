# ワークフロー(全体図)

このハーネスは **(任意)事前検討 → 要件定義 → 画面設計 → 詳細設計 →(TDD採用時)テスト具体化 → 実装** のフェーズを **3ツール (ClaudeCode / ClaudeDesign / ClaudeCode)** で分担して進めます。**Phase 0(事前検討の取り込み)は `input/事前検討資料/` に資料が投入された案件でのみ発動**し、**Phase 3.5(テスト具体化 + レビューゲート)はプロファイルで「テスト戦略 = TDD」を選んだ案件でのみ発動**します。

このファイルはワークフローの公式図です。具体的な手順は [harness/02_workflow.md](harness/02_workflow.md) を参照してください。

---

## 1. 全体フロー

```mermaid
flowchart TB
  classDef cc1 fill:#E0F2FE,stroke:#0369A1,color:#0C4A6E
  classDef cd  fill:#FCE7F3,stroke:#BE185D,color:#831843
  classDef cc2 fill:#DCFCE7,stroke:#15803D,color:#14532D
  classDef io  fill:#FEF9C3,stroke:#A16207,color:#713F12
  classDef gate fill:#FEE2E2,stroke:#B91C1C,color:#7F1D1D

  Start([案件ワークスペースをコピー]):::io

  subgraph P0["Phase 0 — 事前検討の取り込み(任意 / 資料投入時のみ)"]
    direction TB
    P0A[input/事前検討資料/ を読み込み]
    P0B[PR-1 事前検討サマリ生成<br/>問題→原因→対応策→想定要件]
    P0A --> P0B
  end
  class P0,P0A,P0B cc1

  subgraph P1["Phase 1 — 要件定義 + 基本設計(画面以外)"]
    direction TB
    P1A[インテーク<br/>output/project_profile.md]
    P1B[選定<br/>output/_doc_plan.md]
    P1C[企画 P-* 該当時]
    P1D[要件定義 R-*]
    P1DM[DM-1 ドメインモデル<br/>DDD採用時]
    P1E[基本設計 B-*<br/>B-7, B-8 を除く]
    P1A --> P1B --> P1C --> P1D --> P1DM --> P1E
  end
  class P1,P1A,P1B,P1C,P1D,P1DM,P1E cc1

  H1[(output/_handoff_to_claude_design/<br/>引き渡しパッケージ)]:::io

  subgraph P2["Phase 2 — 画面設計"]
    direction TB
    P2A[B-7 画面一覧・遷移図]
    P2B[B-8 画面設計書]
    P2C[画面モック/プロトタイプ]
    P2A --> P2B --> P2C
  end
  class P2,P2A,P2B,P2C cd

  H2[(output/04_画面設計_from_ClaudeDesign/<br/>ClaudeDesign 成果物)]:::io

  subgraph P3["Phase 3 — 詳細設計 + 画面影響B-*の確定"]
    direction TB
    P3A[取り込みチェック]
    P3B[画面影響B-* 更新<br/>B-6, B-11, B-14, B-19]
    P3C[詳細設計 D-*]
    P3A --> P3B --> P3C
  end
  class P3,P3A,P3B,P3C cc1

  subgraph P35["Phase 3.5 — テスト具体化 + レビューゲート(TDD採用時)"]
    direction TB
    P35A[3.5-① テスト仕様確定<br/>D-15 最終化 + TS-1 受け入れ]
    P35G1{{★ゲート1<br/>仕様レビュー}}
    P35B[3.5-② Red テストコード生成<br/>UT-* / AT-*]
    P35G2{{★ゲート2<br/>Red コードレビュー}}
    P35A --> P35G1 --> P35B --> P35G2
  end
  class P35,P35A,P35B cc1
  class P35G1,P35G2 gate

  H25[(output/_handoff_to_implementation/<br/>Red テスト + 設計引き渡し)]:::io

  subgraph P4["Phase 4 — 実装"]
    direction TB
    P4A[テストを Green 化する形で実装]
  end
  class P4,P4A cc2

  Start -->|事前検討資料あり| P0
  P0 --> P1
  Start -->|資料なし| P1
  P1 --> H1 --> P2 --> H2 --> P3
  P3 -->|TDD採用| P35 --> H25 --> P4
  P3 -->|TDD不採用| P4
```

凡例: 青=ClaudeCode (ハーネス) / 桃=ClaudeDesign / 緑=ClaudeCode (実装) / 黄=引き渡し成果物 / 赤=レビューゲート

---

## 2. 役割分担

| Phase | 担当ツール | 主成果物 | 場所 |
|---|---|---|---|
| 0(任意) | **ClaudeCode (このハーネス)** | PR-1 事前検討サマリ(資料投入時のみ) | このリポジトリ `output/00_事前検討/` |
| 1 | **ClaudeCode (このハーネス)** | 要件定義 R-* + 基本設計 B-*(画面以外) + DM-1 ドメインモデル(DDD採用時) | このリポジトリ `output/` |
| 2 | **ClaudeDesign** | 画面設計 B-7, B-8 + 画面モック | ClaudeDesign 上のプロジェクト |
| 3 | **ClaudeCode (このハーネス)** | 詳細設計 D-* + 画面影響B-*の更新 | このリポジトリ `output/` |
| 3.5 | **ClaudeCode (このハーネス)** | D-15 最終化 + TS-1 受け入れテスト仕様 + Red テストコード(TDD採用時) | このリポジトリ `output/` |
| 4 | **ClaudeCode (実装)** | アプリケーションコード(テストを Green 化) | 別の実装リポジトリ |

このハーネスが直接担当するのは **(任意)Phase 0・Phase 1・Phase 3・(TDD採用時)Phase 3.5** です。Phase 2 / 4 への引き渡しと取り込みのみハーネスが管理します。**Phase 0 は `input/事前検討資料/` に資料が投入された案件でのみ、Phase 3.5 は「テスト戦略 = TDD」の案件でのみ発動**します。
なお、**ADR(アーキテクチャ決定記録)は特定フェーズに属さず**、設計上の意思決定が発生するたびに Phase 1・3 で随時 `output/横断/ADR/` に蓄積します。

---

## 3. ディレクトリと成果物の対応

```
input/
└── 事前検討資料/                       ← Phase 0 の入力(ユーザーが資料を投入 / 任意)

output/
├── project_profile.md                  ← Phase 1 開始時(インテーク)
├── _doc_plan.md                        ← Phase 1 開始時(選定)
├── _id_registry.md                     ← 全 Phase で随時
├── _review_log.md                      ← 全 Phase で随時
├── 00_事前検討/                        ← Phase 0 (PR-1) / 資料投入時のみ
├── 01_企画/                            ← Phase 1 (P-*)
├── 02_要件定義/                        ← Phase 1 (R-*)
├── 03_基本設計/                        ← Phase 1 + Phase 3 (B-* 画面以外)
├── _handoff_to_claude_design/          ← Phase 1 → Phase 2 引き渡し
├── 04_画面設計_from_ClaudeDesign/      ← Phase 2 成果物 (B-7, B-8)
├── 05_詳細設計/                        ← Phase 3 (D-*) + Phase 3.5 (D-15 最終化, TS-1)
├── _handoff_to_implementation/         ← Phase 3.5 → Phase 4 引き渡し(Red テスト / TDD採用時)
└── 横断/                               ← R-13 用語集, R-14 RTM, DM-1 ドメインモデル 等
    └── ADR/                            ← ADR アーキテクチャ決定記録(随時蓄積)+ _index.md
```

---

## 4. ドキュメント間依存(画面設計の影響)

画面設計の前に確定できるもの / 後でないと確定できないものを区分します。Phase 1 では「画面非依存」を確定し、「画面依存」は方針レベルで止め、Phase 3 で確定させます。

> テスト系(D-15 単体テスト / TS-1 受け入れテスト)が何を典拠に作られるかの依存は、§7.5「Phase 3.5」のテスト依存図を参照(TDD採用時)。

```mermaid
flowchart LR
  classDef independent fill:#DCFCE7,stroke:#15803D,color:#14532D
  classDef screen      fill:#FCE7F3,stroke:#BE185D,color:#831843
  classDef dependent   fill:#FEE2E2,stroke:#B91C1C,color:#7F1D1D

  subgraph A["A. 画面非依存(Phase 1で確定)"]
    direction TB
    R[R-* 全要件]
    B1[B-1 システム方式]
    B2[B-2 アーキテクチャ]
    B12[B-12 論理ER]
    DM[DM-1 ドメインモデル<br/>DDD採用時]
    B17[B-17 運用設計]
    B19p[B-19 セキュリティ<br/>方針レベル]
  end
  class R,B1,B2,B12,DM,B17,B19p independent

  subgraph S["B-7, B-8 画面設計(Phase 2)"]
    Screen[画面一覧・遷移・各画面]
  end
  class Screen,S screen

  subgraph C["C. 画面依存(Phase 3で確定)"]
    direction TB
    B6[B-6 機能一覧]
    B11[B-11 外部IF]
    B14[B-14 CRUD図]
    B19c[B-19 セキュリティ<br/>画面別制御]
    D2[D-2 クラス図]
    D4[D-4 シーケンス図]
    D13[D-13 API仕様書]
    D14[D-14 エラーメッセージ]
    D15[D-15 単体テスト仕様書]
  end
  class B6,B11,B14,B19c,D2,D4,D13,D14,D15 dependent

  R --> Screen
  B1 --> Screen
  B12 --> Screen
  Screen --> B6
  Screen --> B11
  Screen --> B14
  Screen --> B19c
  Screen --> D2
  Screen --> D4
  Screen --> D13
  Screen --> D14
  Screen --> D15
```

---

## 5. フェーズ移行のシーケンス

```mermaid
sequenceDiagram
  actor User as ユーザー
  participant CC1 as ClaudeCode<br/>(ハーネス)
  participant CD as ClaudeDesign
  participant CC2 as ClaudeCode<br/>(実装)

  User->>CC1: インテーク開始
  CC1->>User: 質問票で対話
  CC1->>CC1: project_profile.md / _doc_plan.md 作成

  Note over CC1: Phase 1: R-* + B-*(画面以外)
  CC1->>User: Phase 1 完了レビュー依頼
  User->>CC1: 承認
  CC1->>CC1: _handoff_to_claude_design/ 生成
  CC1-->>User: 引き渡しパッケージ準備完了

  User->>CD: パッケージを入力に画面設計を依頼
  CD-->>User: B-7, B-8, モック作成
  User->>CC1: 04_画面設計_from_ClaudeDesign/ に配置

  CC1->>CC1: 取り込み整合性チェック
  Note over CC1: Phase 3: D-* + 画面影響B-*更新
  CC1->>User: Phase 3 完了レビュー依頼
  User->>CC1: 承認

  opt テスト戦略 = TDD のとき(Phase 3.5)
    Note over CC1: Phase 3.5: テスト具体化
    CC1->>CC1: D-15 最終化 + TS-1 作成(UT-*/AT-*)
    CC1->>User: ★ゲート1 テスト仕様レビュー依頼
    User->>CC1: 承認
    CC1->>CC1: Red テストコード生成(失敗状態を確認)
    CC1->>User: ★ゲート2 Red コードレビュー依頼
    User->>CC1: 承認
    CC1->>CC1: _handoff_to_implementation/ 生成
  end

  User->>CC2: 全ドキュメント + Red テストを入力に実装依頼
  CC2-->>User: アプリケーションコード(テストを Green 化)
```

---

## 6. 引き渡しパッケージ仕様 (Phase 1 → 2)

`output/_handoff_to_claude_design/` の構成(**Phase 1 完了時にユーザーが ClaudeDesign に渡すパッケージの仕様**)。生成手順は [harness/02_workflow.md §6](harness/02_workflow.md) を参照。

```
_handoff_to_claude_design/
├── README.md                       # ClaudeDesign 向け説明書(画面設計の前提条件)
├── 00_案件サマリ.md                # project_profile からの抜粋 + 制約
├── 01_要件サマリ.md                # R-1 / R-7 or R-8 / R-9 のダイジェスト
├── 02_入力資料一覧.md              # refs/ のインデックス + 各資料の使い方
└── refs/                           # 該当ドキュメントのコピー
    ├── R-1_業務要件定義書.md
    ├── R-7_ユーザーストーリー.md  または  R-8_機能要件定義書.md
    ├── R-9_非機能要件定義書.md
    ├── R-13_用語集.md
    ├── B-1_システム方式設計書.md
    ├── B-2_アーキテクチャ設計書.md
    ├── B-12_論理ER図.md
    └── DM-1_ドメインモデル.md   # DDD採用時
```

`refs/` の中身は **コピー** とする(ClaudeDesign 側では追加情報を取りに来られないため、Phase 1 完了時のスナップショットを固定する)。

---

## 7. 取り込み仕様 (Phase 2 → 3)

ClaudeDesign 成果物を受け入れる `output/04_画面設計_from_ClaudeDesign/` の構成(**ユーザーが配置する場所と必須ファイルの仕様**)。取り込みチェックの実行手順は [harness/02_workflow.md §7](harness/02_workflow.md)、整合性チェックの詳細観点は [harness/03_quality_checklist.md](harness/03_quality_checklist.md) を参照。

```
04_画面設計_from_ClaudeDesign/
├── README.md                  # 取り込み手順 + チェックリスト
├── B-7_画面一覧_画面遷移図.md
├── B-8_画面設計書.md
├── mockups/                   # 画面モック画像 / Figma リンク等
└── _import_log.md             # 取り込み日 + ClaudeDesign プロジェクトURL
```

---

## 7.5 Phase 3.5 — テスト具体化 + レビューゲート(TDD採用時)

`output/project_profile.md` の「テスト戦略」が **TDD** の案件でのみ実施。Phase 3(詳細設計)完了後、Phase 4(実装)に入る前に、設計ドキュメントから **テストを先に作り上げ**、2段階のレビューゲートでユーザー承認を得る。実行手順は [harness/02_workflow.md §9.5](harness/02_workflow.md) を参照。

### 入口ガード(満たさなければ着手しない)

- [ ] `project_profile.md` の「テスト戦略 = TDD」
- [ ] 技術スタック + テストフレームワークが確定(TBD 不可)← ルール7「推測で埋めない」
- [ ] D-15 の骨子(対象モジュール × 観点)が Phase 3 で作成済
- [ ] 対象機能(B-6)/ ユーザーストーリー(R-7)の受け入れ基準(AC)が確定

### 2段階ゲートの概要

```
3.5-① テスト仕様の確定 (D-15 最終化 + TS-1 作成 / UT-*・AT-* 採番)
        ↓
       ★ゲート1(仕様レビュー)→ ユーザー承認
        ↓
3.5-② Red テストコード生成 (UT-*/AT-* に1対1対応の実行可能テスト)
        ↓
       ★ゲート2(Red コードレビュー)→ ユーザー承認
        ↓
       Phase 4(別リポジトリ)で Green 化
```

アジャイル運用では Just Enough により、ゲート1とゲート2を1回のレビューに統合してよい。

### テスト依存(何を典拠にテストを作るか)

```mermaid
flowchart LR
  classDef req  fill:#FEF9C3,stroke:#A16207,color:#713F12
  classDef des  fill:#E0F2FE,stroke:#0369A1,color:#0C4A6E
  classDef tst  fill:#FCE7F3,stroke:#BE185D,color:#831843

  AC[受け入れ基準 AC<br/>R-7 / R-8]:::req
  B8[B-8 画面設計書]:::des
  D12[D-12 モジュール仕様]:::des
  TS1[TS-1 受け入れテスト仕様<br/>AT-*]:::tst
  D15[D-15 単体テスト仕様<br/>UT-*]:::tst
  Code[Red テストコード]:::tst

  AC --> TS1
  B8 --> TS1
  B8 --> D15
  D12 --> D15
  TS1 --> Code
  D15 --> Code
```

### ゲート完了基準

| ゲート | 完了基準 |
|---|---|
| ゲート1(仕様) | 全機能(B-6)・全 AC に1件以上のケースが割当 / 期待結果が検証可能(数値・状態が具体)/ RTM テストID列充填 / `_review_log.md` 記録 / ユーザー承認 |
| ゲート2(Red) | ゲート1の全ケースに対応コードが存在 / 全テストが Red で実行確認済(実行ログを `_review_log.md` に添付)/ テスト名と UT-*/AT-* が機械的に対応 / `_test_manifest.md` が `check.py` テストマニフェスト突合で緑(掲載漏れ・ゴースト無し / v0.13〜)/ 技術スタック準拠 / ユーザー承認 |

---

## 8. Phase 4 実装への引き渡し

Phase 3 完了時点(TDD採用時は Phase 3.5 のゲート2承認後)で、実装 (ClaudeCode) に渡す入力一覧。引き渡し作業の手順は [harness/02_workflow.md §10](harness/02_workflow.md) を参照。

- `output/02_要件定義/` 全ドキュメント
- `output/03_基本設計/` 全ドキュメント
- `output/04_画面設計_from_ClaudeDesign/` 全ドキュメント
- `output/05_詳細設計/` 全ドキュメント(D-15 単体テスト仕様 / TS-1 受け入れテスト仕様 を含む)
- `output/横断/` 全ドキュメント(R-13 用語集, R-14 RTM, DM-1 ドメインモデル, ADR アーキテクチャ決定記録)
- **(TDD採用時)** `output/_handoff_to_implementation/` — Red テストコード(`tests/unit/`, `tests/acceptance/`)+ `_test_manifest.md`(UT/AT ↔ ファイル ↔ 要件 の対応表)+ README(Green 化手順)

別リポジトリの ClaudeCode は、これらを `docs/design/` 等にコピー or サブモジュール参照して実装に着手する。**TDD採用時は、`_handoff_to_implementation/tests/` の Red テストをプロジェクトに取り込み、テストを Green にする形で実装を進める**(テストを後から都合よく書き換えない)。

### 8.1 設計 repo と実装 repo の同期(v0.12〜)

設計 repo(このハーネス)と実装 repo は **分けて運用**する。設計ドキュメントは実装 repo の **`docs/design/`** に置き、そこを **読み取り専用スナップショット**として扱う。同期方式は2つ。

| 方式 | 向くケース | 取り込み |
|---|---|---|
| **git submodule** | バージョン管理したい / 設計の更新を追跡したい(推奨) | 設計 repo を実装 repo の `docs/design` に submodule 配置 |
| **単純コピー** | submodule を避けたい / 一回きりのスナップショットでよい | 設計 repo 側で `bash harness/tools/sync-to-impl.sh <実装repoパス>` |

実装 repo 側に置くスケルトン(`CLAUDE.md` / `docs/design/README.md` / 読取専用ガード `pre-commit`)は [harness/templates/impl_repo/](harness/templates/impl_repo/) に同梱。使い方は同ディレクトリの `README.md` 参照。

#### submodule セットアップ(Windows / macOS 両対応)

ローカルパス運用(1人 + 1台)を想定。**実装 repo 側**で実行する。

```bash
# 実装 repo のルートで:
# 相対パスでの submodule 追加を推奨(マシン間で .gitmodules が壊れにくい)
git submodule add ../<設計repoのディレクトリ名> docs/design

# 例: 親ディレクトリに design-repo と impl-repo が並んでいる場合
#   <親>/design-repo   ← 設計 repo(このハーネスのコピー)
#   <親>/impl-repo     ← 実装 repo
# impl-repo 側で:
git submodule add ../design-repo docs/design

git add .gitmodules docs/design
git commit -m "chore: 設計 repo を docs/design に submodule 追加"
```

- **Windows(Git Bash)/ macOS 共通**。パス区切りはどちらも `/`(Git は内部で `/` を使う)。
- `.gitmodules` は `git submodule add` が自動生成する(テンプレは同梱しない)。**相対パス(`../design-repo`)を推奨** — 絶対パスやマシン固有パスはクローン先で壊れるため避ける。生成された `.gitmodules` の `url` が絶対パスになっていたら相対パスに手で直す。
- 設計 repo が進んだら実装 repo 側で `git submodule update --remote docs/design` → コミットでポインタを進める(この同期コミットは読取専用ガードを `--no-verify` でバイパスしてよい)。

#### 同期の記録(両方式共通)

同期するたびに、設計 repo の [output/_handoff_to_implementation/_sync_log.md](output/_handoff_to_implementation/_sync_log.md) に **commit / 日付 / 同期した ADR** を記録する。`_sync_log.md` は **TDD 不採用案件でも使う**(Red テストの有無に関わらず、同期追跡のために置かれる雛形)。

### 8.2 ADR を同期キーにした設計変更の扱い

ADR(`output/横断/ADR/`)を **両 repo の同期キー**とする。実装中に設計を変えたくなったら、まず **影響レベル**を判断する。

| レベル | 判断 | アクション |
|---|---|---|
| **小** | 設計に影響しない実装詳細 | 実装 repo 内で対応。ADR 不要 |
| **中** | 設計に影響する(構造・IF・データが変わる) | **ADR を切る**(frontmatter `origin: implementation`)→ 設計 repo に逆同期して D-* / B-* を更新 → `_sync_log.md` に記録 |
| **大** | 要件レベルの問題 | **実装を一時停止**し、設計 repo に戻って R-* / B-* から見直す |

ADR の `origin` フィールド(v0.12〜)で、その決定が **設計フェーズ発(`design`)** か **実装フェーズ発(`implementation`)** かを明示する。実装フェーズ発の ADR は、設計 repo に逆同期するまで `_sync_log.md` の「逆同期メモ」に残しておく。

---

## 9. セッション分割の運用ガイド

規模の大きい案件では、1セッションに作業を詰め込むとコンテキストが肥大し、ツール(特にファイル書き込み)が不安定になります。これを避けるため、**作業をセッション単位に分割**して進めます。このハーネスは状態ファイル(`output/project_profile.md` / `output/_doc_plan.md` / `output/_id_registry.md`)駆動で再開できるため、セッションを分割しても進行状況は失われません(CLAUDE.md「起動時の挙動」が現在地を自動判別します)。

### 9.1 区切りの単位

- **目安: ドキュメント2〜3本ごとに1セッション**。コンテキスト肥大の予防と、セッション切り替えの手間のバランス点。
- **フェーズ境界(Phase 1→2→3→3.5)では必ずセッションを切る**。引き渡しパッケージ(`_handoff_to_*`)が自然な区切りになる。
- 参照資料が多い作業や大型ドキュメント(例: B-8 画面設計書、D-* 詳細設計)は単独セッションにする。
- **最初のセッションはインテーク → 選定(`_doc_plan.md` 生成)に専念**する。ここで全ドキュメント数が確定し、初めて具体的な分割計画(何をどのセッションで書くか)が立てられる。

### 9.2 セッション終了時の手順(必須)

各セッションを終える前に、状態ファイルを最新化してから git commit する。**このコミットが次セッションの再開点**になる。

1. 着手したドキュメントを完了まで通す(`check.py` → 手動チェックリスト → `_review_log.md` 追記)。中途半端なドキュメントを残さない(ルール2「1ドキュメント1セッション」)。
2. `output/_doc_plan.md` の該当ドキュメントの「状態」を更新(進行中 / 承認済 等)。
3. `output/_id_registry.md` に新規採番IDを登録。
4. `git add -A && git commit` — コミットメッセージに**どこまで完了したか**と**次にやること**を明記。

### 9.3 セッション開始時の手順(再開)

新しいセッションでは、Claude が CLAUDE.md「起動時の挙動」に従って現在地を自動判別する。ユーザーは「続きをお願い」と伝えるだけでよい。Claude は次の順で状態を確認してから着手する。

1. `output/project_profile.md`(案件前提)と `output/_doc_plan.md`(進捗)を読む。
2. `output/_id_registry.md` の最終採番を確認。
3. 直近の `git log` で前セッションの区切りを確認。
4. **次に着手すべきドキュメントをユーザーに提示**してから作業を開始する(いきなり書き始めない)。

### 9.4 セッション境界のイメージ

具体的なドキュメントは `_doc_plan.md` 確定後に割り付ける。以下は2〜3本ごとに区切る場合の典型例(ウォーターフォール / 大規模)。

```
[S1]  インテーク + 選定 → _doc_plan.md 確定 ............ commit
[S2]  R-1, R-7/R-8 .................................... commit
[S3]  R-9, R-13(用語集) .............................. commit
 :    (要件定義 R-* を 2〜3本ごと)
[Sx]  B-1, B-2 ....................................... commit
 :    (基本設計 B-* 画面以外を 2〜3本ごと)
[Sy]  横断完了 → _handoff_to_claude_design/ 生成 ...... commit  ← Phase 1 終了
 ───  セッションを切り ClaudeDesign へ(Phase 2)───
[Sz]  画面設計成果物 取り込み + 画面影響B-* 更新 ....... commit  ← Phase 3 開始
 :
```

> セッション数の目安: 全ドキュメントが N 本なら、おおよそ `N ÷ 2.5 + フェーズ境界の本数` セッション。例えば Phase 1 で 20 本なら 8〜10 セッション程度を見込む。
