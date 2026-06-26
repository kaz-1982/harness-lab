# 設計 ↔ 実装 同期ログ(_sync_log.md)

このファイルは、**設計 repo(このハーネス)と実装 repo(別リポジトリ)の間で同期した内容**を時系列で記録する台帳です(v0.12〜)。
両 repo を分けて運用するとき、**ADR を同期キー**にして「どの決定がどちらの repo に、いつ反映されたか」を追跡します。
同期方式(git submodule / 単純コピー)は問いません。手順は [../../WORKFLOW.md](../../WORKFLOW.md) §8 を参照。

---

## 1. 同期方式

<!-- この案件で採用した同期方式に ✅ を付ける -->

- [ ] **git submodule**: 設計 repo を実装 repo の `docs/design/` に submodule 配置(`<実装repo>/docs/design` = 本 repo)
- [ ] **単純コピー**: `bash harness/tools/sync-to-impl.sh <実装repoパス>` で `docs/design/` にスナップショットをコピー

- 実装 repo: `TBD: 実装リポジトリの URL またはローカルパス`
- 設計 repo(本 repo): `TBD: この設計リポジトリの URL`

---

## 2. スナップショット同期履歴(設計 → 実装)

設計 repo の内容を実装 repo の `docs/design/` に反映した記録。submodule なら「ポインタを進めた commit」、単純コピーなら「sync-to-impl.sh を実行した時点」を記録する。

| 日付 | 設計 repo commit | 同期方式 | 反映先(実装 repo) | 備考 |
|---|---|---|---|---|
| YYYY-MM-DD | `<hash>` | submodule / copy | docs/design/ | 例: Phase 3 完了スナップショット |

---

## 3. ADR 同期対応表(両 repo の同期キー)

設計フェーズ・実装フェーズで生まれた ADR が、両 repo にいつ反映されたかの対応表。
ADR の `origin` フィールド(`design` / `implementation`)と整合させること。

| ADR ID | origin | 決定の要旨 | 設計 repo 反映日 | 実装 repo 反映日 | 影響レベル | 状態 |
|---|---|---|---|---|---|---|
| ADR-0001 | design | 例: ドメイン層をフレームワーク非依存に | YYYY-MM-DD | YYYY-MM-DD | 中 | 同期済 |

- **origin**: `design`(設計フェーズ発)/ `implementation`(実装フェーズ発)
- **影響レベル**(WORKFLOW.md §8 の分類):
  - **小** = 設計影響なし(実装 repo のみで完結。ADR 不要のことが多い)
  - **中** = 設計影響あり(ADR を切る → 後で D-* / B-* を更新)
  - **大** = 要件レベル(実装を一時停止し、設計 repo に戻って R-* / B-* から見直す)
- **状態**: `未同期` / `同期済` / `要再同期`(片側のみ反映され差分が残っている)

---

## 4. 逆同期メモ(実装 → 設計)

実装フェーズで `origin: implementation` の ADR が生まれた場合、設計 repo 側で D-* / B-* / R-* に反映する作業を残す。

- TBD: 逆同期が必要な ADR と、設計 repo 側で更新すべきドキュメント
