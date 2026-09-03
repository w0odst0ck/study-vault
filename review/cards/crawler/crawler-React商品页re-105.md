---
{
  "id": "crawler-React商品页re-105",
  "domain": "crawler",
  "source": "knowledge/crawler/16-browser-render.md",
  "q": "React 商品页 requests 拿到空壳，完整采集流程怎么走？",
  "a": "看响应体 → 数据不在 → 找 XHR/fetch 接口（DevTools Network）→ JSON 直拿 → 接口有防护 → Playwright：等 wait_for_selector/networkidle，page.evaluate 取 DOM 或 page.route 拦截响应 JSON，懒加载滚动循环",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: React 商品页 requests 拿到空壳，完整采集流程怎么走？

**A**: 看响应体 → 数据不在 → 找 XHR/fetch 接口（DevTools Network）→ JSON 直拿 → 接口有防护 → Playwright：等 wait_for_selector/networkidle，page.evaluate 取 DOM 或 page.route 拦截响应 JSON，懒加载滚动循环
