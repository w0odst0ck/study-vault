---
{
  "id": "crawler-大规模批量采集时如何处理-049",
  "domain": "crawler",
  "source": "knowledge/crawler/11-vendor-crawl-evaluation.md",
  "q": "大规模批量采集时如何处理 stdout 缓冲问题？",
  "a": "使用 `python -u` 运行脚本（-u 强制 stdout/stderr 无缓冲），或用交互式 Python 脚本模式（直接调用内部函数）替代 CLI 运行，实现实时进度输出和动态参数调整。",
  "created": "2026-07-25",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-25",
  "reviews": 0
}
---

**Q**: 大规模批量采集时如何处理 stdout 缓冲问题？

**A**: 使用 `python -u` 运行脚本（-u 强制 stdout/stderr 无缓冲），或用交互式 Python 脚本模式（直接调用内部函数）替代 CLI 运行，实现实时进度输出和动态参数调整。
