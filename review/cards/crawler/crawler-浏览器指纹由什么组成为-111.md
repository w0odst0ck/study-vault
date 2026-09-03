---
{
  "id": "crawler-浏览器指纹由什么组成为-111",
  "domain": "crawler",
  "source": "knowledge/crawler/17-anti-crawl-principles.md",
  "q": "浏览器指纹由什么组成？为什么能唯一标识？",
  "a": "- 组成四类：Canvas / WebGL / 字体列表 / 系统参数\n  - 唯一性：信息极其丰富、熵高难复制\n  - **一致性**：UA 与所有特征互相匹配（时区/语言/屏幕与 UA 一致），风控专抓不一致",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: 浏览器指纹由什么组成？为什么能唯一标识？

**A**: - 组成四类：Canvas / WebGL / 字体列表 / 系统参数
  - 唯一性：信息极其丰富、熵高难复制
  - **一致性**：UA 与所有特征互相匹配（时区/语言/屏幕与 UA 一致），风控专抓不一致
