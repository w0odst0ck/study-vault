---
{
  "id": "crawler-LLM调用失败时的安全-018",
  "domain": "crawler",
  "source": "knowledge/crawler/05-multi-source-intel-collection.md",
  "q": "LLM 调用失败时的安全策略是什么？",
  "a": "LLM 默认禁用（`--llm` 按需启用），调用失败返回 `None` 不 `sys.exit(1)`，规则分类保底。",
  "created": "2026-07-22",
  "last_reviewed": "2026-07-22",
  "interval": 1,
  "ease": 2.36,
  "next_review": "2026-07-23",
  "reviews": 1
}
---

**Q**: LLM 调用失败时的安全策略是什么？

**A**: LLM 默认禁用（`--llm` 按需启用），调用失败返回 `None` 不 `sys.exit(1)`，规则分类保底。
