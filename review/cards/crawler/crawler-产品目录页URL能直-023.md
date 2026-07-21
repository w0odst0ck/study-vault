---
{
  "id": "crawler-产品目录页URL能直-023",
  "domain": "crawler",
  "source": "knowledge/crawler/06-1688-factory-monitor.md",
  "q": "产品目录页 URL 能直接从 shopURL 推导出来吗？",
  "a": "不能。必须从名片页 DOM 中通过 `data-btrack=\"pc-card-shop-gallery-btn\"` 属性定位入口获取。",
  "created": "2026-07-18",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-18",
  "reviews": 0
}
---

**Q**: 产品目录页 URL 能直接从 shopURL 推导出来吗？

**A**: 不能。必须从名片页 DOM 中通过 `data-btrack="pc-card-shop-gallery-btn"` 属性定位入口获取。
