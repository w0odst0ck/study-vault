---
{
  "id": "dsa-C的vector-044",
  "domain": "dsa",
  "source": "knowledge/dsa/07-dynamic-programming.md",
  "q": "C++ 的 vector 二维数组定义和 Python 列表推导式有什么差异？",
  "a": "Python `[[0]*n for _ in range(m)]`；C++ `vector<vector<int>> dp(m, vector<int>(n, 0))`。注意 Python 不能用 `[[0]*n]*m` 因为会共享引用",
  "created": "2026-07-22",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-22",
  "reviews": 0
}
---

**Q**: C++ 的 vector 二维数组定义和 Python 列表推导式有什么差异？

**A**: Python `[[0]*n for _ in range(m)]`；C++ `vector<vector<int>> dp(m, vector<int>(n, 0))`。注意 Python 不能用 `[[0]*n]*m` 因为会共享引用
