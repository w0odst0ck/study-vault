---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - 数据工程
  - Hive
  - 数仓
  - Hadoop
cards: []
---

# 数据仓库与 Hive 基础

> 数仓分层 / Hive SQL / 数据建模
> 来源：旧知识库「Knowledge-Base-for-Interviews」

---

## 1. 数仓分层

| 层级 | 名称 | 作用 |
|------|------|------|
| ODS | 操作数据层 | 原始数据，不做任何处理 |
| DWD | 明细数据层 | 清洗、去重、标准化 |
| DWS | 汇总数据层 | 轻度汇总，按主题组织 |
| ADS | 应用数据层 | 面向具体业务的数据 |

**核心原则**：下层不可被跨层引用、数据只向下流动。

---

## 2. Hive SQL 核心差异

| 项目 | Hive | 传统 SQL |
|------|------|---------|
| 存储 | HDFS | 本地磁盘 |
| 执行引擎 | MapReduce/Tez/Spark | 本地引擎 |
| 事务 | 不支持（ACID 有限） | 完整支持 |
| 索引 | 无（分区+分桶替代） | B+树 |
| 存储格式 | Parquet/ORC/AVRO | 行存 |

### Hive 特有语法

```sql
-- 分区表
CREATE TABLE orders (
  id INT, amount DOUBLE
) PARTITIONED BY (dt STRING)

-- 分桶表
CLUSTERED BY (user_id) INTO 10 BUCKETS

-- 行转列
SELECT id, SUM(IF(type='A', val, 0)) AS type_a,
          SUM(IF(type='B', val, 0)) AS type_b
FROM t GROUP BY id

-- 列转行（炸裂）
SELECT id, category
FROM t LATERAL VIEW EXPLODE(categories) t2 AS category
```

---

## 3. 数据建模

| 模型 | 适用 | 特点 |
|------|------|------|
| 星型模型 | 分析场景 | 中心事实表 + 维度表，查询快 |
| 雪花模型 | 复杂维度 | 维度表再细分，空间换时间 |
| 宽表 | 快速查询 | 冗余存储，减少 JOIN |

### 事实表 vs 维度表

| | 事实表 | 维度表 |
|--|--------|--------|
| 内容 | 业务度量（订单金额） | 描述属性（用户信息） |
| 变化 | 不断增长 | 缓慢变化 |
| 粒度 | 细 | 粗 |

---

## 回顾

- Q: 数仓分层的目的是什么？
  A: 数据解耦（变动互不影响）、数据复用（下层清洗上层直接用）、权限管控

- Q: Hive 分区和分桶的区别？
  A: 分区是目录划分（按日期），分桶是文件划分（按 hash）。分区减少扫描范围，分桶优化 JOIN/抽样

- Q: Hive 行转列和列转行的常用方法？
  A: 行转列用 `SUM(IF(...))` 或 `CASE WHEN` 配合聚合；列转行用 `LATERAL VIEW EXPLODE`

- Q: 星型模型和雪花模型的优缺点？
  A: 星型查询快（JOIN 少）、冗余多；雪花模型规范化、空间省但 JOIN 多性能差

- Q: 事实表有哪些类型？
  A: 事务事实表（每笔交易）、周期快照事实表（每天快照）、累积快照事实表（流转过程）
