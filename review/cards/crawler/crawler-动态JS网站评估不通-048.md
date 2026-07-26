---
{
  "id": "crawler-动态JS网站评估不通-048",
  "domain": "crawler",
  "source": "knowledge/crawler/11-vendor-crawl-evaluation.md",
  "q": "动态 JS 网站评估不通过时的降级策略是什么？",
  "a": "尝试 playwright → 失败则降级为 catalog：只保存页面的 HTML/CSS 资源快照，不做深度详情解析。典型例子：欧普照明（JS SPA 无独立 URL）、雷士照明（无案例详情页）。",
  "created": "2026-07-25",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-25",
  "reviews": 0
}
---

**Q**: 动态 JS 网站评估不通过时的降级策略是什么？

**A**: 尝试 playwright → 失败则降级为 catalog：只保存页面的 HTML/CSS 资源快照，不做深度详情解析。典型例子：欧普照明（JS SPA 无独立 URL）、雷士照明（无案例详情页）。
