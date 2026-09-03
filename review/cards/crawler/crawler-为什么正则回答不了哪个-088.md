---
{
  "id": "crawler-为什么正则回答不了哪个-088",
  "domain": "crawler",
  "source": "knowledge/crawler/15-html-parsing.md",
  "q": "为什么正则回答不了\"哪个 p 在 div 里\"这种层级问题？",
  "a": "匹配层级关系需要记忆**嵌套深度（栈）**；正则 = 有限状态自动机，**无栈** → 理论不可表达；树结构解析必须交给 DOM 解析器",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 为什么正则回答不了"哪个 p 在 div 里"这种层级问题？

**A**: 匹配层级关系需要记忆**嵌套深度（栈）**；正则 = 有限状态自动机，**无栈** → 理论不可表达；树结构解析必须交给 DOM 解析器
