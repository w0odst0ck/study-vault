---
{
  "id": "crawler-cookie失效至少有-122",
  "domain": "crawler",
  "source": "knowledge/crawler/17-anti-crawl-principles.md",
  "q": "cookie 失效至少有 5 种原因，分别是什么？判断场景：cookie 的 Expires 明明没过期，但长时间没活动后请求突然跳登录页——这是哪种失效？",
  "a": "- ① 过期（Expires/Max-Age 到点）② 服务端注销（踢下线）③ 会话滑动过期（idle 超时作废——看着没过期其实已死）④ 风控吊销 ⑤ 环境绑定变化（UA/IP/设备变更）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: cookie 失效至少有 5 种原因，分别是什么？判断场景：cookie 的 Expires 明明没过期，但长时间没活动后请求突然跳登录页——这是哪种失效？

**A**: - ① 过期（Expires/Max-Age 到点）② 服务端注销（踢下线）③ 会话滑动过期（idle 超时作废——看着没过期其实已死）④ 风控吊销 ⑤ 环境绑定变化（UA/IP/设备变更）
