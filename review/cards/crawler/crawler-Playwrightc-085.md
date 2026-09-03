---
{
  "id": "crawler-Playwrightc-085",
  "domain": "crawler",
  "source": "knowledge/crawler/14-http-protocol.md",
  "q": "Playwright cookie 持久化闭环缺哪步？探测接口怎么选？探测失败自动重登还是手动？",
  "a": "- 5 步闭环：登录 → 持久化存盘 → 加载还原 → **探测验证** → 失效重登（factory-monitor 只有前 3 步）\n  - 验证不能只看状态码：**阴险形态 200+登录页 HTML**（码和内容分开看）\n  - 探测接口判据 = **露馅性**（没登录就露馅）；判定三板斧：URL 跳 login=失效 / 200 但登录框特征=失效 / 正常列表=有效\n  - 探测失败：先重试 1-2 次（指数退避）→ 仍失败=确认失效 → **不能自动重登**（卡验证码+触发风控）→ 标记 COOKIE_EXPIRED + 通知人工（有头）→ save_cookies 覆盖",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: Playwright cookie 持久化闭环缺哪步？探测接口怎么选？探测失败自动重登还是手动？

**A**: - 5 步闭环：登录 → 持久化存盘 → 加载还原 → **探测验证** → 失效重登（factory-monitor 只有前 3 步）
  - 验证不能只看状态码：**阴险形态 200+登录页 HTML**（码和内容分开看）
  - 探测接口判据 = **露馅性**（没登录就露馅）；判定三板斧：URL 跳 login=失效 / 200 但登录框特征=失效 / 正常列表=有效
  - 探测失败：先重试 1-2 次（指数退避）→ 仍失败=确认失效 → **不能自动重登**（卡验证码+触发风控）→ 标记 COOKIE_EXPIRED + 通知人工（有头）→ save_cookies 覆盖
