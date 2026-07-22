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

- Q: 京东新版页面和旧版的核心区别是什么？
  A: 新版 React 2025+ 渲染，CSS 类名压缩混淆。关键结构 `class=price/value/attrs/item/top-name` 未被混淆，属性表仍存在于渲染 DOM
- Q: 为什么京东解析器要复用 DOMParser？
  A: 每次 parse 7-12MB HTML，三次独立解析性能差。一次解析传 doc 给所有子函数，时间从 3× 降到 1×。jsdom 超 10MB 会崩（Node 端限制，浏览器端正常）
- Q: 多 SKU 京东页面的价格如何采集？
  A: 循环匹配全部 `class=price value` 块，15-18 个价格变体，取 min 为售价、max 为原价
- Q: 前端解析器如何防止 XSS？
  A: 图片用 `document.createElement('img')` DOM API 构建，禁止 `innerHTML` 拼接商品数据
- Q: quickScan 的作用是什么？
  A: 快速扫描前 20% HTML 即可判定平台类型和版本，无需全量加载，让用户 20% 进度时获得识别反馈
- Q: 京东新版属性表如何提取？
  A: `<div class=attrs>` 存在于渲染 DOM。新版通过 unquoted attrs 正则匹配提取，非旧版 CSS class 匹配
