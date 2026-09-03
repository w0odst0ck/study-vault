# DOM（Document Object Model）

HTML 嵌套结构对应的树形数据模型：解析器把一维 HTML 文本变成二维树（根 = document）。

**关键点**：文本也是节点（TextNode）——树里没有裸字符串；iframe = 多个文档的特例（每个文档一棵树）。

**爬虫意义**：`DOMParser().parseFromString(html)` → 树 → `querySelector` 按结构取数；"用正则解析 HTML"不完备（正则是一维扫描，树是二维结构）。
