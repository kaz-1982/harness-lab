# templates/_format.md — 書式ルール

生成する全ドキュメント共通の書式。

## 見出し
- `#` はドキュメントタイトルに1つだけ
- 章は `##`、節は `###`

## 表記
- 日本語。です・ます調。
- 専門用語は初出で括弧書き説明：例「MECE（モレなく・ダブりなく分けること）」
- 箇条書きは `-` で統一

## 図（drawio）

ロジックツリー・マトリクス・フロー図は **drawio（diagrams.net）形式の独立ファイル**として出力する。

### 出力ルール
- 図は `output/` に **`.drawio` ファイル**として保存する（例：`02_原因ツリー_why.drawio`）。
- 対応する Markdown（例：`02_原因ツリー_why.md`）には、図そのものは貼らず**リンクと箇条書きの構造**を載せる：
  - `> 図：[02_原因ツリー_why.drawio](02_原因ツリー_why.drawio)（drawio / diagrams.net で開く）`
  - そのあとに**ツリー構造を箇条書き**で必ず残す（会話中に一目で読めるように。drawio を開けない環境でも構造が分かる）。
- ロジックツリーは **左→右**（頂点が左、末端が右）を基本とする。

### .drawio ファイルの書き方（mxGraph XML）
骨格は以下。`root` 内に `id="0"` と `id="1"` を必ず置き、ノード（`vertex="1"`）とエッジ（`edge="1"`）を `parent="1"` で並べる。

```xml
<mxfile host="app.diagrams.net">
  <diagram id="why-tree" name="原因ツリー">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="826" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="P" value="問題：（ここに問題）" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#333333;fontStyle=1" vertex="1" parent="1">
          <mxGeometry x="40" y="40" width="220" height="60" as="geometry" />
        </mxCell>
        <mxCell id="A" value="（原因カテゴリA）" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1">
          <mxGeometry x="340" y="40" width="220" height="60" as="geometry" />
        </mxCell>
        <mxCell id="eA" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="P" target="A">
          <mxGeometry relative="1" as="geometry" />
        </mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

### スタイル（style 属性）
- 通常ノード：`rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333`
- 頂点（問題・目標）：上に `fontStyle=1` と `fillColor=#f5f5f5` を付けて区別
- **原因ノード（②）は全件、通常ノード（白）で等価に描く。** 特定の原因を色で強調・選別しない（強調＝事実上の絞り込みになり、ほかの原因が軽視されるため）。
- **本筋／複数原因に効く施策（③）**：`rounded=1;whiteSpace=wrap;html=1;fillColor=#e6ffe6;strokeColor=#22aa22;strokeWidth=2`
  - 「複数の原因をまとめて解決する施策・レベルを上げた本筋のアプローチ」を緑で強調する印。「すぐ作れる」を表す印ではない。
- エッジ：`edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0`
  - **接続点を固定**：親の右辺中央（`exitX=1;exitY=0.5`）から子の左辺中央（`entryX=0;entryY=0.5`）へ出す。これで矢印が水平に走り、斜めや交差を防ぐ。
- ラベル内の改行は `&#10;`（または `html=1` のまま `<br>`）

### 座標ルール（生成時に崩れないツリーを描く）

drawio は座標を自分で指定する。**手動の「水平ツリー」に頼らず、生成する時点で整列した座標を計算して書き込む。**
ポイントは1つだけ：**親ノードを、その子ノード群の「縦の中央」に置く**こと。これで矢印が水平に走り、斜め・交差・重なりが消える。

**定数（目安）**：ノード幅 `W=220`／高さ `H=60`／列の間隔 `COLGAP=300`／行の間隔 `ROW=100`／原点 `(40, 40)`。

**計算手順（ボトムアップ）**：

1. **横（x）= 深さ**：`x = 40 + 深さ × 300`（頂点が深さ0）。同じ深さのノードは必ず同じ x にそろえる。
2. **葉（子を持たないノード）に縦位置を割り当てる**：ツリーを上の枝から順にたどり（DFS・兄弟順）、
   出てきた葉に上から `i = 0, 1, 2, …` を振って `y = 40 + i × 100`。
   - 葉は**深さがばらばらでもよい**（浅い枝の末端も1行を使う）。とにかく「末端」を上から積む。
3. **親（子を持つノード）の縦位置 = 子群の中央**：葉から根に向かって計算する。
   `親.y =（いちばん上の子.y ＋ いちばん下の子.y）÷ 2`。
   - 子が1つなら、親.y はその子.y と同じになる（＝矢印が真横に）。
4. **エッジ**は接続点を固定する（スタイルの `exitX/exitY/entryX/entryY` を必ず付ける）。

**ワークト例**（葉を上から積み、親を子の中央に置いた結果。この座標はそのまま整列する）：

```
P ┳ A ┳ A1        葉の順(DFS): A1, A2, B1, C  →  y = 40,140,240,340
  ┃   ┗ A2        A.y=(40+140)/2=90   B.y=240(子1つ)   P.y=(90+340)/2=215
  ┣ B ━ B1        x: 深さ0→40  深さ1→340  深さ2→640
  ┗ C
```

```xml
        <mxCell id="P" value="問題" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#333333;fontStyle=1" vertex="1" parent="1"><mxGeometry x="40" y="215" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="A" value="A" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="340" y="90" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="A1" value="A1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="640" y="40" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="A2" value="A2" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="640" y="140" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="B" value="B" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="340" y="240" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="B1" value="B1" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="640" y="240" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="C" value="C" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="340" y="340" width="220" height="60" as="geometry" /></mxCell>
        <mxCell id="ePA" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="P" target="A"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="ePB" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="P" target="B"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="ePC" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="P" target="C"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eAA1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="A" target="A1"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eAA2" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="A" target="A2"><mxGeometry relative="1" as="geometry" /></mxCell>
        <mxCell id="eBB1" style="edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;endArrow=block;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0" edge="1" parent="1" source="B" target="B1"><mxGeometry relative="1" as="geometry" /></mxCell>
```

**仕上げの検算（保存前に必ず確認）**：
- [ ] 同じ深さ（同じ x）の隣り合うノードは、y の差が `H+10 = 70` 以上あるか（重なり防止）。
- [ ] すべての親ノードの y が、その子ノードの y の範囲内に収まっているか（中央に来ているか）。
- [ ] すべてのエッジに `exitX=1;exitY=0.5` と `entryX=0;entryY=0.5` が付いているか。
- [ ] ノードが多くて窮屈なら `ROW` を 120〜140 に広げる。ラベルが3行以上なら、そのノードだけ `height` を増やす。

> 補助：それでも気になる場合は drawio で **「配置 → レイアウト → 水平ツリー」**（Arrange → Layout → Horizontal Tree）を押すと再整列できる。
> ただし**主目標は「生成した時点で崩れていない」こと**。手動整列を前提にしない。

> エッジの `source` / `target` には、つなぐノードの `id` を入れる。`id` は枝の意味がわかる短い英数字（`P` `A` `A1` `A1a` など）にすると、修正時に追いやすい。

### 収束させる図（③対応策ツリー）の座標

③対応策ツリーは「**原因（全件）→ 対策（原因の数だけ・1対1）→ 収束した対策（必要に応じて）→ 本筋**」と
左→右に並べ、**必要なところだけ右へ収束**させる。座標は通常ツリーと同じ「中央寄せ」で計算する。

1. **横（x）= 列**：原因 → 1対1の対策 → 収束対策 → 本筋。同じ列は同じ x にそろえる（例：`40` / `330` / `620` / `910`）。
2. **原因と1対1の対策は同じ y にそろえる**：末端原因に上から `y = 40 + i × 90` を振り、その**真横（同じ y）に対応する対策**を置く。矢印が水平に走り、原因↔対策の対応が一目で分かる。
3. **収束した対策の y = 束ねる対策群の中央**、**本筋の y = 束ねる収束対策群の中央**：`(上端 + 下端) ÷ 2`。
4. **収束は必要なところだけ。** 束ねない対策はそのまま右へ送ってよい（原因の数だけ対策が残ってもよい）。
5. エッジは右辺中央（`exitX=1;exitY=0.5`）→左辺中央（`entryX=0;entryY=0.5`）。多対一でも水平に近く整う。右へ行くほどノード数は同じか減る（増やさない）。

## 識別番号（ID）— 必ず付け、drawio のラベルにも表示する
- **末端原因**：`C1, C2, C3, …`（C＝原因）。②で採番し、②③両方のノードラベル先頭に表示。
- **1対1の対策**：`M1, M2, M3, …`（M＝対策）。**原因 `Cn` に対応する対策を `Mn`** とし、番号をそろえて1対1を明示。
- **収束した対策**：`T1, T2, …`（T＝とりまとめ）。ラベルに束ねた対策を併記（例：`T1 営業支援ツール導入（M1+M2+M3）`）。単独なら `T3 …（M6・単独）`。
- **本筋アクション**：`A1, A2, …`（A＝アクション）。束ねた収束対策を併記（例：`A1 …（T1+T2+T3）`）。
- **表示のしかた**：drawio 各ノードの value 先頭に番号を入れる（例：`C1 見積書を手作業で作成`）。mxCell の `id` も同じ番号にそろえると、エッジ・修正時に追いやすい。
- **②と③で同じ C番号**を使い、`Cn → Mn → Tk → An` と対応をたどれるようにする。Markdown の対応表・収束表も同じ番号で書く。原因・対策を増減したら番号を振り直す（抜け番・重複なし）。

## その他
- 1ドキュメント1ファイル
- 図や表は、説明文とセットにする（図だけ・表だけにしない）
