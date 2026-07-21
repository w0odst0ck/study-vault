---
{
  "id": "programming-整合时gitigno-009",
  "domain": "programming",
  "source": "knowledge/programming/03-project-integration-strategy.md",
  "q": "整合时 .gitignore 的维护原则是什么？",
  "a": "宁多勿漏——覆盖所有子项目的敏感数据模式（cookies/*.db/*.xlsx/cache/.env 等），敏感数据一概不入库。",
  "created": "2026-07-21",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-21",
  "reviews": 0
}
---

**Q**: 整合时 .gitignore 的维护原则是什么？

**A**: 宁多勿漏——覆盖所有子项目的敏感数据模式（cookies/*.db/*.xlsx/cache/.env 等），敏感数据一概不入库。
