---
{
  "status": "active",
  "created": "2026-07-23",
  "updated": "2026-09-03",
  "tags": [
    "爬虫",
    "采集架构",
    "质量管理",
    "数据源"
  ],
  "cards": [
    "crawler-manual机制的工作-038",
    "crawler-precheck预检命-039",
    "crawler-全量采集规范要求每来源产-037",
    "crawler-多源采集流水线的三种采集-036",
    "crawler-配置驱动原则的关键约束是-040"
  ]
}
---

# 多源知识采集流水线架构

> 来源：智能照明方案馆项目 collector/
> 日期：2026-07-23

## 架构设计：配置驱动 + 适配器模式 + 三轮递进

### 采集器分层

```
collector/
├── collector.py          # CLI 入口（round1/round2/round3/all/status）
├── config.toml           # 数据源配置（场景驱动，三轮分源）
├── requirements.txt      # Python 依赖
├── fetchers/             # 采集器（按协议分类）
│   ├── static_fetcher.py # requests + bs4 静态页面
│   ├── dynamic_fetcher.py# playwright JS 渲染
│   └── pdf_fetcher.py    # PDF 下载 + content-type 检测
├── parsers/              # 解析器（按来源定制）
│   ├── base.py           # BaseParser 基类
│   └── wbus_parser.py    # Wbus 解析器示例
└── storage.py            # 存储工具（正文 md + 原始 HTML + 图片 + PDF + 报告）
```

### 采集器协议分类

| 协议类型 | 技术方案 | 适用场景 | 处理策略 |
|---------|---------|---------|---------|
| 静态 HTML | requests + bs4 + lxml | 大部分国内企业官网 | 直接采集解析 |
| 动态 JS | playwright | 单页应用、反爬 JS 校验 | 自动跳过→标 manual |
| PDF | requests + content-type 检测 | 产品手册、国家标准 | 加 content-type 校验避免误判 |
| API | requests JSON | 开放数据接口 | 频率限制控制 |

## 数据源生命周期管理

### 来源分类与预检

```
precheck 命令：python collector.py precheck

结果类型:
- OK      → 23 个（可正常采集）
- 动态跳过 → 10 个（需 playwright，自动标 manual）
- 不可达   → 5 个（PAK PDF 过期、安科瑞 JS、知乎屏蔽等）
```

### 不可达源处理（manual 机制）

```
自动失败 → 标注 manual:类型+URL+说明 → 写入 refs/_manual_todo.md → 统一收集
```

示例：`manual:PDF-index|https://paksmart.com/download|PDF 目录页无直接下载链接`

### 数据源配置示例

```toml
[source.opple]
name = "欧普照明"
url = "https://www.opple.com/product/..."
type = "static"
scenario = "office"

[source.philips]
name = "飞利浦"
url = "https://www.signify.com/..."
type = "dynamic"
scenario = "general"
```

## 全量采集规范

### 每来源 5 类产出

| # | 产出 | 用途 | 存储位置 |
|---|------|------|---------|
| 1 | 正文 md | 知识文档素材 | `refs/{scenario}/{source}/content.md` |
| 2 | 原始 HTML | 追溯原始数据 | `refs/{scenario}/{source}/raw.html` |
| 3 | 图片 | 视觉参考 | `refs/{scenario}/{source}/images/` |
| 4 | PDF | 原版文档 | `refs/{scenario}/{source}/docs/` |
| 5 | 采集报告 | 状态与元数据 | `refs/{scenario}/{source}/report.json` |

### 处理优先级

```
自动采集（首选项） → 自动失败产生 manual 标记
    → 手动收集（浏览器操作） → 素材落地到 refs/
```

## 进度管理

### STATUS.md 看板格式

```
### 办公场景 [P0] [完成]
  ✅ 欧普照明
  ✅ 雷士照明
  ✅ 飞利浦
  🔄 三雄极光 (采集运行中)
  ⏳ 松下 (排队中)
  ⚠️ 安科瑞 (manual:不可达)

### 工厂场景 [P0] [进行中]
  ✅ 海洋王
  ⏳ 华荣照明
  ...
```

## 配置驱动原则

- **config.toml 是唯一数据源配置**，代码不做硬编码
- 新增数据源：改 toml + 写适配器（如有新协议类型）
- 新增场景：按场景分组 toml 配置 + 创建 refs/ 目录
- 采集器 CLI 只读 config，不关心具体来源

## 回顾
<!-- cards: crawler-manual机制的工作-038, crawler-precheck预检命-039, crawler-全量采集规范要求每来源产-037, crawler-多源采集流水线的三种采集-036, crawler-配置驱动原则的关键约束是-040 -->
<!-- cards: crawler-manual机制的工作-038, crawler-precheck预检命-039, crawler-全量采集规范要求每来源产-037, crawler-多源采集流水线的三种采集-036, crawler-配置驱动原则的关键约束是-040 -->
<!-- cards: crawler-manual机制的工作-038, crawler-precheck预检命-039, crawler-全量采集规范要求每来源产-037, crawler-多源采集流水线的三种采集-036, crawler-配置驱动原则的关键约束是-040 -->
<!-- cards: crawler-manual机制的工作-038, crawler-precheck预检命-039, crawler-全量采集规范要求每来源产-037, crawler-多源采集流水线的三种采集-036, crawler-配置驱动原则的关键约束是-040 -->
<!-- cards: crawler-manual机制的工作-038, crawler-precheck预检命-039, crawler-全量采集规范要求每来源产-037, crawler-多源采集流水线的三种采集-036, crawler-配置驱动原则的关键约束是-040 -->
- Q: 多源采集流水线的三种采集器类型是什么？
  A: static_fetcher（requests+bs4 静态页面）、dynamic_fetcher（playwright JS 渲染）、pdf_fetcher（带 content-type 检测的 PDF 下载）。
- Q: 全量采集规范要求每来源产出哪 5 类文件？
  A: ① 正文 md（知识素材）、② 原始 HTML（追溯用）、③ 图片（视觉参考）、④ PDF（原版文档）、⑤ 采集报告（状态与元数据）。
- Q: manual 机制的工作流程是什么？
  A: 自动采集失败 → 标注 `manual:类型+URL+说明` → 统一写入 `refs/_manual_todo.md` → 手动收集完成后落地到对应 refs/ 目录。
- Q: precheck 预检命令的结果类型有哪些？
  A: OK（可正常采集）、动态跳过（需 playwright 自动标 manual）、不可达（连接失败，标记原因）。
- Q: 配置驱动原则的关键约束是什么？
  A: config.toml 是唯一数据源配置，代码不做硬编码。新增源只改 toml + 写适配器（如有新协议），采集器 CLI 只读 config 不关心具体来源。
