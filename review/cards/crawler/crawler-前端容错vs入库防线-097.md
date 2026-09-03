---
{
  "id": "crawler-前端容错vs入库防线-097",
  "domain": "crawler",
  "source": "knowledge/crawler/15-html-parsing.md",
  "q": "前端容错 vs 入库防线，分别是什么？",
  "a": "- 前端（采集侧）= **默认值 / 降级链 / null 兜底**（不是\"多抓\"——那是采集策略）\n  - 入库 = 契约校验 / 类型校验 / **坏行隔离**（严、宁缺毋滥）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 前端容错 vs 入库防线，分别是什么？

**A**: - 前端（采集侧）= **默认值 / 降级链 / null 兜底**（不是"多抓"——那是采集策略）
  - 入库 = 契约校验 / 类型校验 / **坏行隔离**（严、宁缺毋滥）
