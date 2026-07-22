---
{
  "id": "crawler-跨平台Context-011",
  "domain": "crawler",
  "source": "knowledge/crawler/02-playwright-browser-manager.md",
  "q": "跨平台 Context 隔离的设计目的是什么？",
  "a": "每个平台独立 browser context，通过 `switch_platform()` 切换，避免 Cookie/Storage 串用导致跨平台风控。",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: 跨平台 Context 隔离的设计目的是什么？

**A**: 每个平台独立 browser context，通过 `switch_platform()` 切换，避免 Cookie/Storage 串用导致跨平台风控。
