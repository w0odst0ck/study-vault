---
{
  "id": "dsa-反转链表的迭代法pre-016",
  "domain": "dsa",
  "source": "knowledge/dsa/02-linked-list.md",
  "q": "反转链表的迭代法（prev/cur/nxt）是什么？",
  "a": "prev 指向已反转部分头，cur 指向当前待反转节点，nxt 保存后续。每次 cur.next = prev 后整体前移。",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: 反转链表的迭代法（prev/cur/nxt）是什么？

**A**: prev 指向已反转部分头，cur 指向当前待反转节点，nxt 保存后续。每次 cur.next = prev 后整体前移。
