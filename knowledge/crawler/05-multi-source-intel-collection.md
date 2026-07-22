---
{
  "status": "active",
  "created": "2026-07-17",
  "updated": "2026-07-22",
  "tags": [
    "爬虫",
    "情报采集",
    "架构设计"
  ],
  "cards": [
    "crawler-Intel模块的领域分-016",
    "crawler-LLM调用失败时的安全-018",
    "crawler-数据源协议选择的优先级顺-017",
    "crawler-跨天去重用什么方法清理-019"
  ]
}
---

# 多数据源情报采集（Intel 模块）架构

> 来源：BriefNexus 项目 intel/ 模块
> 日期：2026-07

## 架构设计：适配器模式 + 配置驱动

### 模块结构

```python
intel/
├── main.py                    # CLI 入口（crawl/export/generate/all）
├── intel_config.ini           # 源开关配置
├── collector/
│   ├── __init__.py            # 采集器注册表
│   └── platforms/             # 平台适配器（可插拔）
│       ├── base.py            # BaseCollector 基类
│       ├── white_house.py     # White House Briefing Room（政策）
│       ├── eu_commission.py   # EU Press Corner（政策）
│       ├── nvidia_blog.py     # NVIDIA Blog（技术）
│       ├── sec_edgar.py       # SEC EDGAR 8-K（合规）
│       └── globenewswire.py   # GlobeNewswire（资本）
├── engine/
│   ├── dedup.py               # MD5 去重[ⓘ]
│   └── exporter.py            # JSON 导出
└── output/                    # .gitignore
```

### 配置注册

```ini
[sources]
enabled = white_house:intel.collector.platforms.white_house:WhiteHouseCollector,
          nvidia_blog:intel.collector.platforms.nvidia_blog:NvidiaBlogCollector
```

**扩展新源只需：写适配器类 + 注册配置，引擎代码零修改。**

## 数据源演化

| 版本 | 采集器 | 领域 |
|------|--------|------|
| v1 | arXiv/CSA/上海住建委 | 学术/照明 |
| v2 | WH/EU/NVIDIA/SEC/GlobeNewswire/Fed | 全球科技/政策/金融 |
| v2.1 +金融 | 东方财富/巨潮/央行 | 国内金融 |
| v3 +感知 | arXiv arXiv感知/ADAS期刊 | 自动驾驶 |

### 移除教训[ⓘ]
- **arXiv** → 不适用宏观科技资讯
- **CSA** → 数据源变动
- **上海住建委** → 单城市维度太窄
- **GlobeNewswire** → RSS 400
- **Federal Reserve** → RSS 403
- **央行** → connection reset
- **东方财富** → 418 反爬

## 领域分类体系

```python
class Domain(str, Enum):
    FINANCE = "finance"           # 金融/资本
    SELF_DRIVING = "self_driving" # 自动驾驶
    SEMICONDUCTOR = "semiconductor"  # 半导体（规划）
```

- `-d` 参数必选，支持按领域过滤
- `list` 按领域分组展示

## 跨天去重

```python
class DedupStore:
    """MD5 去重持久化"""
    # 存储：MD5 hash → JSON 文件
    # 清理：30 天过期自动清理
    # 验证：23 条 → 第二次 0 条（全被去重拦住）
```

## 全流程输出

```bash
# 采集 → 导出（格式不限）
python -m intel.main crawl
python -m intel.main export --format markdown
python -m intel.main generate --llm     # LLM 可选
```

### LLM 异常安全[ⓘ]
- LLM 默认禁用，`--llm` 标志按需启用
- 调用失败返回 `None`，不 `sys.exit(1)`
- 规则分类保底

## 数据源类型分析

| 协议 | 特点 | 举例 |
|------|------|------|
| **RSS/Atom[ⓘ]** | 标准、稳定、结构化 | EU Commission/SEC EDGAR |
| **HTML 解析** | 灵活但脆弱 | White House |
| **REST API** | 强、但有限流 | arXiv API/SAMR API |
| **JS 渲染** | 最难处理 | 东方财富/巨潮 |
| **Connection Reset** | 最隐蔽 | 央行 |

### 协议选择建议
```
首选: 官方 API（有限流但稳定）
次选: RSS/Atom Feed
后备: HTML 解析（页面结构变则代码变）
避免: JS 渲染页面（除非 Playwright）

## 回顾
<!-- cards: crawler-Intel模块的领域分-016, crawler-LLM调用失败时的安全-018, crawler-数据源协议选择的优先级顺-017, crawler-跨天去重用什么方法清理-019 -->
<!-- cards: crawler-Intel模块的领域分-016, crawler-LLM调用失败时的安全-018, crawler-数据源协议选择的优先级顺-017, crawler-跨天去重用什么方法清理-019 -->
<!-- cards: crawler-Intel模块的领域分-016, crawler-LLM调用失败时的安全-018, crawler-数据源协议选择的优先级顺-017, crawler-跨天去重用什么方法清理-019 -->
- Q: Intel 模块的领域分类体系有哪些？
  A: finance（金融/资本）、self_driving（自动驾驶）、semiconductor（半导体，规划中）。`-d` 参数必选，支持按领域过滤和分组展示。
- Q: 数据源协议选择的优先级顺序是什么？
  A: 官方 API（有限流但稳定）> RSS/Atom Feed（标准稳定）> HTML 解析（灵活但页面结构变则代码变）> 避免 JS 渲染页面。
- Q: LLM 调用失败时的安全策略是什么？
  A: LLM 默认禁用（`--llm` 按需启用），调用失败返回 `None` 不 `sys.exit(1)`，规则分类保底。
- Q: 跨天去重用什么方法？清理策略是什么？
  A: MD5 hash 持久化去重，30 天过期自动清理。23 条源数据第二次采集 0 条，全被去重拦住。
```
