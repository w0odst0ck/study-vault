---
{
  "id": "crawler-LLM调用失败时的安全-018",
  "domain": "crawler",
  "source": "knowledge/crawler/05-multi-source-intel-collection.md",
  "q": "LLM 调用失败时的安全策略是什么？",
  "a": "LLM 默认禁用（`--llm` 按需启用），调用失败返回 `None` 不 `sys.exit(1)`，规则分类保底。",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: LLM 调用失败时的安全策略是什么？

**A**: LLM 默认禁用（`--llm` 按需启用），调用失败返回 `None` 不 `sys.exit(1)`，规则分类保底。
