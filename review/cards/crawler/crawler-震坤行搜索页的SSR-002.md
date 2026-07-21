---
{
  "id": "crawler-震坤行搜索页的SSR-002",
  "domain": "crawler",
  "source": "knowledge/crawler/01-b2b-platforms-anti-crawl.md",
  "q": "震坤行搜索页的 SSR 数据提取关键字段映射是什么？",
  "a": "搜索结果通过 `window.__INITIAL_DATA__` JSON 嵌入 HTML，字段映射：`proSkuProductName`→标题、`proBrandName`→品牌、`proMaterialNo`→型号、`proSkuNo`→编码。",
  "created": "2026-07-21",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-21",
  "reviews": 0
}
---

**Q**: 震坤行搜索页的 SSR 数据提取关键字段映射是什么？

**A**: 搜索结果通过 `window.__INITIAL_DATA__` JSON 嵌入 HTML，字段映射：`proSkuProductName`→标题、`proBrandName`→品牌、`proMaterialNo`→型号、`proSkuNo`→编码。
