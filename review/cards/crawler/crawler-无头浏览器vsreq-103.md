---
{
  "id": "crawler-无头浏览器vsreq-103",
  "domain": "crawler",
  "source": "knowledge/crawler/16-browser-render.md",
  "q": "无头浏览器 vs requests 本质差别？CDP 是什么？Playwright 通过它干什么？为什么拦截网络请求拿 JSON 更好？",
  "a": "- 无头浏览器 = 完整浏览器（执行 JS + 全渲染管线）；requests 只读 HTML（第①步产物）\n  - **CDP = Chrome 调试协议**（DevTools 同款通信方式，DevTools 是工具不是协议）；Playwright 启动真 Chromium → CDP 连接 → 操作翻译成 CDP 命令**驱动**浏览器（不是\"模拟\"——本质是真 Chrome）\n  - 拦截 JSON 三优势：① **数据源头**（结构化 JSON，不用从 DOM 抠）② **稳**（不受懒加载/重排/元素变动影响）③ 快（少渲染步骤）；找到接口 requests 都能直接打",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 无头浏览器 vs requests 本质差别？CDP 是什么？Playwright 通过它干什么？为什么拦截网络请求拿 JSON 更好？

**A**: - 无头浏览器 = 完整浏览器（执行 JS + 全渲染管线）；requests 只读 HTML（第①步产物）
  - **CDP = Chrome 调试协议**（DevTools 同款通信方式，DevTools 是工具不是协议）；Playwright 启动真 Chromium → CDP 连接 → 操作翻译成 CDP 命令**驱动**浏览器（不是"模拟"——本质是真 Chrome）
  - 拦截 JSON 三优势：① **数据源头**（结构化 JSON，不用从 DOM 抠）② **稳**（不受懒加载/重排/元素变动影响）③ 快（少渲染步骤）；找到接口 requests 都能直接打
