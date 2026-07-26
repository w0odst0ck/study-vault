---
{
  "id": "crawler-clean_text全-042",
  "domain": "crawler",
  "source": "knowledge/crawler/10-index-driven-material-mgmt.md",
  "q": "clean_text 全量清洗的执行流程和典型规模？",
  "a": "运行 `python3 clean_text.py --all`，283 文件输入 → 277 OK，6 跳过。关键处理包括：移除 HTML 导航/页脚区块（正则匹配）、保留图片外链、html2text 转换（Python 3.13 需额外安装）。",
  "created": "2026-07-25",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-07-25",
  "reviews": 0
}
---

**Q**: clean_text 全量清洗的执行流程和典型规模？

**A**: 运行 `python3 clean_text.py --all`，283 文件输入 → 277 OK，6 跳过。关键处理包括：移除 HTML 导航/页脚区块（正则匹配）、保留图片外链、html2text 转换（Python 3.13 需额外安装）。
