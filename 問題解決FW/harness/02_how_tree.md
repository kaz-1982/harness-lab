# 02_how_tree.md — ③ 対応策（How）ロジックツリー（1対1 → 必要に応じて収束）

目的：②で洗い出した**末端の根本原因（全件・C番号つき）**それぞれに、**まず対策を1つずつ（1原因1対策）必ず付ける**。
そのうえで、**必要に応じて**対策を右へ**収束**させ（束ねられるものだけ束ねる）、実際にとる**本筋アクション**に寄せる。
対策には識別番号（M番号）を付け、収束・本筋にも番号を付けて、原因↔対策の対応を番号で追えるようにする。
各対策・本筋には**目指す品質水準（既定＝市販品同等以上・POC不可）**を必ず添える。

> **識別番号（ID）の付け方**（詳細は `templates/_format.md`「識別番号（ID）」）
> - 末端原因＝`C1, C2, …`（②で採番済み）／1対1の対策＝`M1, M2, …`／収束した対策＝`T1, T2, …`／本筋アクション＝`A1, A2, …`。
> - **原因 `Cn` に対応する対策は `Mn`**（番号をそろえて1対1を明示）。収束・本筋は束ねた番号を併記（例：`T1（M1+M2+M3）` / `A1（T1+T2+T3）`）。
> - **drawio の各ノードのラベル先頭に番号を表示**する（例：`C1 見積書を手作業で作成` / `M1 見積作成を自動化する`）。mxCell の `id` も同じ番号にそろえる。

> **基本ルール**
> 1. **対策は必ず「原因の数だけ」作る。** すべての末端原因 `Cn` に対策 `Mn` を1つずつ対応させる（1対1）。これで**原因↔対策の対応がユーザーの目で判断できる**形になり、カバレッジ（対策のない原因ゼロ）も自動的に満たす。
> 2. **そこから必要に応じて右へ収束させる。** 似た対策・1つにまとめられる対策だけを束ねて数を減らし、少数の本筋に寄せる。**減るほど実行しやすい。**
> 3. **無理に収束しない。** 束ねると効きが落ちる／自然にまとまらないものは、そのまま右へ送ってよい。**原因の数だけ対策が残っても構わない。**

作り方・MECE のチェックは `harness/_mece_guide.md` を必ず参照すること。

---

## 進め方

### ステップ A：末端の原因（全件・C番号）を左端に並べる

`output/02_原因ツリー_why.md` の「根本原因の一覧（全件）」を、③の図の**左端の列**に C番号つきですべて置く。**原因は1つも省かない。**

### ステップ B：各原因に対策を1つずつ付ける（1対1・Cn↔Mn・原因の数だけ必ず作る）

**すべての原因 `Cn` の真横に、その原因への対策 `Mn` を1つ置く。**「`Cn` 原因 → `Mn` 対策」が**同じ高さ（横一直線）**で並ぶので、対応関係が番号と位置の両方で一目で分かる。

- 発想の軸は `_mece_guide.md` を参照（やめる／減らす／変える／自動化する／増やす、対象別、達成手段別 など）。
- 打ち切る条件は「**誰が・何を・どうするか**が言える」具体度。
- この段階では**対策の数＝原因の数**。1施策で複数原因に効きそうでも、**まずは原因ごとに `Mn` を1つずつ書き出す**（後で束ねる）。

> **ユーザーに対応を見てもらう。** 「`Cn` → `Mn`」の1対1の対応を提示し、**この対応で合っているか、対策が原因に効くかを人の目で判断**してもらう（ここが収束の前提）。

### ステップ C：必要に応じて右へ収束させる（T番号・無理にしない）

1対1で並べた対策 `Mn` を見渡し、**まとめられるものだけ**を右の列で1つの収束対策 `Tk` に束ねる（ラベルに `Tk（Mx+My+…）` と併記）。

- 「**これとこれは同じ打ち手だ**」というものを束ね、対策の数を減らす（減るほど実行しやすい）。
- **束ねないものはそのまま右へ送ってよい**（`Tk（Mn・単独）` のように単独でもよい）。自然にまとまらない／束ねると効きが落ちる対策は無理にまとめない。**原因の数だけ対策が残っても構わない。**
- 収束しても**カバレッジは維持**（どの原因も、番号をたどれば対策に行き着く）。収束は“まとめられるものをまとめる”ことで、原因を捨てる口実にしない。

### ステップ D：本筋アクションへ寄せる（A番号・最右・最少）

収束した対策 `Tk` を、**実際にとる少数の打ち手＝本筋アクション `An`**（ラベルに `An（Tx+Ty+…）` と併記）に寄せる（図のいちばん右）。
対症療法の寄せ集めで終わらせず、狙いを一段引き上げて「結局これをやる」を1〜数個立てる。（収束が進まなければ、本筋＝収束対策と同じでもよい。）

### ステップ E：各対策・本筋の「目指す品質水準」を決める（妥協しない・POC不可）

「すぐ作れる」を採用理由にしない。**先に到達すべき品質を決め、それを満たす形で設計する。**

- **既定の品質バー＝「市販・既存サービスと同等以上」。POC・間に合わせは目標にしない**（市場で十分に通用する品質が完了の定義）。比較対象がない領域でも、**同種のベストプラクティスと同等以上**を基準にする。
- 各対策・本筋に「**目指す品質水準**」と「**比較対象**」を1行で添える。
- 品質を満たすのに手間がかかっても**外す理由にしない**（着手順を後ろにするだけ。実装力は Claude が支える）。

### ステップ F：drawio で図にして output に保存（番号つき・1対1 → 収束）

`templates/03_対応策ツリー_how.md` の雛形に沿って `output/03_対応策ツリー_how.md` を作り、図は
`output/03_対応策ツリー_how.drawio`（mxGraph XML）として保存する。

- **左→右**：**原因 C（全件）→ 対策 M（原因の数だけ・1対1）→ 収束した対策 T（必要に応じて）→ 本筋 A（最少）**。
- **原因 `Cn` と1対1の対策 `Mn` は同じ高さ（横一直線）に置く**——対応が番号と位置で一目で分かるように。
- **各ノードのラベル先頭に番号を表示**（`C1` / `M1` / `T1（M1+M2+M3）` / `A1（T1+T2+T3）`）。mxCell の `id` も同じ番号にそろえる。
- **原因ノード・1対1の対策ノードは白（等価）**、**複数の対策を束ねた収束対策・本筋は緑**で強調（緑＝「すぐ作れる」ではなく「**束ね・本筋**」）。
- **座標は `templates/_format.md`「収束させる図の座標」**で計算する。

下は**書き方の例**（②の末端原因 C1〜C6 → 対策 M1〜M6（1対1）→ 必要分だけ収束 T → 本筋 A）。

```xml
<mxfile host="app.diagrams.net">
  <diagram id="how-tree" name="対応策ツリー（1対1→収束）">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="826" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="h1" value="① 原因 C（全件）" style="text;html=1;align=left;fontStyle=1" vertex="1" parent="1"><mxGeometry x="40" y="10" width="220" height="24" as="geometry" /></mxCell>
        <mxCell id="h2" value="② 対策 M（原因の数だけ・1対1）" style="text;html=1;align=left;fontStyle=1" vertex="1" parent="1"><mxGeometry x="330" y="10" width="260" height="24" as="geometry" /></mxCell>
        <mxCell id="h3" value="③ 収束 T（必要に応じて束ねる）" style="text;html=1;align=left;fontStyle=1" vertex="1" parent="1"><mxGeometry x="620" y="10" width="260" height="24" as="geometry" /></mxCell>
        <mxCell id="h4" value="④ 本筋 A" style="text;html=1;align=left;fontStyle=1" vertex="1" parent="1"><mxGeometry x="910" y="10" width="220" height="24" as="geometry" /></mxCell>
        <mxCell id="C1" value="C1 見積書を手作業で作成" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="40" y="40" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="C2" value="C2 報告書も手作業で作成" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="40" y="130" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="C3" value="C3 案件情報が個人のExcelに散在" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="40" y="220" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="C4" value="C4 承認者が1人に集中している" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="40" y="310" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="C5" value="C5 承認ルールが不明確" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="40" y="400" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="C6" value="C6 新人が手順を聞いて回る" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="40" y="490" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="M1" value="M1 見積作成を自動化する" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="330" y="40" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="M2" value="M2 報告書作成を自動化する" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="330" y="130" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="M3" value="M3 案件情報を一元管理する" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="330" y="220" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="M4" value="M4 承認者を複数体制にする" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="330" y="310" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="M5" value="M5 承認ルールを明文化する" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="330" y="400" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="M6" value="M6 手順を標準化・教材化する" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="330" y="490" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="T1" value="T1 営業支援ツール導入（M1+M2+M3）&#10;出力を市販品質にそろえる" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e6ffe6;strokeColor=#22aa22" vertex="1" parent="1"><mxGeometry x="620" y="130" width="240" height="60" as="geometry" /></mxCell>
        <mxCell id="T2" value="T2 承認フローを再設計（M4+M5）" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e6ffe6;strokeColor=#22aa22" vertex="1" parent="1"><mxGeometry x="620" y="355" width="240" height="60" as="geometry" /></mxCell>
        <mxCell id="T3" value="T3 手順を標準化・教材化（M6・単独）" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="620" y="490" width="240" height="60" as="geometry" /></mxCell>
        <mxCell id="A1" value="A1 業務を「仕組み」で再設計（T1+T2+T3）" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e6ffe6;strokeColor=#22aa22;strokeWidth=2;fontStyle=1" vertex="1" parent="1"><mxGeometry x="910" y="310" width="240" height="60" as="geometry" /></mxCell>
        <mxCell id="eC1M1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="C1" target="M1"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eC2M2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="C2" target="M2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eC3M3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="C3" target="M3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eC4M4" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="C4" target="M4"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eC5M5" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="C5" target="M5"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eC6M6" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="C6" target="M6"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eM1T1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="M1" target="T1"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eM2T1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="M2" target="T1"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eM3T1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="M3" target="T1"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eM4T2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="M4" target="T2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eM5T2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="M5" target="T2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eM6T3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="M6" target="T3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eT1A1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="T1" target="A1"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eT2A1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="T2" target="A1"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eT3A1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="T3" target="A1"><mxGeometry relative="1" as="geometry" /></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

> 上は**書き方の例**です。実際の中身はユーザーの原因に合わせて作ること。
> **原因C1〜C6 → 対策M1〜M6（1対1・横一直線・Cn↔Mn）→ 収束（T1はM1+M2+M3、T2はM4+M5、T3はM6単独）→ 本筋A1（T1+T2+T3）**。
> **原因の数だけ対策がある**のが起点で、収束は**必要な分だけ**。番号でどの原因がどの対策・本筋に行き着くか追える。
> Markdown 側（`03_対応策ツリー_how.md`）には、この `.drawio` へのリンクと、**C↔M の1対1対応表**、収束（T）と本筋（A）のまとめを残すこと。

### ステップ G：ユーザーに見せて、一緒に改善する（重要なループ）

図と「原因↔対策」の対応（番号つき）を提示し、こちらから問いかけてコメントを促す。例：

```
対応策の初稿を作りました（output/03_対応策ツリー_how.md）。一緒に見てください。
まず「Cn 原因 → Mn 対策」を1対1（横一直線）で並べ、右へ必要な分だけ束ねています（T・A 番号つき）。

確認したいポイント：
- 各原因 Cn に付けた対策 Mn は、その原因に効きますか？（1対1の対応が妥当か。人の目での判断をお願いします）
- 束ねた（収束した）まとまり T は自然ですか？　逆に「これは分けたい／これは一緒で良い」はありますか？
- いちばん右の本筋 A は、実際にこれをやればいい、と思える形ですか？
- 各打ち手の品質は市販品・既存サービスと比べて十分ですか？（POCで止まっていないか）

気になる点を教えてください。一緒に直していきます。
```

ユーザーのコメントを受けたら：
1. 図を**直す**（対策の差し替え・束ね方の調整・本筋への引き上げ・具体化）。
2. 直した図を再提示し、**何をどう変えたか**を一言添える。
3. 「他に気になる点はありますか？」と再度促す。
4. **ユーザーが「これで良い」と言うまで繰り返す。** Claude から打ち切らない。

毎回、`output/03_対応策ツリー_how.drawio`（図）と `output/03_対応策ツリー_how.md`（リンク＋C↔M対応表＋収束）の両方を上書き更新する。原因や対策を増減したら**番号を振り直す**（抜け番・重複なし）。

### ステップ H：次へ

全原因に対策が1対1で付き、必要な収束（T）と本筋（A）が決まり、各打ち手の品質水準も決まったら、
「**これらを優先順位（着手順）づけして、実行計画（④）にまとめてよいですか？**」と確認し、合意できたら `harness/03_action_plan.md` に進む。

---

## 注意

- **対策は必ず「原因の数だけ」作る（1対1・Cn↔Mn）。** すべての原因の真横に対策を1つ置き、対応を番号と位置で人の目で判断できるようにする。これでカバレッジも満たす。
- **識別番号を必ず付け、drawio にも表示する。** 原因C／対策M／収束T／本筋A。`Cn↔Mn` で1対1、収束・本筋は束ねた番号を併記。
- **収束は必要に応じて・無理にしない。** まとめられるものだけ右へ束ねる。**原因の数だけ対策が残ってもよい。** 減るほど実行しやすいが、効きを犠牲にして1つにしない。
- **原因を捨てない。** 収束しても、どの原因も番号をたどれば対策に行き着く（カバレッジ維持）。
- **本筋を出す。** いちばん右に「結局これをやる」という少数の打ち手を立てる（収束が進まなければ収束対策＝本筋でよい）。
- **品質を先に決める・POC不可。** 「すぐ作れる」を理由に品質を落とさない。既定の品質バーは「市販・既存サービス同等以上」。
- コスト・納期で対策を外さない（実装力は Claude が支える）。**着手の順番は④で効果（インパクト）で決める**。
- この段階では**優先順位（着手順）はまだ決めない**（④で品質ゲート＋効果で決める）。

以上。対応策の合意が取れたら ④ `harness/03_action_plan.md` へ。
