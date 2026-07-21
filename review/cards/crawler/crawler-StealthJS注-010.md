---
{
  "id": "crawler-StealthJS注-010",
  "domain": "crawler",
  "source": "knowledge/crawler/02-playwright-browser-manager.md",
  "q": "Stealth JS 注入的核心原理是什么？",
  "a": "修改 `navigator.webdriver=false`、模拟 `window.chrome` 对象、添加 plugins、覆盖 permissions query、修改 languages/hardwareConcurrency/deviceMemory 等指纹参数。",
  "created": "2026-07-21",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-21",
  "reviews": 0
}
---

**Q**: Stealth JS 注入的核心原理是什么？

**A**: 修改 `navigator.webdriver=false`、模拟 `window.chrome` 对象、添加 plugins、覆盖 permissions query、修改 languages/hardwareConcurrency/deviceMemory 等指纹参数。
