---
{
  "id": "crawler-怎么选中acla-090",
  "domain": "crawler",
  "source": "knowledge/crawler/15-html-parsing.md",
  "q": "怎么选中 `<a class=\"offer-title\" href=\"/offer/12345\">`？`.offer-price-row, .price, [class*=\"price\"]` 链怎么工作？",
  "a": "- 组合语法：**标签.类名 + [属性*=值]** → `a.offer-title[href*=\"/offer/\"]`；类名从真实 HTML 抄，**选择器只描述结构，字段映射是提取之后的事**\n  - `.xxx class` 语法不存在（class 是属性名不是标签）\n  - 多选器链 = 备选地址列表（逗号=或），精确优先、模糊兜底；`[class*=\"title\"]` 模糊 vs `.title` 精确；hash 类名不能写死（每次构建会变）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 怎么选中 `<a class="offer-title" href="/offer/12345">`？`.offer-price-row, .price, [class*="price"]` 链怎么工作？

**A**: - 组合语法：**标签.类名 + [属性*=值]** → `a.offer-title[href*="/offer/"]`；类名从真实 HTML 抄，**选择器只描述结构，字段映射是提取之后的事**
  - `.xxx class` 语法不存在（class 是属性名不是标签）
  - 多选器链 = 备选地址列表（逗号=或），精确优先、模糊兜底；`[class*="title"]` 模糊 vs `.title` 精确；hash 类名不能写死（每次构建会变）
