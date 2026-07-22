---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - SQL
  - 窗口函数
  - 数据工程
  - 面试
cards: []
---

# SQL 面试核心：窗口函数、CTE、性能优化

> 数据岗手撕 SQL 必考
> 来源：旧知识库「Knowledge-Base-for-Interviews」

---

## 1. 窗口函数

### 语法

```sql
SELECT 字段,
       SUM(amount) OVER (PARTITION BY region ORDER BY date) AS cum_total
FROM sales
```

**三要素**：`PARTITION BY`（分组） + `ORDER BY`（排序） + `ROWS/RANGE`（窗口范围）

### 常用窗口函数

| 类型 | 函数 | 用途 |
|------|------|------|
| 排名 | `ROW_NUMBER()` / `RANK()` / `DENSE_RANK()` | 分组排名 |
| 聚合 | `SUM()` / `AVG()` / `COUNT()` OVER(...) | 累计/移动计算 |
| 偏移 | `LAG()` / `LEAD()` | 获取前后行值 |
| 分桶 | `NTILE(n)` | 按顺序分 n 组 |

### 面试高频场景

```sql
-- 分组 TOP N：每个部门工资最高的前 3 名
SELECT * FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY dept ORDER BY salary DESC) AS rn
  FROM employees
) t WHERE rn <= 3

-- 同比环比：本月 vs 上月
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month) AS prev_month,
       (revenue - LAG(revenue) OVER (ORDER BY month)) / LAG(revenue) OVER (ORDER BY month) AS growth
FROM monthly_revenue
```

---

## 2. CTE 与子查询

```sql
-- CTE：比子查询更清晰，可复用
WITH top_dept AS (
  SELECT dept, AVG(salary) AS avg_sal
  FROM employees GROUP BY dept
  ORDER BY avg_sal DESC LIMIT 3
)
SELECT e.name, e.dept, e.salary
FROM employees e
JOIN top_dept t ON e.dept = t.dept

-- 递归 CTE：树形结构（组织架构、类目）
WITH RECURSIVE org_tree AS (
  SELECT id, name, manager_id, 1 AS level
  FROM org WHERE manager_id IS NULL
  UNION ALL
  SELECT e.id, e.name, e.manager_id, t.level + 1
  FROM org e JOIN org_tree t ON e.manager_id = t.id
)
SELECT * FROM org_tree
```

---

## 3. 性能优化

### 执行顺序

```
FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

### 优化原则

| 原则 | 错误做法 | 正确做法 |
|------|---------|---------|
| 减少数据量 | SELECT * | 只选需要的列 |
| 利用索引 | WHERE 函数(列) = 值 | WHERE 列 = 值 |
| 避免 DISTINCT | 用 DISTINCT 去重 | 先确认是否真的需要，或用 EXISTS |
| JOIN 顺序 | 大表 JOIN 小表 | 小表驱动大表 |
| 避免 NULL | `!=` 排除 NULL 失效 | `IS NULL` 或 `COALESCE` |

---

## 回顾

- Q: ROW_NUMBER()、RANK()、DENSE_RANK() 的区别？
  A: 并列时 ROW_NUMBER() 随机分配、RANK() 跳过后续排名、DENSE_RANK() 不跳过

- Q: LAG() 和 LEAD() 的作用？
  A: LAG(col, n) 获取前 n 行的值，LEAD(col, n) 获取后 n 行的值

- Q: CTE 相比子查询的优势？
  A: 可复用、可递归、逻辑更清晰、调试方便

- Q: 窗口函数和 GROUP BY 的区别？
  A: GROUP BY 聚合后行数减少，窗口函数不减少行数且保留原数据

- Q: SQL 执行顺序是什么？
  A: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
