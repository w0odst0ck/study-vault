---
{
  "id": "crawler-requests200-094",
  "domain": "crawler",
  "source": "knowledge/crawler/15-html-parsing.md",
  "q": "requests 200 + HTML 完整但提取不到商品，两种原因？排查第一步看什么？请求层 vs 解析层怎么分？",
  "a": "- **排查第一步 = 看响应体原文归类**（requests 没有 DOM！）：登录页/错误页 → 请求层；空壳 JS 未跑 / script JSON 未抠（__NEXT_DATA__）/ 懒加载未触发 → 解析层\n  - 分层：请求层 = 页面不对（状态码/重定向/登录页）；解析层 = 页面对但没数据（空壳/JSON/懒加载）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: requests 200 + HTML 完整但提取不到商品，两种原因？排查第一步看什么？请求层 vs 解析层怎么分？

**A**: - **排查第一步 = 看响应体原文归类**（requests 没有 DOM！）：登录页/错误页 → 请求层；空壳 JS 未跑 / script JSON 未抠（__NEXT_DATA__）/ 懒加载未触发 → 解析层
  - 分层：请求层 = 页面不对（状态码/重定向/登录页）；解析层 = 页面对但没数据（空壳/JSON/懒加载）
