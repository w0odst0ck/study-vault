---
{
  "id": "crawler-商品数据存在于哪里re-107",
  "domain": "crawler",
  "source": "knowledge/crawler/16-browser-render.md",
  "q": "商品数据存在于哪里？requests 拿 HTML 能拿到吗？",
  "a": "数据存在于**接口 JSON**（XHR/fetch 响应）；HTML 只有 `<div id=\"root\">` 挂载点；requests 不执行 JS → 拿不到（除非数据内联进 HTML）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 商品数据存在于哪里？requests 拿 HTML 能拿到吗？

**A**: 数据存在于**接口 JSON**（XHR/fetch 响应）；HTML 只有 `<div id="root">` 挂载点；requests 不执行 JS → 拿不到（除非数据内联进 HTML）
