---
{
  "id": "crawler-chromiumla-021",
  "domain": "crawler",
  "source": "knowledge/crawler/06-1688-factory-monitor.md",
  "q": "`chromium.launch()` 之后缺少什么关键步骤？",
  "a": "不会自动创建浏览器上下文，需显式调用 `browser.new_context()` 再 `context.new_page()`。",
  "created": "2026-07-21",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-21",
  "reviews": 0
}
---

**Q**: `chromium.launch()` 之后缺少什么关键步骤？

**A**: 不会自动创建浏览器上下文，需显式调用 `browser.new_context()` 再 `context.new_page()`。
