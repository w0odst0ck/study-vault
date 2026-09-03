---
{
  "id": "crawler-React页面查看源代-093",
  "domain": "crawler",
  "source": "knowledge/crawler/15-html-parsing.md",
  "q": "React 页面查看源代码为什么看不到商品数据？PH 油猴为什么能拿到渲染后 DOM？",
  "a": "- CSR 响应体 = **空壳 + JS bundle**，数据根本不在响应体里（不是\"数据等 JS 跑\"）；浏览器执行 JS 后才请求 API、生成 DOM\n  - 油猴跑在页面内（与页面 JS 共享 DOM）→ 渲染完成 → `document.documentElement.outerHTML` 序列化；requests 只拿响应体（JS 未执行）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: React 页面查看源代码为什么看不到商品数据？PH 油猴为什么能拿到渲染后 DOM？

**A**: - CSR 响应体 = **空壳 + JS bundle**，数据根本不在响应体里（不是"数据等 JS 跑"）；浏览器执行 JS 后才请求 API、生成 DOM
  - 油猴跑在页面内（与页面 JS 共享 DOM）→ 渲染完成 → `document.documentElement.outerHTML` 序列化；requests 只拿响应体（JS 未执行）
