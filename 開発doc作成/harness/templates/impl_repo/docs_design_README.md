# docs/design — 設計 repo スナップショット(読み取り専用)

> このファイルは **実装 repo の `docs/design/README.md` 用スケルトン**です(v0.12〜)。
> **submodule 運用**で設計 repo をネストさせた場合に、目印として実装 repo 側に手で置きます。
> (単純コピー運用では `sync-to-impl.sh` が同等の README を自動生成するため、このスケルトンは不要です。)
> `{{...}}` を案件に合わせて埋めてください。

このディレクトリは **設計 repo のスナップショット**です。実装 repo 側では **編集しないでください**。

| 項目 | 値 |
|---|---|
| 設計 repo | {{設計repoのURL or ローカルパス}} |
| 同期方式 | git submodule |
| submodule パス | `docs/design` |

## ルール

- このディレクトリの中身は **設計 repo が原本**です。実装 repo 側のコミットで中身を変えないこと。
- submodule の更新: `git submodule update --remote docs/design`(設計 repo が進んだら実行)。
- 実装中に設計を変えたくなったら、**ADR を切って**(`origin: implementation`)記録し、設計 repo に逆同期してから D-* / B-* を更新します。影響レベルの判断は設計 repo の `WORKFLOW.md` §8 を参照。

## 影響レベル(設計変更が生じたとき)

- **小** = 設計影響なし → 実装 repo のみで対応
- **中** = 設計影響あり → ADR を切る → 後で設計 repo の D-* / B-* を更新
- **大** = 要件レベル → 実装を一時停止し設計 repo に戻る
