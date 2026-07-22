---
{
  "id": "dsa-链表操作中dangli-068",
  "domain": "dsa",
  "source": "knowledge/dsa/13-dsa-solve-methodology.md",
  "q": "链表操作中 dangling pointer 怎么防？",
  "a": "用 dummy 节点保底，每次操作后推进指针（`cur = cur.next`），提前想好循环终止条件",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: 链表操作中 dangling pointer 怎么防？

**A**: 用 dummy 节点保底，每次操作后推进指针（`cur = cur.next`），提前想好循环终止条件
