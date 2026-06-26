---
adr_id: ADR-0001
title: サーバサイド言語に TypeScript を採用
status: Accepted
date: 2026-06-26
deciders: テックリード, PM
origin: design
related: B-2
---

# ADR-0001 サーバサイド言語に TypeScript を採用

> 原典外・ハーネス拡張(MADR 形式)。

## コンテキスト
本 SaaS のサーバサイド実装言語を決める必要がある。
チームの既存スキル分布、ライブラリエコシステム、性能要件 R-NF-001(CSV 出力 3 秒以内、8,000 件)とのバランスを判断する。

## 決定
TypeScript 5.x + NestJS 10 + Prisma 5 を採用する。

## 検討した選択肢
- **TypeScript / NestJS**: チームの既存スキルが揃っており、Prisma による DB アクセスも快適。性能は十分実現可能。
- **Go / Echo**: 性能面で安心だが、チームに本格的な経験者が PM のみ。教育コストが高い。
- **Python / FastAPI**: 速度は遅め。ORM の選択肢が散らばっており保守性に不安。

## 影響(Consequences)
- 良い影響:
  - チームの立ち上がりが早い(初日からテストを書ける)
  - 共通の Zod スキーマで Frontend / API のバリデーションを統一できる
- 注意点:
  - 8,000 件の CSV 出力で 3 秒以内に収まるかは、初期スプリントで負荷テストを実施して確認する
  - V8 / Node.js の世代を 20 LTS で固定し、本番更新時は ADR を別途起こす

## 関連
- B-2 ソフトウェアアーキテクチャ設計書 §4.4 技術スタック
