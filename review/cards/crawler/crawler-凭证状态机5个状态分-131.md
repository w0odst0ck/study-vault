---
{
  "id": "crawler-凭证状态机5个状态分-131",
  "domain": "crawler",
  "source": "knowledge/crawler/19-credential-management.md",
  "q": "凭证状态机 5 个状态分别是什么？为什么不能用\"活/死\"布尔值代替？",
  "a": "- 5 态：ACTIVE 有效 → SUSPECT 濒死 → DEAD 失效 → RENEWING 重登中 → ABANDON 放弃；ACTIVE↔SUSPECT 由连续 N 次探活结果驱动\n  - 布尔只有\"活/死\"，丢**中间态 SUSPECT**——它最值钱：濒死就降频半速（提前止损），避免\"突然死\"的整批损失；每个状态绑定\"该做什么\"（动作），而不是\"死了再说\"",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 凭证状态机 5 个状态分别是什么？为什么不能用"活/死"布尔值代替？

**A**: - 5 态：ACTIVE 有效 → SUSPECT 濒死 → DEAD 失效 → RENEWING 重登中 → ABANDON 放弃；ACTIVE↔SUSPECT 由连续 N 次探活结果驱动
  - 布尔只有"活/死"，丢**中间态 SUSPECT**——它最值钱：濒死就降频半速（提前止损），避免"突然死"的整批损失；每个状态绑定"该做什么"（动作），而不是"死了再说"
