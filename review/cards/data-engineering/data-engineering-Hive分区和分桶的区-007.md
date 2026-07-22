---
{
  "id": "data-engineering-Hive分区和分桶的区-007",
  "domain": "data-engineering",
  "source": "knowledge/data-engineering/02-hive-data-warehouse.md",
  "q": "Hive 分区和分桶的区别？",
  "a": "分区是目录划分（按日期），分桶是文件划分（按 hash）。分区减少扫描范围，分桶优化 JOIN/抽样",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: Hive 分区和分桶的区别？

**A**: 分区是目录划分（按日期），分桶是文件划分（按 hash）。分区减少扫描范围，分桶优化 JOIN/抽样
