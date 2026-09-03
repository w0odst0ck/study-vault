---
{
  "id": "crawler-工厂监控脚本被Clou-118",
  "domain": "crawler",
  "source": "knowledge/crawler/17-anti-crawl-principles.md",
  "q": "工厂监控脚本被 Cloudflare 质询页挡了（403），requests 过不去。按什么顺序处理？",
  "a": "- ① 鉴别：先确认是否真质询（403/503 + challenge 特征页）；也可能是 UA 被拦/速率限制 = 请求层\n  - ② 请求层问题先降频/换 UA（便宜步骤先走，别急着上最贵的）\n  - ③ 真质询才上 PW（真实指纹）/ curl_cffi\n  - ④ 改道兜底：仍不行 → 打接口 / 其他数据源 / 官方 API\n  - 记忆点：**鉴别 → 分层 → 改道**",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 工厂监控脚本被 Cloudflare 质询页挡了（403），requests 过不去。按什么顺序处理？

**A**: - ① 鉴别：先确认是否真质询（403/503 + challenge 特征页）；也可能是 UA 被拦/速率限制 = 请求层
  - ② 请求层问题先降频/换 UA（便宜步骤先走，别急着上最贵的）
  - ③ 真质询才上 PW（真实指纹）/ curl_cffi
  - ④ 改道兜底：仍不行 → 打接口 / 其他数据源 / 官方 API
  - 记忆点：**鉴别 → 分层 → 改道**
