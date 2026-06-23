# ClaudeDesign 成果物受け入れディレクトリ

このディレクトリは、ClaudeDesign (Phase 2) で作成された画面設計を受け入れるための場所です。
全体フロー: [../../WORKFLOW.md](../../WORKFLOW.md)

---

## 目的

Phase 2 で ClaudeDesign が作成した画面設計 (B-7, B-8) と画面モックをここに集約し、Phase 3 で詳細設計 (D-*) や画面影響B-* (B-6, B-11, B-14, B-19) の入力として参照します。

---

## 配置するファイル

ClaudeDesign 完了後、ユーザーが以下を配置してください:

```
04_画面設計_from_ClaudeDesign/
├── README.md                       ← このファイル
├── B-7_画面一覧_画面遷移図.md     ← 必須
├── B-8_画面設計書.md               ← 必須
├── mockups/                        ← 画面モック画像 / Figma リンク等(任意)
└── _import_log.md                  ← 必須(取り込みログ)
```

`_import_log.md` のフォーマット例:

```markdown
# ClaudeDesign 取り込みログ

- 取り込み日: 2026-XX-XX
- ClaudeDesign プロジェクトURL: https://...
- ClaudeDesign 側のバージョン: v0.X
- 引き渡しパッケージのバージョン: 引き渡し日 2026-XX-XX 時点
- 新規採番された画面ID: S-001 〜 S-NNN
- 新規発生した機能ID(ハーネス側で登録要): F-XXX, F-YYY
- 新規発生した API ID(ハーネス側で登録要): A-XXX
- 用語集に追加候補の用語: 〇〇, △△
```

---

## 取り込み手順(Claude 自動実行)

ユーザーが「ClaudeDesign 完了」と伝えたら、Claude は以下を自動で実行します。

### Step 1: ファイル存在確認
- `B-7_画面一覧_画面遷移図.md`
- `B-8_画面設計書.md`
- `_import_log.md`

不足があればユーザーに確認。

### Step 2: ID登録
`_import_log.md` の「新規採番された画面ID」「新規発生した機能ID/API ID」を `output/_id_registry.md` に追記。

### Step 3: 整合性チェック([../../harness/03_quality_checklist.md](../../harness/03_quality_checklist.md) の「Phase 2 → Phase 3 取り込み」セクション)

- [ ] 画面ID(S-*)が `_id_registry.md` と整合
- [ ] エンティティ名が `output/03_基本設計/B-12_論理データモデル.md` と一致
- [ ] 用語が `output/横断/R-13_用語集.md` と一致(未登録は追加)
- [ ] アクセス権限が `output/02_要件定義/R-9_非機能要件定義書.md` と整合
- [ ] 機能呼び出しが `output/03_基本設計/B-6_機能一覧.md` に存在(なければ B-6 更新タスク化)

### Step 4: `_doc_plan.md` 更新
- B-7, B-8 の `状態` を `引き渡し済` → `取り込み済`
- 画面影響B-* (B-6, B-11, B-14, B-19) を Phase 3 の作業対象として `進行中` に

### Step 5: `_review_log.md` に記録
取り込みチェック結果を追記。

---

## 不整合が見つかった場合

ClaudeDesign 側の修正が必要な場合は、以下の選択肢をユーザーに提示します:

- 案A: ClaudeDesign 側で修正してもらい、再度このディレクトリに配置
- 案B: ハーネス側で吸収(用語追加・ER 修正・新規 ID 採番)
- 案C: 一部だけ ClaudeDesign 側、残りはハーネス側

修正方針の決定は `_review_log.md` に「Phase 2 取り込み — 不整合対応」として記録。
