---
{
  "id": "crawler-StealthJS注-010",
  "domain": "crawler",
  "source": "knowledge/crawler/02-playwright-browser-manager.md",
  "q": "Stealth JS 注入的核心原理是什么？",
  "a": "修改 `navigator.webdriver=false`、模拟 `window.chrome` 对象、添加 plugins、覆盖 permissions query、修改 languages/hardwareConcurrency/deviceMemory 等指纹参数。",
  "created": "2026-07-22",
  "last_reviewed": "2026-07-22",
  "interval": 1,
  "ease": 2.36,
  "next_review": "2026-07-23",
  "reviews": 1
}
---

**Q**: Stealth JS 注入的核心原理是什么？

**A**: 修改 `navigator.webdriver=false`、模拟 `window.chrome` 对象、添加 plugins、覆盖 permissions query、修改 languages/hardwareConcurrency/deviceMemory 等指纹参数。
