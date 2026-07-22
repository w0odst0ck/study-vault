# 🎋 study-vault

> 🔗 [w0odst0ck.github.io/study-vault](https://w0odst0ck.github.io/study-vault/)

个人知识库。写文档 → 自动生成复习卡 → 间隔重复 → 在线/本地预览。

## 数据状态

| 指标 | 数值 |
|------|------|
| 知识文档 | 42 篇 |
| 复习卡片 | 191 张 |
| 覆盖域 | 7 个 |
| 连续天数 | 🔥 当前 streak |

## 7 个知识域

| 域 | 文档 | 卡片 |
|----|------|------|
| 爬虫 | 8 篇 | 35 张 |
| 数据分析 | 2 篇 | 8 张 |
| 数据工程 | 3 篇 | 10 张 |
| 独立站 | 4 篇 | 20 张 |
| 数据结构与算法 | 13 篇 | 70 张 |
| 机器学习 | 2 篇 | 10 张 |
| 编程 | 8 篇 | 38 张 |

## 快速开始

```bash
# 本地预览
python3 scripts/serve.py          # http://localhost:8080

# 写知识文档 → 自动提取卡片（含自动导出）
python3 scripts/review.py import  # 从 knowledge/ 提取复习卡片

# 复习
python3 scripts/review.py         # 默认进入复习模式
python3 scripts/review.py --quick --count 5  # 速刷 5 张

# 统计
python3 scripts/review.py stats   # 查看统计
```

## 目录结构

```
study-vault/
├── knowledge/            ← 知识文档（42 篇，7 个域）
│   ├── crawler/         ← 爬虫技术
│   ├── data-analysis/   ← 数据分析
│   ├── data-engineering/ ← 数据工程
│   ├── dsa/             ← 数据结构与算法
│   ├── independent-site/ ← 独立站
│   ├── machine-learning/ ← 机器学习
│   └── programming/     ← 编程
├── references/           ← 外部参考手册+题库
├── review/               ← 复习卡片（191 张）
├── plan/                 ← 学习规划
├── scripts/              ← 辅助脚本
├── site/                 ← 前端页面
├── memory/               ← 每日复盘
├── annotations/          ← 正文注释
├── glossary/             ← 术语表
└── project-refs/         ← 项目参考
```

## 工作流

```
写文档（knowledge/xxx.md）
  → python3 scripts/review.py import（自动提取卡片 + 自动导出）
  → python3 scripts/review.py（复习到期卡片）
  → python3 scripts/serve.py（本地预览）
```

无需第三方依赖，Python 3.7+ 即可。
