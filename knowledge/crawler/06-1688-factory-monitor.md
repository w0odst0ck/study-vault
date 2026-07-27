---
status: active
created: 2026-07-18
updated: 2026-07-18
tags:
  - 爬虫
  - 1688
  - 工厂监控
  - 全链路采集
cards: []
---

# 1688 工厂监控全链路采集

> 来源：factory-monitor 项目（1688-factory-monitor → PageHarvest/factory-monitor/）
> 日期：2026-07-18

## 项目定位

监控 1688 平台上优质工厂的商品变化：定时扫描搜索页 → 遍历名片页 → 采集产品目录 → 过滤 + 预警。

## 全链路流水线

```
阶段一  搜索 5 页（~120 家）→ 全部入库 status=active
阶段二  打开名片页找到产品目录 URL → 回填 catalog_url
阶段三  打开产品目录页 → 滚动加载全部商品 → 排序取 Top10 → 写快照
阶段四  Top10 ≥2 个含灯类关键词 → active，否则 paused
阶段五  对比两次快照 → 数据异常/增长信号 → 写 alerts
```

### 模块划分

| 文件 | 作用 |
|------|------|
| `collector/search.py` | 搜索 5 页 + 名片页补全 catalog_url |
| `collector/offers.py` | 产品目录采集 + 滚动加载 + Top10 排序 + 入库 |
| `engine/alerter.py` | 预警引擎（数据异常 + 增长信号） |
| `engine/filter.py` | 商品级过滤：Top10 ≥2 个灯类关键词保留，否则 paused |
| `cli/run.py` | 一键编排：搜索 → 采集 → 过滤 → 预警 |
| `cli/query.py` | 查询 CLI |

## 关键踩坑记录（8 条）

### 1. URL 编码
- 1688 工厂搜索页使用 **GBK** 编码中文关键词，非 UTF-8
- 直接 requests 传中文会乱码，需 `urllib.parse.quote(keyword, encoding='gbk')`

### 2. Card URL 拼接
- 不从 DOM `<a>` 标签取链接（不可靠）
- 从 `data-aplus-report` 属性取 `item_id`，拼接成完整 URL

### 3. Cookie 上下文
- `chromium.launch()` 不会自动创建浏览器上下文
- 需显式调用 `browser.new_context()` 再 `context.new_page()`

### 4. wait_until 策略
- 1688 页面的长连接使 `"networkidle"` 一直超时
- 改为 `"load"` 或 `"domcontentloaded"` 即可

### 5. Alias ID
- 部分工厂的 `memberId` 是简短别名[ⓘ]（如 `wellfinesilicone`），非标准的 `b2b-` 前缀
- 遍历时需判断：是 alias 则跳过（因为 alias 的工厂详情页无法直接访问）

### 6. 产品目录页入口定位
- 名片页内通过 `data-btrack[ⓘ]="pc-card-shop-gallery-btn"` 属性定位入口
- **shopURL[ⓘ] 不可直接推导**为产品目录 URL，必须从名片页 DOM 获取

### 7. UNIQUE 冲突[ⓘ]
- `shop_url` 字段设为 UNIQUE，但初始占位符为空字符串 → 多条记录互相覆盖
- 方案：`shop_url=card_url`（每家不同）+ 新增专用 `catalog_url` 字段

### 8. 产品目录页懒加载
- 默认只渲染 ~20 个商品
- 需滚动到底部[ⓘ]触发懒加载，才能获取完整商品列表

## 踩坑模式总结

| 类型 | 数量 | 代表 |
|------|------|------|
| **编码问题** | 1 | GBK 关键词 |
| **DOM 解析** | 2 | Card URL、产品目录入口 |
| **Playwright 特性** | 3 | Cookie 上下文、wait_until、滚动懒加载 |
| **数据库设计** | 1 | UNIQUE + 空占位符冲突 |
| **数据多样性** | 1 | Alias ID |

## 架构模式

### 验证驱动开发
先写 `collector/verify.py[ⓘ]` 逐步骤验证 DOM 选择器，验证通过后再提取为正式脚本。验证脚本保留作为选择器参考。

### 分层隔离
```
core/        ← 基础设施（db / browser）
collector/   ← 采集逻辑（search / offers）
engine/      ← 业务逻辑（filter / alert）
cli/         ← 入口编排（run / query）
```

## 回顾

- Q: 1688 工厂搜索页的中文关键词编码方式是什么？
  A: 使用 GBK 编码[ⓘ]，非 UTF-8。需 `urllib.parse.quote(keyword, encoding='gbk')`。
- Q: `chromium.launch()` 之后缺少什么关键步骤？
  A: 不会自动创建浏览器上下文，需显式调用 `browser.new_context()` 再 `context.new_page()`。
- Q: 1688 页面使用 `"networkidle"` 等待策略时为什么会超时？
  A: 页面长连接导致 `"networkidle"` 一直等待网络空闲，改为 `"load"` 或 `"domcontentloaded"`。
- Q: 产品目录页 URL 能直接从 shopURL 推导出来吗？
  A: 不能。必须从名片页 DOM 中通过 `data-btrack="pc-card-shop-gallery-btn"` 属性定位入口获取。
- Q: shop_url UNIQUE 约束导致空字符串覆盖问题的解决方案是什么？
  A: 初始 `shop_url=card_url`（每家不同）+ 新增专用 `catalog_url` 字段，避免空占位符冲突。
- Q: 验证驱动开发的模式是怎样的？
  A: 先写验证脚本逐步骤验证 DOM 选择器，验证通过后再提取为正式脚本，验证脚本保留作为选择器参考。
