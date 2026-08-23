---
{
  "id": "data-engineering-Hive行转列和列转行-008",
  "domain": "data-engineering",
  "source": "knowledge/data-engineering/02-hive-data-warehouse.md",
  "q": "Hive 行转列和列转行的常用方法？",
  "a": "行转列用 `SUM(IF(...))` 或 `CASE WHEN` 配合聚合；列转行用 `LATERAL VIEW EXPLODE`",
  "created": "2026-07-22",
  "last_reviewed": "2026-08-23",
  "interval": 1,
  "ease": 2.36,
  "next_review": "2026-08-24",
  "reviews": 1
}
---

**Q**: Hive 行转列和列转行的常用方法？

**A**: 行转列用 `SUM(IF(...))` 或 `CASE WHEN` 配合聚合；列转行用 `LATERAL VIEW EXPLODE`
