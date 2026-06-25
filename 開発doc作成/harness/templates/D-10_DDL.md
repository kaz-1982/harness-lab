---
doc_id: D-10
doc_name: DDL
phase: 詳細設計
required_when: 全規模・全手法で必須
depends_on: [D-9]
mode: 両対応
---

# {{案件名}} - DDL

## 1. 目的
実際に DB に適用する CREATE 文 / ALTER 文を確定する。
本書は D-9 テーブル定義書を機械的に DDL 化したものであり、本書がそのまま実装リポジトリの初期マイグレーションになる。

## 2. 適用範囲・スコープ
- 含むもの: {{CREATE TABLE / CREATE INDEX / ALTER TABLE / 必要時 VIEW / TRIGGER}}
- 含まないもの: {{データ投入(初期マスタは別ファイル) / マイグレーション運用(B-17 運用設計書で扱う)}}

## 3. 前提・依存
- 参照ドキュメント: D-9 テーブル定義書・インデックス設計書, D-8 物理データモデル
- 採番済ID: テーブル T-* は D-8 / D-9 で確定済
- 採用 DB: {{D-8 と整合}}
- マイグレーションツール: {{例: Flyway / Liquibase / Prisma Migrate / 直接 SQL}}

## 4. 本文

### 4.1 採用 DB と DDL 方言
{{採用 DB 製品とバージョン、DDL の方言(MySQL / PostgreSQL / Oracle / SQL Server)}}

### 4.2 DDL 本体

```sql
-- T-001: t_customer
CREATE TABLE t_customer (
  customer_id  VARCHAR(10)  NOT NULL,
  name         VARCHAR(50)  NOT NULL,
  email        VARCHAR(100) NOT NULL,
  created_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (customer_id),
  UNIQUE KEY uk_customer_email (email)
);

-- T-002: t_order
CREATE TABLE t_order (
  order_id      VARCHAR(20)   NOT NULL,
  customer_id   VARCHAR(10)   NOT NULL,
  order_date    DATE          NOT NULL,
  total_amount  DECIMAL(12,0) NOT NULL DEFAULT 0,
  status        VARCHAR(20)   NOT NULL,
  customer_name VARCHAR(50)   NULL,
  created_at    TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (order_id),
  FOREIGN KEY (customer_id) REFERENCES t_customer(customer_id),
  CHECK (total_amount >= 0)
);
CREATE INDEX idx_order_customer_date ON t_order (customer_id, order_date);
CREATE INDEX idx_order_status        ON t_order (status);
```

### 4.3 適用順序
| # | 対象 | コマンド種別 | 備考 |
|---|---|---|---|
| 1 | t_customer | CREATE TABLE | 最初に作成(FK の親) |
| 2 | t_order | CREATE TABLE | FK が t_customer を参照 |
| 3 | t_order インデックス | CREATE INDEX | テーブル作成後 |

### 4.4 ロールバック方針
- DROP 順序は CREATE の逆順(t_order → t_customer)
- 本番適用前にステージング環境で DRY RUN
- マイグレーション失敗時の切り戻し: {{ツール固有の手順}}

### 4.5 初期マスタ(別ファイル参照)
初期マスタデータは本書ではなく `output/05_詳細設計/seeds/` 等の別ファイルで管理する(本書は DDL のみ)。

## 5. 関連トレーサビリティ
- 上流: D-9 テーブル定義書・インデックス設計書 / D-8 物理データモデル
- 下流:
  - 実装リポジトリのマイグレーション
  - B-17 運用設計書(マイグレーション運用手順)

## 6. 改訂履歴
| 版 | 日付 | 変更者 | 変更内容 |
|---|---|---|---|
| 0.1 | YYYY-MM-DD | | 初版作成 |

## 7. レビュー状態
- 単体品質チェック: 未 / 実施済(YYYY-MM-DD)
- 整合性チェック: 未 / 実施済(YYYY-MM-DD)
- TBD / 残課題:
  - (なし、または箇条書き)
- 承認: 未 / 承認(承認者、日付)

---

### 補足: 記入例(参考)

> ```sql
> CREATE TABLE t_order (
>   order_id     VARCHAR(20)   NOT NULL,
>   customer_id  VARCHAR(10)   NOT NULL,
>   order_date   DATE          NOT NULL,
>   total_amount DECIMAL(12,0) NOT NULL DEFAULT 0,
>   status       VARCHAR(20)   NOT NULL,
>   created_at   TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
>   PRIMARY KEY (order_id),
>   FOREIGN KEY (customer_id) REFERENCES t_customer(customer_id)
> );
> CREATE INDEX idx_customer_date ON t_order (customer_id, order_date);
> ```
