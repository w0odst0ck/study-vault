# 🎋 study-vault

活的知识库。技术知识积累 + SM-2 间隔复习 + 复盘沉淀。

## 站点功能

| 页面 | 链接 | 说明 |
|------|------|------|
| 📊 **仪表盘** | `site/index.html` | 卡片统计 + 快速入口 |
| 📇 **复习** | `site/review/` | SM-2 间隔重复（键盘操作） |
| 📚 **知识库** | `site/knowledge/` | 目录树 + 文档阅读 + 全文搜索 + 注释侧栏 |
| 📖 **术语表** | `site/glossary/` | 术语浏览 + 搜索筛选 |
| 🔗 **参考资源** | `site/references/` | 书籍 / 课程 / 工具 / 数据集 |

## 公开内容

```
study-vault/
├── index.md         ← 领域总纲
├── scripts/         ← 辅助脚本
│   └── review.py    ← 复习引擎 + 数据导出
├── site/            ← GitHub Pages 前端
│   ├── index.html   ← 仪表盘
│   ├── knowledge/   ← 知识库阅读器
│   ├── review/      ← 复习页
│   ├── glossary/    ← 术语表
│   ├── references/  ← 参考资源
│   └── data/        ← JSON 数据（自动导出）
├── knowledge/       ← 知识文档（11 篇）
├── review/          ← 复习卡片（38 张）
├── annotations/     ← 注释（56 条）
├── glossary/        ← 术语表（12 个）
└── references/      ← 参考资源索引
```

## 本地私有内容（不上传）

```
memory/          ← 每日复盘日志
plan/            ← 学习规划
project-refs/    ← 项目参考页
```

## 日常使用

```bash
# 本地启动
python3 scripts/serve.py              # 启动本地服务 → http://localhost:8080

# 新增知识
vim knowledge/xxx.md                  # 写知识文档
python3 scripts/review.py import      # 提取复习卡片

# 复习
python3 scripts/review.py             # 到期卡片
python3 scripts/review.py --quick     # 速刷 5 张

# 导出 + 部署
python3 scripts/review.py export      # 生成前端数据
python3 scripts/review.py deploy      # 导出 → 提交 → 推送到 GitHub Pages
```

## 脚本

```bash
python3 scripts/review.py                # 复习到期卡片
python3 scripts/review.py import         # 从 knowledge/ 提取卡片
python3 scripts/review.py export         # 导出全部站点数据
python3 scripts/review.py deploy         # 导出 + 提交 + 推送到 GitHub
python3 scripts/review.py stats          # 统计信息
```

无需第三方依赖，Python 3.7+ 即可。
