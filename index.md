# 🎋 知识库索引

> 青简 · 知识整理 · 学而时习之

<!-- DASHBOARD_START -->

## 📊 知识库状态

> 更新于 2026-07-18

```
  知识文档     10 篇    复习卡片     38 张
  注释文件     10 篇    今日到期     33 张
  术语表      12 个     连续天数    1 🔥
  已标记 [ⓘ]  10 篇    留存率      13.2%
```

| 领域 | 知识 | 注释 | 卡片 |
|------|------|------|------|
| crawler | 6篇 | 6篇 | 25张 |
| data-analysis | 1篇 | 1篇 | 3张 |
| programming | 3篇 | 3篇 | 10张 |

---

<!-- DASHBOARD_END -->

## 领域总览

### 1️⃣ AI & 认知架构

| 领域 | 规划 | 知识 | 说明 |
|------|------|------|------|
| RAG | [plan/01-rag.md](plan/01-rag.md) | [knowledge/rag/](knowledge/rag/) | 检索增强生成 — 知识库核心引擎 |
| MCP | [plan/02-mcp.md](plan/02-mcp.md) | [knowledge/mcp/](knowledge/mcp/) | Model Context Protocol — 接口标准 |

### 2️⃣ Web & 数据采集

| 领域 | 规划 | 知识 | 说明 |
|------|------|------|------|
| 爬虫 | [plan/03-crawler.md](plan/03-crawler.md) | [knowledge/crawler/](knowledge/crawler/) | 数据源获取与清洗 · B2B反爬 · Playwright · 国标采集 · PDF定位 · 多源情报 |
| 独立站 | [plan/04-independent-site.md](plan/04-independent-site.md) | [knowledge/independent-site/](knowledge/independent-site/) | 从零建站相关技术栈 |

### 3️⃣ 数据 & 统计

| 领域 | 规划 | 知识 | 说明 |
|------|------|------|------|
| 数据分析 | [plan/05-data-analysis.md](plan/05-data-analysis.md) | [knowledge/data-analysis/](knowledge/data-analysis/) | 工程化数据分析方法论 · B2B选品 · 价格监控 |
| 概率论与数理统计 | [plan/06-probability-statistics.md](plan/06-probability-statistics.md) | [knowledge/probability-statistics/](knowledge/probability-statistics/) | 统计学基础（复习） |

### 4️⃣ 计算机科学基础

| 领域 | 规划 | 知识 | 说明 |
|------|------|------|------|
| 编程 | [plan/07-programming.md](plan/07-programming.md) | [knowledge/programming/](knowledge/programming/) | 语言基础、范式、最佳实践 · Pydantic v2 · Phase0启动 |
| 数据结构与算法 | [plan/08-dsa.md](plan/08-dsa.md) | [knowledge/dsa/](knowledge/dsa/) | 核心数据结构、算法设计与分析（复习） |
| 分布式系统 | [plan/09-distributed-systems.md](plan/09-distributed-systems.md) | [knowledge/distributed-systems/](knowledge/distributed-systems/) | 分布式理论、一致性、容错 |

### 5️⃣ 自动驾驶 & 机器人

| 领域 | 规划 | 知识 | 说明 |
|------|------|------|------|
| 自动驾驶算法 | [plan/10-autonomous-driving.md](plan/10-autonomous-driving.md) | [knowledge/autonomous-driving/](knowledge/autonomous-driving/) | 感知、规划、控制（复习） |
| ROS | [plan/11-ros.md](plan/11-ros.md) | [knowledge/ros/](knowledge/ros/) | 机器人操作系统（复习） |
| CARLA | [plan/12-carla.md](plan/12-carla.md) | [knowledge/carla/](knowledge/carla/) | 自动驾驶仿真器 |

### 6️⃣ 基础设施

| 领域 | 规划 | 知识 | 说明 |
|------|------|------|------|
| 大数据 | [plan/13-big-data.md](plan/13-big-data.md) | [knowledge/big-data/](knowledge/big-data/) | 大数据生态、存储与计算框架 |

---

## 目录结构

```
study-vault/
├── index.md              ← 本文件，领域总纲
├── plan/                 ← 各领域规划 + 进度跟踪
├── knowledge/            ← 知识文档（13 个领域子目录）
├── references/           ← 跨领域参考资源
│   ├── books.md
│   ├── courses.md
│   ├── papers.md
│   ├── repos.md
│   ├── tools.md
│   └── datasets.md
├── project-refs/         ← 项目参考页
│   ├── independent-site.md
│   └── autonomous-driving.md
├── review/               ← 复习模块（SM-2 间隔重复）
│   ├── stats.json
│   ├── _review-log.md
│   └── cards/{domain}/
├── scripts/              ← 辅助脚本
│   └── review.py
└── memory/               ← 按时间戳存档的复盘记忆
```

## 复习模块

复习引擎 `scripts/review.py`，支持：

- **自动抽取**：`python scripts/review.py import` — 扫描 knowledge/ 下 QA，生成复习卡片
- **间隔重复**：`python scripts/review.py` — 每天跑，到期卡片自动弹出→打分→调度下次
- **多种模式**：`--quick` 5 张速刷、`--domain rag` 专项、`--reset` 重置
- **统计追踪**：`stats` 命令查看总额、到期、连续天数、留存率
- **复盘闭环**：复习记录自动写入 `memory/`

详情见 [plan/REVIEW.md](plan/REVIEW.md)。

## 交叉引用机制

- **plan/** → 各领域规划 + 实时进度跟踪表
- **knowledge/** → 对应领域的知识文档，平铺目录便于 RAG 索引
- **references/** → 跨领域共享资源（一本书可能覆盖多个域）
- **project-refs/** → 项目→知识域的映射表，一个项目涉及哪些领域一目了然
- **memory/** → 复盘记录沉淀点，内容提炼后进入 knowledge/

> 一条知识的完整生命周期：**Plan → Learn → Knowledge Doc → Reference (可选) → Review (memory/)**

## 规划原则

- **工作向**：RAG、MCP、爬虫、独立站、数据分析、大数据、分布式系统
- **复习向**：概率论与数理统计、数据结构与算法、自动驾驶算法、ROS、CARLA
- **编程**：贯穿所有领域的基础能力，持续积累

---

> 知识库拟接入 MCP 接口 + RAG 架构，当前已完成骨架搭建。
