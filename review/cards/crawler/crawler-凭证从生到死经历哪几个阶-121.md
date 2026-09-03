---
{
  "id": "crawler-凭证从生到死经历哪几个阶-121",
  "domain": "crawler",
  "source": "knowledge/crawler/17-anti-crawl-principles.md",
  "q": "凭证从生到死经历哪几个阶段？RFC 6265 的哪四个要素决定\"什么时候回传、什么时候失效\"？",
  "a": "- 四阶段闭环：颁发 → 存储 → 使用 → 失效 → 刷新重获\n  - RFC 6265 四要素（决定何时回传/何时失效）：Domain / Path / Secure / 过期\n  - 类比：凭证=公司工牌（有有效期/会吊销/重办走流程/多张卡=轮换池）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 凭证从生到死经历哪几个阶段？RFC 6265 的哪四个要素决定"什么时候回传、什么时候失效"？

**A**: - 四阶段闭环：颁发 → 存储 → 使用 → 失效 → 刷新重获
  - RFC 6265 四要素（决定何时回传/何时失效）：Domain / Path / Secure / 过期
  - 类比：凭证=公司工牌（有有效期/会吊销/重办走流程/多张卡=轮换池）
