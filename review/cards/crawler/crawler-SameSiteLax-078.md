---
{
  "id": "crawler-SameSiteLax-078",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "SameSite=Lax 对爬虫意味着什么？坑在哪？",
  "a": "- SameSite=Lax = 跨站请求不发 cookie（顶级导航 GET 例外）\n  - 对爬虫：requests/httpx 不执行浏览器同源策略 → 基本无感；**坑在 Playwright**（跨站子资源请求被拦 cookie）+ 重定向链跨域作用域丢失",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: SameSite=Lax 对爬虫意味着什么？坑在哪？

**A**: - SameSite=Lax = 跨站请求不发 cookie（顶级导航 GET 例外）
  - 对爬虫：requests/httpx 不执行浏览器同源策略 → 基本无感；**坑在 Playwright**（跨站子资源请求被拦 cookie）+ 重定向链跨域作用域丢失
