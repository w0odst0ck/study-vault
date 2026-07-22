---
{
  "id": "dsa-验证BST为什么不能-015",
  "domain": "dsa",
  "source": "knowledge/dsa/08-binary-tree.md",
  "q": "验证 BST 为什么不能只检查左 < 根 < 右？",
  "a": "需要全局范围约束（min/max），仅检查局部会漏掉深层违规（如右子树中出现比根小的值）",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: 验证 BST 为什么不能只检查左 < 根 < 右？

**A**: 需要全局范围约束（min/max），仅检查局部会漏掉深层违规（如右子树中出现比根小的值）
