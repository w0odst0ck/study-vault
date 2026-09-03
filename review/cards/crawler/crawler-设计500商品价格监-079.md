---
{
  "id": "crawler-设计500商品价格监-079",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "设计 500 商品价格监控轮询器：用什么客户端？状态码怎么处理？ETag 怎么用？限速怎么做？",
  "a": "- 客户端：requests/httpx + Session（连接复用+cookie 仓库）；Playwright 留给重反爬站点（500 商品开浏览器太重）\n  - 状态码：200 解析 / 304 跳过解析用旧快照 / 301-308 跟随限跳数 / 403 换身份 / 404 标记下架 / 429 读 Retry-After / 5xx 指数退避+抖动\n  - **ETag 条件请求 = monitor 命根子**（存 products 表 etag 列）\n  - 限速：每商品时间戳 + 自适应（429 后按 Retry-After 拉长）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 设计 500 商品价格监控轮询器：用什么客户端？状态码怎么处理？ETag 怎么用？限速怎么做？

**A**: - 客户端：requests/httpx + Session（连接复用+cookie 仓库）；Playwright 留给重反爬站点（500 商品开浏览器太重）
  - 状态码：200 解析 / 304 跳过解析用旧快照 / 301-308 跟随限跳数 / 403 换身份 / 404 标记下架 / 429 读 Retry-After / 5xx 指数退避+抖动
  - **ETag 条件请求 = monitor 命根子**（存 products 表 etag 列）
  - 限速：每商品时间戳 + 自适应（429 后按 Retry-After 拉长）
