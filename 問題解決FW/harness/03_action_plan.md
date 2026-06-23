# 03_action_plan.md — ④ 優先順位づけ・アクションプラン

目的：対応策ツリーで出したすべての施策を、まず**品質ゲート（既定＝市販品同等以上・POC不可）**で点検し、
そのうえで**効果（インパクト）の大きい順**に着手順をつけ、「誰が・何を・どの品質で」が分かる**実行計画**に仕上げる。

> **QCD は Q（品質）が最優先。** コスト・納期（C/D＝工数・期間・コスト）は**優先順位の判断軸にしない**（実装力は Claude が支えるため）。
> 優先順位は『**効果（インパクト）**』だけで決める。「すぐできる・安い」を理由に順位を上げ下げしない。
> **施策を C/D で捨てない**——全施策を実行対象として残し、着手の順番だけを効果で決める（数を無理に絞らない＝収束は強制しない）。

---

## 進め方

### ステップ A：施策を一覧にする

`output/03_対応策ツリー_how.md` の**対応策・本筋アクション（右側の打ち手）**を**すべて**抜き出して一覧にする。
各打ち手に「**担当する原因（複数可）**」と「**目指す品質水準（比較対象）**」も併記する（③で決めたもの）。

### ステップ B：品質ゲート → 効果（インパクト）で並べる

**(1) 品質ゲート（先に通す）**：各施策が「目指す品質水準（既定＝市販・既存サービス同等以上・POC不可）」を満たせるかを確認する。
- 満たせない施策は、**外すのではなく品質を満たすよう作り込む**（手段を変える・既製品を使う・本筋に引き上げる等）。
- どうしても品質に届かない案だけを落とす。**「すぐできるが品質が低い（POC 止まり）」案を優先しない**——品質は譲らない前提。

**(2) 効果（インパクト）で並べる**：品質ゲートを通った施策を、**効果の大きさだけ**で序列する（大／中／小で十分）。

- **効果**：原因にどれだけ効くか／問題がどれだけ改善するか。複数原因に効く「束ね施策」や「本筋のアプローチ」は効果が大きいことが多い。
- **コスト・工数・期間・「すぐできるか」は順位に使わない。** それらは「着手の段取り」で考えることで、優先順位の判断軸にはしない。

効果の大きい順に施策を並べた図を `output/04_優先順位マトリクス.drawio`（drawio）として保存する。
**効果 大／中／小** の3つの帯（バンド）に施策ノードを置く（すべて品質ゲート通過済み）。drawio の書き方は `templates/_format.md` を参照。下は土台の例。
この帯の中に施策ノード（`fillColor=#ffffff` 等）を追加していく。

```xml
<mxfile host="app.diagrams.net">
  <diagram id="priority" name="効果（インパクト）順">
    <mxGraphModel dx="800" dy="600" grid="1" gridSize="10" guides="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="826" pageHeight="826" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
        <mxCell id="gate" value="品質ゲート：市販品同等以上・POC不可 を全施策が通過済み（届かない案は作り込むか本筋に引き上げる）" style="whiteSpace=wrap;html=1;fillColor=#f5f5f5;strokeColor=#999999;align=center;fontStyle=2" vertex="1" parent="1"><mxGeometry x="40" y="20" width="740" height="40" as="geometry" /></mxCell>
        <mxCell id="b1" value="効果 大（先に着手）" style="whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#999999;verticalAlign=top;align=left;fontStyle=1" vertex="1" parent="1"><mxGeometry x="40" y="80" width="740" height="150" as="geometry" /></mxCell>
        <mxCell id="b2" value="効果 中" style="whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#999999;verticalAlign=top;align=left;fontStyle=1" vertex="1" parent="1"><mxGeometry x="40" y="240" width="740" height="150" as="geometry" /></mxCell>
        <mxCell id="b3" value="効果 小（着手は後でも、捨てない）" style="whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#999999;verticalAlign=top;align=left;fontStyle=1" vertex="1" parent="1"><mxGeometry x="40" y="400" width="740" height="150" as="geometry" /></mxCell>
        <mxCell id="sA" value="施策A（本筋・複数原因に効く）" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#e6ffe6;strokeColor=#22aa22" vertex="1" parent="1"><mxGeometry x="80" y="130" width="200" height="50" as="geometry" /></mxCell>
        <mxCell id="sB" value="施策B" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="320" y="130" width="200" height="50" as="geometry" /></mxCell>
        <mxCell id="sC" value="施策C" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="80" y="290" width="200" height="50" as="geometry" /></mxCell>
        <mxCell id="sD" value="施策D" style="rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333333" vertex="1" parent="1"><mxGeometry x="80" y="450" width="200" height="50" as="geometry" /></mxCell>
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

- **効果 大 = 先に着手**。複数原因に効く束ね施策・本筋のアプローチが入りやすい。
- **効果 中／小 = 着手は後でよい**が、**捨てない**。手が回り次第まわす（「効果が小さい＝やらない」ではない）。
- **コスト・期間で帯を決めない。** 帯は効果の大きさだけで決める。

> Markdown 側（`04_アクションプラン.md`）には、この `.drawio` へのリンクと、**評価表（対応する原因・品質目標・効果・着手順の列）**を必ず載せる。
> drawio を開けない環境でも、表だけで着手順が分かるようにする。**「実現性」「コスト」の列は作らない**（順位の判断軸にしないため）。

### ステップ C：ユーザーと着手順を合意する

評価結果を見せ、「この順番（効果の大きい順）で着手していく形で合っていますか？」と確認する。
ユーザーの肌感を反映して調整する。**ただしコスト・納期を理由に施策を落とさない**（落とすのは品質ゲートに届かない案だけ）。

### ステップ D：アクションプランに落とす

効果の大きいものから、`templates/04_アクションプラン.md` に沿って
`output/04_アクションプラン.md` を作る。各施策について最低限：

- **何を**（施策）
- **目指す品質水準**（比較対象＝市販品・既存サービス等。これを下回ったら未完。POC は完了にしない）
- **対応する原因**（②のどの原因に効くか。複数可）
- **誰が**（担当）
- **どう確かめるか**（効果の測り方・完了の判断基準。**品質の合格ライン＝市販品と比べて見劣りしないか**を必ず入れる）

> 期限（いつまでに）は任意。引けるなら添えるが、**納期を優先順位の判断には使わない**。

### ステップ E：締めくくり

全体（①〜④）を3〜5行で振り返り、最初の問題ステートメントに立ち返って
「この計画で問題は解決に向かうか」を一緒に確認する。
必要なら前のステップに戻って見直す。

```
ここまでで、問題 → 原因（全件・等価）→ 対応策（全原因に対応・本筋あり）→ 実行計画（効果順）が整理できました。

  ・問題：（1文）
  ・本筋のアプローチ：（複数原因に効く打ち手）
  ・効果の大きい順の着手：（上から。いずれも品質は市販品同等以上・POC不可）

このプランで進めてみて、効果と品質を確かめながら見直していきましょう。
気になる点があれば、どのステップからでも戻れます。
```

---

## 注意

- **着手は効果の大きいものから。** ただし残りも**捨てずに残す**（効果小も含め、順次まわす）。数を無理に絞らない（収束は強制しない）。
- **品質は優先順位の対象にしない（ゲート）。** 「順位が低いから品質も下げる」はしない。やるなら市販品同等以上、できないなら作り込むか本筋に引き上げる。
- **コスト・納期（C/D）で順位を決めない・施策を捨てない。** 工数・期間・費用は判断軸にしない（実装力は Claude が支える）。
- 「どう確かめるか」を必ず入れる。効果と**品質の合格ライン**の両方を測れる形にする。
- 担当は仮でよい（ユーザーが決められる範囲で）。空欄なら「未定」と明記。

以上。`output/04_アクションプラン.md` を保存し、全体を振り返って完了。
