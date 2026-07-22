---
{
  "id": "dsa-BFS层序遍历如何区分-014",
  "domain": "dsa",
  "source": "knowledge/dsa/08-binary-tree.md",
  "q": "BFS 层序遍历如何区分每一层？",
  "a": "每层开始时用 `len(q)` 固定当前层大小，循环该次数后开始下一层",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: BFS 层序遍历如何区分每一层？

**A**: 每层开始时用 `len(q)` 固定当前层大小，循环该次数后开始下一层
