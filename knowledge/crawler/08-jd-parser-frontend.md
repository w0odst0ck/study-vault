---
status: active
created: 2026-07-21
updated: 2026-07-21
tags:
  - 爬虫
  - 前端解析
  - 京东
  - JS
  - DOMParser
  - XSS
cards: []
---

# 京东前端解析器（JS）

> 纯浏览器端 JS 解析器，兼容新旧 JD 商品页，提取全量结构化数据

## 背景

JD 商品页存在两种渲染版本：

- **旧版**：传统服务端渲染，DOM 结构稳定，class 名可预测
- **新版（React 2025+）**：CSS 类名压缩混淆，但关键结构（`class=price/value/attrs/item/top-name`）未被混淆，属性表 `attrs` 仍存在于渲染 DOM

## 解析器架构

### 平台检测

```javascript
function quickScan(html) {
  // 快速扫描前 20% 内容判定平台
  // 返回平台标识 + 旧版/新版标记
}
```

`quickScan` 在 20% 内容处即可告知用户平台类型，无需等全量加载。

### 解析流程

1. **DOMParser 预解析**：`parseDetail` 一次解析 7-12MB HTML → 复用 doc 给所有子函数
2. **字段提取**：各子函数接收 doc 参数独立提取
3. **数据合并**：`toRows` 统一输出为结构化行

```
parseDetail(html)
  ├─ quickScan(html)         → 平台 + 版本
  ├─ extractTitle(doc)       → 标题
  ├─ extractBrand(doc)       → 品牌
  ├─ extractModel(doc)       → 型号
  ├─ extractPrice(doc)       → 全量价格（min/max）
  ├─ extractShop(doc)        → 店铺
  ├─ extractImages(doc)      → 主图 CDN
  ├─ extractAttrs(doc)       → 属性表
  ├─ extractHighlight(doc)   → 高亮属性
  ├─ extractSales(doc)       → 已售
  ├─ extractRate(doc)        → 好评率
  └─ extractTags(doc)        → 标签
```

### 新旧兼容

| 字段 | 旧版方式 | 新版方式 |
|------|---------|---------|
| 属性表 | CSS class 匹配 | unquoted attrs 正则匹配 |
| 价格 | DOM 选择器 | 全量匹配 `class=price value` 块 |
| 图片 | DOM 属性 | 360buyimg CDN 筛选 |

### 全量价格采集

多 SKU 页面包含 15-18 个价格变体。循环匹配全部 `class=price value` 块，取 min/max 记录。

## 关键技术决策

### DOMParser 复用

一次 `parseDetail` 预解析 DOM，传递 doc 给所有子函数。避免三次解析 7-12MB HTML。

**风险**：jsdom 中超过 10MB HTML 会崩。生产始终在浏览器端运行，浏览器对 15MB+ DOM 处理正常。

### XSS 防护

图片列使用 DOM API 构建（`document.createElement('img')`），禁止 `innerHTML` 拼接。

### 多版本检测

`quickScan` 快速扫描 + 提前告知用户平台类型。失败时显示失败文件明细（文件名 + 原因）。

## 测试数据

- `test_jd_detail.html` + `test_jd.zip`：模拟旧版 JD 页
- `test_jd_real.zip`：松下 + 米家真实详情页，17MB

## 确认状态

| 平台 | 检测 | 核心数据 | 属性表 | 评价 |
|------|------|---------|--------|------|
| 1688 | ✅ | ✅ | ✅ | ✅ |
| 震坤行 | ✅ | ✅ | ✅ | ✅ |
| 京东（旧版）| ✅ | ✅ | ✅ | ✅ |
| 京东（新版）| ✅ | ✅ | ✅（20 项）| ✅（50万+）|

## 回顾

### 京东新版页面和旧版的核心区别是什么？

新版页面使用 React 2025+ 渲染，CSS 类名被压缩混淆。旧版 class 名可预测。但关键结构 `class=price/value/attrs/item/top-name` 在新版中未被混淆，属性表 `attrs` 仍存在于渲染 DOM 中。

### 为什么要复用 DOMParser？

每次解析 7-12MB HTML，三次独立解析性能差。一次解析传递 doc 给所有子函数，整体解析时间从 3× 降到 1×。但 jsdom 中超过 10MB 会崩溃——此限制仅限 Node 端，浏览器端正常。

### 多 SKU 页面的价格如何采集？

循环匹配全部 `class=price value` 块，一个多 SKU 页面通常包含 15-18 个价格变体。取最小值作为售价、最大值作为原价记录。

### 前端解析器如何防止 XSS？

图片列使用 DOM API (`document.createElement('img')`) 构建，禁止 `innerHTML` 拼接商品数据。所有用户可控字段走 DOM API 设置属性/文本内容。

### quickScan 的作用是什么？

快速扫描前 20% HTML 内容即可判定平台类型和版本，无需等待全量加载完成。让用户 20% 进度时就获得平台识别反馈。

### 京东新版属性表如何提取？

attribute 页面中 `<div class=attrs>` 实际存在于渲染 DOM。新版通过 unquoted attrs 正则匹配提取，而不是旧版的 CSS class 匹配。
