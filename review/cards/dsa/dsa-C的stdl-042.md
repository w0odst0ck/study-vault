---
{
  "id": "dsa-C的stdl-042",
  "domain": "dsa",
  "source": "knowledge/dsa/05-binary-search.md",
  "q": "C++ 的 std::lower_bound 和 Python bisect.bisect_left 对应什么？",
  "a": "都对应「第一个 >= target」的位置。C++ 返回迭代器，Python 返回索引。Python 标准库 `bisect` 模块二分实现比手写更稳",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: C++ 的 std::lower_bound 和 Python bisect.bisect_left 对应什么？

**A**: 都对应「第一个 >= target」的位置。C++ 返回迭代器，Python 返回索引。Python 标准库 `bisect` 模块二分实现比手写更稳
