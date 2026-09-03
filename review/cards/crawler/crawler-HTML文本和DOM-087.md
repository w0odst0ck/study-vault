---
{
  "id": "crawler-HTML文本和DOM-087",
  "domain": "crawler",
  "source": "knowledge/crawler/15-html-parsing.md",
  "q": "HTML 文本和 DOM 树分别是什么？一个文档几棵树？画 `<div><p>苹果</p><p>香蕉</p></div>` 的 DOM 树，几个节点？",
  "a": "- HTML 文本 = 一维字符流（raw）；DOM 树 = 解析后的树形结构，**一个文档一棵**（根 = document；iframe 是多个文档的特例）\n  - **文本也是节点**（TextNode）——树里没有裸字符串；例图 5 节点 = 3 元素（div/p/p）+ 2 文本（苹果/香蕉）；两个 p 是兄弟，共同挂 div 下",
  "created": "2026-09-03",
  "last_reviewed": null,
  "interval": 0,
  "ease": 2.5,
  "next_review": "2026-09-03",
  "reviews": 0
}
---

**Q**: HTML 文本和 DOM 树分别是什么？一个文档几棵树？画 `<div><p>苹果</p><p>香蕉</p></div>` 的 DOM 树，几个节点？

**A**: - HTML 文本 = 一维字符流（raw）；DOM 树 = 解析后的树形结构，**一个文档一棵**（根 = document；iframe 是多个文档的特例）
  - **文本也是节点**（TextNode）——树里没有裸字符串；例图 5 节点 = 3 元素（div/p/p）+ 2 文本（苹果/香蕉）；两个 p 是兄弟，共同挂 div 下
