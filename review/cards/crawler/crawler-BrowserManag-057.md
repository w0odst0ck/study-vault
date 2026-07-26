---
{
  "id": "crawler-BrowserManag-057",
  "domain": "crawler",
  "source": "knowledge/crawler/13-project-streamlining-strategy.md",
  "q": "BrowserManager 取代 setup_session 函数解决了什么问题？",
  "a": "旧函数式散落难以复用，且 check_state_fresh 存在死代码（早期 return 跳过 Cookie 过期检查）。新方案用面向对象封装浏览器生命周期，创建 _check_session() 方法自动检测 Cookie 是否过期。",
  "created": "2026-07-25",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-25",
  "reviews": 0
}
---

**Q**: BrowserManager 取代 setup_session 函数解决了什么问题？

**A**: 旧函数式散落难以复用，且 check_state_fresh 存在死代码（早期 return 跳过 Cookie 过期检查）。新方案用面向对象封装浏览器生命周期，创建 _check_session() 方法自动检测 Cookie 是否过期。
