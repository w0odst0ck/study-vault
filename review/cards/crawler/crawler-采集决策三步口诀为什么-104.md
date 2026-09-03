---
{
  "id": "crawler-采集决策三步口诀为什么-104",
  "domain": "crawler",
  "source": "knowledge/crawler/16-browser-render.md",
  "q": "采集决策三步口诀？为什么接口优先？为什么不用固定 sleep？懒加载页面怎么抓全、怎么知道到底？",
  "a": "- 口诀：**先 HTML → 再接口 → 最后浏览器**；接口优先 = 稳定可靠 + 浏览器慢/被识别\n  - sleep = **猜时间**（固定时长，网络波动下白等/抓空）；用 wait_for_selector / wait_for_load_state('networkidle') 等\"产物出现\"\n  - 懒加载：**滚动 → 等新元素 → 抓取 → 循环**；结束条件 = 滚动后新元素不再出现（或\"没有更多\"标记）→ 停止",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 采集决策三步口诀？为什么接口优先？为什么不用固定 sleep？懒加载页面怎么抓全、怎么知道到底？

**A**: - 口诀：**先 HTML → 再接口 → 最后浏览器**；接口优先 = 稳定可靠 + 浏览器慢/被识别
  - sleep = **猜时间**（固定时长，网络波动下白等/抓空）；用 wait_for_selector / wait_for_load_state('networkidle') 等"产物出现"
  - 懒加载：**滚动 → 等新元素 → 抓取 → 循环**；结束条件 = 滚动后新元素不再出现（或"没有更多"标记）→ 停止
