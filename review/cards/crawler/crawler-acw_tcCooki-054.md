---
{
  "id": "crawler-acw_tcCooki-054",
  "domain": "crawler",
  "source": "knowledge/crawler/12-zkh-waf-bypass.md",
  "q": "acw_tc Cookie 的提取和使用策略是什么？",
  "a": "从 Windows Chrome DevTools → Application → Cookies 手动提取，保存到 cookies/cookies_zkh.json。有效期为约 7 天，过期需重新提取。启动时通过 load_cookies() 加载到浏览器上下文。",
  "created": "2026-07-25",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-25",
  "reviews": 0
}
---

**Q**: acw_tc Cookie 的提取和使用策略是什么？

**A**: 从 Windows Chrome DevTools → Application → Cookies 手动提取，保存到 cookies/cookies_zkh.json。有效期为约 7 天，过期需重新提取。启动时通过 load_cookies() 加载到浏览器上下文。
