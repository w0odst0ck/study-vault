---
{
  "id": "crawler-Playwright浏-009",
  "domain": "crawler",
  "source": "knowledge/crawler/02-playwright-browser-manager.md",
  "q": "Playwright 浏览器管理器的三种搜索策略模式是什么？",
  "a": "渲染模式（直接导航取 HTML，适用 SSR 页面）、API 拦截模式（拦截 XHR/Fetch 得 JSON，适用 SPA 页面）、主页交互模式（打开首页绕过 CF -> 输入搜索框 -> 点击按钮，适用首页无保护的平台）。",
  "created": "2026-07-22",
  "last_reviewed": "2026-07-24",
  "interval": 1,
  "ease": 2.36,
  "next_review": "2026-07-25",
  "reviews": 2
}
---

**Q**: Playwright 浏览器管理器的三种搜索策略模式是什么？

**A**: 渲染模式（直接导航取 HTML，适用 SSR 页面）、API 拦截模式（拦截 XHR/Fetch 得 JSON，适用 SPA 页面）、主页交互模式（打开首页绕过 CF -> 输入搜索框 -> 点击按钮，适用首页无保护的平台）。
