---
{
  "id": "crawler-场景题requests-110",
  "domain": "crawler",
  "source": "knowledge/crawler/17-anti-crawl-principles.md",
  "q": "场景题：requests 抓 1688，50 页后 429，重试几次后弹验证码。哪两层在拦？怎么应对？",
  "a": "- 429=请求层 / 验证码=内容层\n  - 应对链：**立即停手（重试=升级导火索，脚本才会死磕）** → 看 Retry-After → 降频加随机间隔 → 换 IP/补 UA → 仍不行才上 PW；退让才能让风控降级",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 场景题：requests 抓 1688，50 页后 429，重试几次后弹验证码。哪两层在拦？怎么应对？

**A**: - 429=请求层 / 验证码=内容层
  - 应对链：**立即停手（重试=升级导火索，脚本才会死磕）** → 看 Retry-After → 降频加随机间隔 → 换 IP/补 UA → 仍不行才上 PW；退让才能让风控降级
