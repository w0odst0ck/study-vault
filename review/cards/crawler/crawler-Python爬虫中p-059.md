---
{
  "id": "crawler-Python爬虫中p-059",
  "domain": "crawler",
  "source": "knowledge/crawler/13-project-streamlining-strategy.md",
  "q": "Python 爬虫中 page.keyboard.select_all() 的错误原因和正确写法？",
  "a": "Playwright 没有 `select_all()` 方法，应使用 `page.keyboard.press('Control+a')`（Windows）或 `page.keyboard.press('Meta+a')`（macOS）。",
  "created": "2026-07-25",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-25",
  "reviews": 0
}
---

**Q**: Python 爬虫中 page.keyboard.select_all() 的错误原因和正确写法？

**A**: Playwright 没有 `select_all()` 方法，应使用 `page.keyboard.press('Control+a')`（Windows）或 `page.keyboard.press('Meta+a')`（macOS）。
