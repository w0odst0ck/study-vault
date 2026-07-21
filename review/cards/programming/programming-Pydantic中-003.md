---
{
  "id": "programming-Pydantic中-003",
  "domain": "programming",
  "source": "knowledge/programming/01-pydantic-v2-model-design.md",
  "q": "Pydantic 中 `Literal` 类型相比枚举有什么优势？",
  "a": "轻量（无需定义类）、天然可序列化为 JSON、API 友好，适合有限状态如 `status: Literal[\"unreviewed\", \"reviewed\", \"archived\"]`。",
  "created": "2026-07-18",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-18",
  "reviews": 0
}
---

**Q**: Pydantic 中 `Literal` 类型相比枚举有什么优势？

**A**: 轻量（无需定义类）、天然可序列化为 JSON、API 友好，适合有限状态如 `status: Literal["unreviewed", "reviewed", "archived"]`。
