---
{
  "id": "dsa-Python回溯用列表-043",
  "domain": "dsa",
  "source": "knowledge/dsa/06-backtracking.md",
  "q": "Python 回溯用列表传递 path，C++ 一般用什么？",
  "a": "C++ 用 `vector<int>& path` 传引用 + 回溯 `pop_back()`；Python 默认传引用但记录时要 `path[:]` 拷贝副本",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: Python 回溯用列表传递 path，C++ 一般用什么？

**A**: C++ 用 `vector<int>& path` 传引用 + 回溯 `pop_back()`；Python 默认传引用但记录时要 `path[:]` 拷贝副本
