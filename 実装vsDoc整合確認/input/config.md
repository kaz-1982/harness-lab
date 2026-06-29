# 整合の入力設定 (config)

このファイルに **2つのディレクトリ**を記入してから、このハーネスで Claude を起動し「整合を取って」と伝えてください。Claude は起動時にまずこのファイルを読み、`APP_DIR` / `DOC_DIR` を確定します。

> 記入のしかた: 各項目の `:` の右に**絶対パス**で書く。空欄のままなら Claude が会話で質問します。会話で明示パスを伝えた場合は、そちらが本ファイルより優先されます。

## 必須

- **APP_DIR**: <!-- 実装のルート。例 /Users/you/dev/MyApp -->
- **DOC_DIR**: <!-- 設計ドキュメントのルート(または其の output/)。例 /Users/you/dev/MyApp_docs/output -->

## 任意

- **案件名**: <!-- runs/<案件名>/ の控えに使う。空なら DOC_DIR から推定 -->
- **SCOPE**: <!-- 対象の限定。空=全体。例「詳細設計だけ」「API周りだけ」 -->
- **OUT**: <!-- ドリフトレポート出力先。空=DOC_DIR配下(output/_drift_report.md 等) -->
- **CANONICAL**: code <!-- 正の原則。code=コードを正(既定) / per-drift=乖離ごとに判断 -->
- **メモ**: <!-- 既知の改善点・注意・足場(DESIGN_DIGEST のパス等) -->

---

## 記入例

```
- APP_DIR: /Users/sudoukazu/dev/Product/007_DietSupport/DietSupport_app
- DOC_DIR: /Users/sudoukazu/dev/Product/007_DietSupport/開発doc作成_v04_DietSupport/output
- 案件名: DietSupport
- SCOPE:
- CANONICAL: code
- メモ: 足場 = APP_DIR/DESIGN_DIGEST.md あり
```
