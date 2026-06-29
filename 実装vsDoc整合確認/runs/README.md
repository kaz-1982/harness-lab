# runs/ — 実行ごとの控え

逆同期を実行した案件ごとに `runs/<案件名>/` を作り、以下の控えを置く:

- `_drift_report.md` のコピー(正本は DOC_DIR 側)
- 実行メモ(入力に使った APP_DIR / DOC_DIR、正の原則、ユーザー判断の結果)

正本(更新されたドキュメント・ID台帳・レビュー記録)は **DOC_DIR 側**に残る。ここは履歴・索引用。

## 実績

- `DietSupport/` — 007_DietSupport の実装↔設計 整合(2026-06-27)。差分9件、新規ID F-018/AT-023/UT-064〜067、食事区分 snack 追加、サーバー汎用同期ストアの両方併記。正本は `007_DietSupport/開発doc作成_v04_DietSupport/output/_drift_report.md`。
