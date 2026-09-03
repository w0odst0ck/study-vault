# 注：HTML 解析（15-html-parsing）

> crawler-learning B2 入库后补注（2026-09-03）

## L1 术语

### DOMParser [ⓘ]
浏览器的容错 HTML 解析器：`new DOMParser().parseFromString(html, 'text/html')` 把任意 HTML 字符串变成 document（DOM 树）。
容错：标签不闭合/属性无引号等"不合法" HTML，真实浏览器和 DOMParser 都按 HTML5 解析算法修复，结果基本一致——所以解析器比正则稳。
**爬虫用法**：抓到的 HTML 先 DOMParser 成树 → querySelector 按结构取数（PageHarvest parser.js 第一件事）。

### DOM 树 [ⓘ]
HTML 嵌套结构对应的树形数据：一维文本 → 二维树。根 = document；**文本也是节点**（TextNode），树里没有裸字符串。
有了树就能问结构问题："div 里第一个 p 是什么？" → `querySelector('div p')`。
解析的本质：一维文本 → 二维树 → 按结构取数据。
见 [glossary/DOM](../glossary/DOM.md)。
