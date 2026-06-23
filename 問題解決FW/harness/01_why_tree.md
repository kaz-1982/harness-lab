# 01_why_tree.md — ② 原因追及（Why）ロジックツリー

目的：確定した問題について、「**なぜ起きているか**」を MECE に分解したロジックツリーを drawio で作り、
ユーザーと一緒に改善しながら**根本原因を出し切る**。挙げた原因は**絞らず・捨てず・等価に扱い**、すべて③で対応策につなぐ。
出し切った**末端原因には識別番号（C1, C2, …）を付け**、drawio にも表示する（③で同じ番号を使って対応をたどる）。

> **この段階では原因を絞らない。** 「重点」「真因◯個」といった選別はしない。少数の原因だけを思考の起点にせず、
> 出した原因はすべて同じ重みで③に渡す。優先順位（着手順）は④で決めるだけで、ここで原因を取捨選択しない。

作り方・MECE のチェックは `harness/_mece_guide.md` を必ず参照すること。識別番号の付け方は `harness/templates/_format.md`「識別番号（ID）」を参照。

---

## 進め方

### ステップ A：ツリーの初稿を作る

1. `output/01_問題定義.md`（問題ステートメント）をツリーの**頂点**に置く。
2. 最初の枝分かれは、**MECE な分解の軸**を1つ選ぶ（軸の選び方は `_mece_guide.md`）。
   - 例：プロセス軸／構成要素軸（人・モノ・カネ・情報、4M）／内と外 など。
3. 各枝について「**なぜ？**」を繰り返し、さらに枝分かれさせる（深さの目安は3〜5階層）。
4. **打ち切る条件**：その原因が
   - ① 自分たちで**手を打てる**レベルまで具体的で、かつ
   - ② **事実・データで確かめられる**ところ、まで来たら止める。
5. 各原因が「**仮説**」か「**確認済み（事実あり）**」かを区別してメモする。

> **5 Whys との関係**：「なぜ？」を5回ほど掘るのが基本ですが、原因は1本道とは限りません。
> 枝分かれさせて**複数の原因を並べる**のがロジックツリーの強みです。

### ステップ B：drawio で図にして output に保存（末端原因に C番号）

`templates/02_原因ツリー_why.md` の雛形に沿って `output/02_原因ツリー_why.md` を作り、図そのものは
`output/02_原因ツリー_why.drawio`（drawio / mxGraph XML）として保存する。**左→右**（頂点が左、末端が右）で描く。

- **すべての原因を同じスタイル（等価）で描く**——特定の原因だけを色で強調しない（強調＝事実上の絞り込みになるため）。
- **末端原因（葉）には識別番号 `C1, C2, …` を付け、ノードのラベル先頭に表示する**（例：`C1 見積書を手作業で作成`）。mxCell の `id` も同じ `C1` にそろえると、③でエッジを追いやすい。中間ノード（カテゴリ）には番号は不要。
- **座標は `templates/_format.md` の手順（葉を上から積み、親は子の中央）で計算し、エッジには接続点（`exitX/entryX`）を必ず付ける。**

下は**書き方の例**（営業部の残業問題。末端原因 C1〜C6）。`source`/`target` でノードの `id` をつないでツリーにする。

```xml
<mxfile host="app.diagrams.net">
  <diagram id="why-tree" name="原因ツリー">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="826" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="P" value="問題：営業部の月残業が目標20hに対し平均45h" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#333333;fontStyle=1" vertex="1" parent="1"><mxGeometry x="40" y="340" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="KA" value="業務量・作業が多い" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="340" y="140" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="KB" value="承認で停滞する" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="340" y="390" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="KC" value="新人の立ち上がりが遅い" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="340" y="540" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="C1" value="C1 見積書を手作業で作成" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="640" y="40" width="240" height="60" as="geometry" /></mxCell>
        <mxCell id="C2" value="C2 報告書も手作業で作成" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="640" y="140" width="240" height="60" as="geometry" /></mxCell>
        <mxCell id="C3" value="C3 案件情報が個人のExcelに散在" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="640" y="240" width="240" height="60" as="geometry" /></mxCell>
        <mxCell id="C4" value="C4 承認者が1人に集中している" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="640" y="340" width="240" height="60" as="geometry" /></mxCell>
        <mxCell id="C5" value="C5 承認ルールが不明確" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="640" y="440" width="240" height="60" as="geometry" /></mxCell>
        <mxCell id="C6" value="C6 新人が手順を聞いて回る" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="640" y="540" width="240" height="60" as="geometry" /></mxCell>
        <mxCell id="ePKA" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="P" target="KA"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="ePKB" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="P" target="KB"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="ePKC" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="P" target="KC"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eKAC1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="KA" target="C1"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eKAC2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="KA" target="C2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eKAC3" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="KA" target="C3"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eKBC4" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="KB" target="C4"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eKBC5" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="KB" target="C5"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eKCC6" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="KC" target="C6"><mxGeometry relative="1" as="geometry" /></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

> 上は**書き方の例**です。実際の中身はユーザーの問題に合わせて作ること。座標は `_format.md` の手順
> （葉を上から積み、親は子の中央／エッジに接続点）で計算すれば、開いた時点で整列しています。
> **末端原因 C1〜C6 はそのまま ③ の起点になり、③でも同じ C番号で対応をたどる。**
> Markdown 側（`02_原因ツリー_why.md`）には、この `.drawio` へのリンクと、**ツリー構造の箇条書き**、**C番号つきの根本原因一覧**を残すこと。

### ステップ C：ユーザーに見せて、一緒に改善する（重要なループ）

図を提示し、**こちらから問いかけて**コメントを促す。例：

```
原因の初稿を作りました（output/02_原因ツリー_why.md）。一緒に見てください。

確認したいポイント：
- 抜けている原因はありませんか？（モレ）
- 同じことを別の枝で重複して書いていませんか？（ダブり）
- 「これは違う」「ここが本当の原因に近い」と感じる枝はどれですか？
- 事実やデータで確かめられている枝はどれですか？

気になる点を教えてください。一緒に直していきます。
```

ユーザーのコメントを受けたら：
1. ツリーを**直す**（枝の追加・削除・付け替え・言い換え）。
2. 直した図を再提示し、**何をどう変えたか**を一言添える。
3. 「他に気になる点はありますか？」と再度促す。
4. **ユーザーが「これで良い」と言うまで繰り返す。** Claude から打ち切らない。

毎回、`output/02_原因ツリー_why.drawio`（図）と `output/02_原因ツリー_why.md`（リンク＋箇条書き）の両方を上書き更新する。
枝を直したら**末端原因の C番号を振り直す**（抜け番・重複がないように）。

### ステップ D：根本原因を全件、C番号つきで一覧化する（絞らない・捨てない）

ツリーに納得が得られたら、**末端の原因（根本原因）を全部、C番号つきでリストにする**。ここで原因を絞らない・捨てない——
挙げた原因はすべて、③で対応策をつける対象になる。**どれか少数を「重点」として選ぶことはしない**。

```
このツリーの末端にある原因を、C1・C2… と番号を振って全部書き出します。
どれも等しく③で対応策を考えます（ここでは取捨選択や順位づけはしません）。
抜けている原因や、まとめ直したい原因があれば教えてください。
```

`output/02_原因ツリー_why.md` の「根本原因の一覧（全件）」に末端原因を**すべて C番号つきで**書く。
原因に「事実／仮説」の状態を併記する（影響度や優先順位はここでは付けない——④で着手順として扱う）。

### ステップ E：次へ

「**洗い出したすべての原因（C1〜Cn）に対して、対応策（③）を考えてよいですか？**」と確認し、合意できたら
`harness/02_how_tree.md` に進む。すべての原因を等価に扱い、漏らさず対応策をつける。

---

## 注意

- **原因に「対策」を混ぜない。** ここでは「なぜ起きているか」だけ。対策は③で。
- **原因を絞らない・捨てない・順位づけしない。** 「重点」「真因◯個」の選別はしない。全原因を等価に扱い、実行の順番（着手順）は④で決める。
- **末端原因には C番号を付ける。** drawio のラベルにも表示し、③で同じ番号を使う（書式は `_format.md`）。
- 「なぜ？」の答えが**人のせい（〇〇さんが悪い）で止まらない**こと。仕組み・条件まで掘る。
- 推測は推測と明記し、可能なら「どう確かめるか」もメモする。
- 1階層の枝は **MECE** を点検（`_mece_guide.md` のチェックリスト）。
- ツリーが大きくなりすぎたら、頂点に近い軸を見直す（分け方が悪いサイン）。重要な枝は深く、軽い枝は浅くてよい。

以上。原因の全件洗い出し（C番号つき）に合意が取れたら ③ `harness/02_how_tree.md` へ。
