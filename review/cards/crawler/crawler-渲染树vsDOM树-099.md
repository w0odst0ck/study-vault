---
{
  "id": "crawler-渲染树vsDOM树-099",
  "domain": "crawler",
  "source": "knowledge/crawler/16-browser-render.md",
  "q": "渲染树 vs DOM 树？display:none 在哪？",
  "a": "DOM = 全量结构（含隐藏元素）；渲染树 = 只含**可见**元素（display:none 在 DOM 但不在渲染树，不占布局）；head 内容也不在渲染树",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 渲染树 vs DOM 树？display:none 在哪？

**A**: DOM = 全量结构（含隐藏元素）；渲染树 = 只含**可见**元素（display:none 在 DOM 但不在渲染树，不占布局）；head 内容也不在渲染树
