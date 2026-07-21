---
{
  "id": "crawler-shop_urlUNI-024",
  "domain": "crawler",
  "source": "knowledge/crawler/06-1688-factory-monitor.md",
  "q": "shop_url UNIQUE 约束导致空字符串覆盖问题的解决方案是什么？",
  "a": "初始 `shop_url=card_url`（每家不同）+ 新增专用 `catalog_url` 字段，避免空占位符冲突。",
  "created": "2026-07-21",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-21",
  "reviews": 0
}
---

**Q**: shop_url UNIQUE 约束导致空字符串覆盖问题的解决方案是什么？

**A**: 初始 `shop_url=card_url`（每家不同）+ 新增专用 `catalog_url` 字段，避免空占位符冲突。
