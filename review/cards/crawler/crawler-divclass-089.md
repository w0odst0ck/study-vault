---
{
  "id": "crawler-divclass-089",
  "domain": "crawler",
  "source": "knowledge/crawler/15-html-parsing.md",
  "q": "`<div class=abc>你好</div>` 浏览器会解析失败扔掉吗？",
  "a": "- **不会**——属性无引号本就是合法 HTML 语法（WHATWG 树构建容错），照常构建 DOM\n  - 容错针对未闭合/错嵌套（如 `<p>a<p>b`），是解析器**规范行为**，不是\"正则兜底\"（浏览器解析与正则无关）",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: `<div class=abc>你好</div>` 浏览器会解析失败扔掉吗？

**A**: - **不会**——属性无引号本就是合法 HTML 语法（WHATWG 树构建容错），照常构建 DOM
  - 容错针对未闭合/错嵌套（如 `<p>a<p>b`），是解析器**规范行为**，不是"正则兜底"（浏览器解析与正则无关）
