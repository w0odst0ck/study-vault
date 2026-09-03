---
{
  "id": "crawler-WAF和四层检测体系是-117",
  "domain": "crawler",
  "source": "knowledge/crawler/17-anti-crawl-principles.md",
  "q": "WAF 和四层检测体系是什么关系？Cloudflare 质询页算哪一层？为什么 requests 过不去？",
  "a": "- WAF 不是独立层：横跨请求层（速率/UA 规则）+ 内容层（JS 质询/验证码）\n  - **JS 质询 = 内容层主动挑战（\"考\"），非特征层**：特征层是\"看\"（被动观察指纹），内容层是\"考\"（要执行 JS 算 token）\n  - requests 不执行 JS → 拿不到 token → 永远 403",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: WAF 和四层检测体系是什么关系？Cloudflare 质询页算哪一层？为什么 requests 过不去？

**A**: - WAF 不是独立层：横跨请求层（速率/UA 规则）+ 内容层（JS 质询/验证码）
  - **JS 质询 = 内容层主动挑战（"考"），非特征层**：特征层是"看"（被动观察指纹），内容层是"考"（要执行 JS 算 token）
  - requests 不执行 JS → 拿不到 token → 永远 403
