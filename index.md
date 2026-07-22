# 🎋 知识库索引

> 青简 · 知识整理 · 学而时习之

## 📊 知识库状态

| 指标 | 数值 |
|------|------|
| 知识文档 | **36 篇** |
| 复习卡片 | **166 张** |
| 覆盖领域 | 5 个（爬虫 / 数据分析 / 独立站 / DSA / 编程） |

| 入口 | 链接 |
|------|------|
| 📇 复习页 | `site/review/` |
| 📊 仪表盘 | `site/index.html` |
| 📚 知识库 | `knowledge/` |
| 📖 术语表 | `glossary/` |
| 🗺️ 学习规划 | `plan/` |
| 📚 参考手册 | `references/_index.md` |

---

## 知识文档总览

### 数据结构与算法（13 篇 + 93 篇参考）

| # | 文档 | 卡数 |
|---|------|------|
| 01 | [数组、双指针、滑动窗口](knowledge/dsa/01-array-two-pointer-sliding-window.md) | 6 |
| 02 | [链表](knowledge/dsa/02-linked-list.md) | 6 |
| 03 | [栈与队列](knowledge/dsa/03-stack-queue.md) | 5 |
| 04 | [哈希表](knowledge/dsa/04-hash-table.md) | 5 |
| 05 | [二分查找](knowledge/dsa/05-binary-search.md) | 6 |
| 06 | [回溯](knowledge/dsa/06-backtracking.md) | 5 |
| 07 | [动态规划](knowledge/dsa/07-dynamic-programming.md) | 6 |
| 08 | [二叉树](knowledge/dsa/08-binary-tree.md) | 6 |
| 09 | [排序算法](knowledge/dsa/09-sorting.md) | 5 |
| 10 | [贪心算法](knowledge/dsa/10-greedy.md) | 5 |
| 11 | [复杂度分析](knowledge/dsa/11-complexity-analysis.md) | 5 |
| 12 | [Python 刷题踩坑](knowledge/dsa/12-python-dsa-pitfalls.md) | 10 |
| 13 | [解题思维方法论](knowledge/dsa/13-dsa-solve-methodology.md) | 5 |
| — | 多语参考 + LeetCode 课程 | [`references/dsa/_index.md`](references/dsa/_index.md) |

### 爬虫（8 篇 · 35 张卡）

| # | 文档 | 卡数 |
|---|------|------|
| 01 | [B2B 反爬实战](knowledge/crawler/01-b2b-platforms-anti-crawl.md) | 4 |
| 02 | [Playwright 浏览器管理器](knowledge/crawler/02-playwright-browser-manager.md) | 3 |
| 03 | [国家标准采集](knowledge/crawler/03-national-standard-collection.md) | 4 |
| 04 | [PDF 参数页定位器](knowledge/crawler/04-pdf-parameter-locator.md) | 4 |
| 05 | [多源情报采集架构](knowledge/crawler/05-multi-source-intel-collection.md) | 4 |
| 06 | [1688 工厂监控流水线](knowledge/crawler/06-1688-factory-monitor.md) | 6 |
| 07 | [纯前端 JS 解析器架构](knowledge/crawler/07-client-side-parser-architecture.md) | 4 |
| 08 | [京东前端解析器](knowledge/crawler/08-jd-parser-frontend.md) | 6 |

### 独立站（4 篇 · 20 张卡）

| # | 文档 | 卡数 |
|---|------|------|
| 01 | [WooCommerce 技术选型](knowledge/independent-site/01-woocommerce-tech-stack-selection.md) | 5 |
| 02 | [竞品逛站方法论](knowledge/independent-site/02-competitive-site-survey-methodology.md) | 5 |
| 03 | [截图仿站工具选型](knowledge/independent-site/03-screenshot-to-site-tool-selection.md) | 5 |
| 04 | [项目重构方法论](knowledge/independent-site/04-project-restructure-methodology.md) | 5 |

### 编程（8 篇 · 38 张卡）

| # | 文档 | 卡数 |
|---|------|------|
| 01 | [Pydantic v2 模型设计](knowledge/programming/01-pydantic-v2-model-design.md) | 4 |
| 02 | [阶段化项目启动](knowledge/programming/02-phase-zero-project-startup.md) | 4 |
| 03 | [项目整合策略](knowledge/programming/03-project-integration-strategy.md) | 5 |
| 04 | [Python 高级特性](knowledge/programming/04-python-advanced.md) | 5 |
| 05 | [Python 面向对象编程](knowledge/programming/05-python-oop.md) | 5 |
| 06 | [Python 多任务编程](knowledge/programming/06-python-multitask.md) | 5 |
| 07 | [FastAPI 实战入门](knowledge/programming/07-fastapi.md) | 5 |
| 99 | [三语对比总结](knowledge/programming/99-cross-language-comparison.md) | 5 |

### 数据分析（1 篇 · 3 张卡）

| 文档 | 卡数 |
|------|------|
| [B2B 选品与价格监控](knowledge/data-analysis/01-b2b-selection-and-price-monitor.md) | 3 |

---

## 工作流

```bash
# 写知识文档 → 提取卡片 → 导出 → 部署
python3 scripts/review.py import          # 从 knowledge/ 提取复习卡片
python3 scripts/review.py                 # 复习到期卡片
python3 scripts/review.py stats           # 查看统计
python3 scripts/review.py export          # 导出到 site/data/cards.json
python3 scripts/serve.py                  # http://localhost:8080
```

## 目录结构

```
study-vault/
├── index.md           ← 本文件（知识库总索引）
├── knowledge/         ← 知识文档（36 篇，5 个域）
├── references/        ← 参考资源（dsa 三语手册 + leetcode）
├── plan/              ← 学习规划（13 个领域）
├── review/            ← 复习卡片（166 张）
├── memory/            ← 每日复盘
├── scripts/           ← 辅助脚本（review.py / serve.py）
├── site/              ← 前端页面（复习页 / 仪表盘）
├── annotations/       ← 正文注释（10 篇）
├── glossary/          ← 术语表（12 条）
└── project-refs/      ← 项目参考
```
