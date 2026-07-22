---
{
  "id": "crawler-多SKU京东页面的价-032",
  "domain": "crawler",
  "source": "knowledge/crawler/08-jd-parser-frontend.md",
  "q": "多 SKU 京东页面的价格如何采集？",
  "a": "循环匹配全部 `class=price value` 块，15-18 个价格变体，取 min 为售价、max 为原价",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: 多 SKU 京东页面的价格如何采集？

**A**: 循环匹配全部 `class=price value` 块，15-18 个价格变体，取 min 为售价、max 为原价
