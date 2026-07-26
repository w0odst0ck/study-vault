---
{
  "status": "active",
  "created": "2026-07-23",
  "updated": "2026-07-25",
  "tags": [
    "项目管理",
    "项目启动",
    "知识库",
    "方案馆"
  ],
  "cards": [
    "programming-一期和二期规划的核心区别-041",
    "programming-为什么采用三轮递进而非一-043",
    "programming-数据源的国内外比例和角色-042",
    "programming-知识库型项目的三层打包策-039",
    "programming-项目目录结构标准包含哪些-040"
  ]
}
---

# 知识库型项目启动方法论

> 来源：智能照明方案馆项目
> 日期：2026-07-23

## 项目定位策略：产品 + 方案 + 案例打包

### 核心理念
- **三层打包** — 产品选型 + 方案设计 + 案例参照，形成完整交付闭环
- **方案先行** — 写方案文档再动手，文无习惯"方案先行，决策后动，不擅自动手"
- **双期规划** — 一期做场景方案库（产品+设计+标准），二期叠加控制系统层（DALI/KNX/Zigbee/EMC）

### 项目目录结构标准

```
项目根/
├── plan/           # 项目规划、计划书、技术选型
├── memory/         # 每日复盘日志，格式 YYYY-MM-DD.md
├── collector/      # 自动采集工具（Python 脚本 + 配置）
├── refs/           # 素材/参考（按 subdir 分组，含 _manual_todo.md）
├── solutions/      # 方案文档（按场景分目录，含 _template.md）
├── README.md       # 项目说明
├── STATUS.md       # 进度看板
└── .gitignore
```

## 项目分期规划

### 第一期：场景方案库
- 覆盖产品选型、场景设计、照度标准
- 20 个场景（P0 办公/工厂/仓库/停车场，P1 商业/学校/医院，P2 酒店）
- 构建最全的照明方案库

### 第二期：智能照明改造
- 在一期方案库基础上叠加控制系统层
- 覆盖 DALI/KNX/Zigbee/EMC 等控制协议
- 提供改造方案 + 成本估算 + 实施指南

## 用户习惯与协作模式

- **用户风格**：方案先行，决策后动，不擅自动手
- **项目经理模式**：提供完整方案供评审，不做先行开发
- **命名约定**：项目中称呼用户为"文无"

## 技术选型策略

### 采集技术栈
```python
# 采集层
requests          # 静态页面 HTTP
bs4 + lxml        # HTML 解析
playwright        # 动态 JS 渲染页面
# 数据处理
pandas            # 数据整理与分析
# 存储
markdown + JSON   # 正文 + 元数据分离
```

### 数据源策略
- **国内源**（42 个）：灯厂9 + 集成商8 + IoT 3 + 控制厂商7 + 论文4 + 文档3 + 招标2 + 市场报告4 + 芯片2
- **国外源**（仅参考）：Signify、Lutron、Acuity Brands、Osram、Zumtobel 等 10 家

### 采集轮次
```bash
# 三轮递进
round1   → 核心 10 场景（P0）
round2   → 扩展 10 场景（P1+P2）
round3   → 交叉回填（补充遗漏）

# CLI 命令
python collector.py round1
python collector.py round2
python collector.py round3
python collector.py all
python collector.py status  # 进度看板
```

## 关键决策记录

1. **双期规划** — 一期纯方案库先跑通，二期再叠加智能控制层，降低初始复杂度
2. **国内源为主** — 42 vs 10 国内外源比例，国外仅做参考不主动采集
3. **三轮递进** — 不一次性全量采集，按优先级分轮次推进
4. **config.toml 驱动** — 所有数据源配在 toml 中，不用代码硬编码
5. **自动+手动混合** — 自动采集优先，自动失败标注 manual 统一收集

## 回顾
<!-- cards: programming-一期和二期规划的核心区别-041, programming-为什么采用三轮递进而非一-043, programming-数据源的国内外比例和角色-042, programming-知识库型项目的三层打包策-039, programming-项目目录结构标准包含哪些-040 -->
<!-- cards: programming-一期和二期规划的核心区别-041, programming-为什么采用三轮递进而非一-043, programming-数据源的国内外比例和角色-042, programming-知识库型项目的三层打包策-039, programming-项目目录结构标准包含哪些-040 -->
<!-- cards: programming-一期和二期规划的核心区别-041, programming-为什么采用三轮递进而非一-043, programming-数据源的国内外比例和角色-042, programming-知识库型项目的三层打包策-039, programming-项目目录结构标准包含哪些-040 -->
- Q: 知识库型项目的三层打包策略是什么？
  A: 产品选型 + 方案设计 + 案例参照，形成产品层、设计层、实证层的完整交付闭环。
- Q: 项目目录结构标准包含哪些核心目录？
  A: plan/（规划）、memory/（每日复盘）、collector/（采集工具）、refs/（素材）、solutions/（方案输出），加上 README.md、STATUS.md、.gitignore。
- Q: 一期和二期规划的核心区别是什么？
  A: 一期做纯场景方案库（产品+设计+标准，20 个场景），二期叠加控制系统层（DALI/KNX/Zigbee/EMC），在方案基础上做智能改造方案。
- Q: 数据源的国内外比例和角色分工是什么？
  A: 国内 42 个源（灯厂/集成商/IoT/控制厂商/论文/招标等），主动采集主力；国外 10 个源（Signify/Lutron 等），仅做参考不主动采集。
- Q: 为什么采用三轮递进而非一次性全量采集？
  A: 降低初始复杂度，按场景优先级分轮推进：round1 核心 10 场景（P0），round2 扩展 10 场景（P1+P2），round3 交叉回填补充遗漏。
