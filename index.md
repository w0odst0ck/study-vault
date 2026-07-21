# 🎋 知识库索引

> 青简 · 知识整理 · 学而时习之

## 📊 知识库状态

> 站点当前为空骨架。启动方法详见 README。

| 功能 | 链接 |
|------|------|
| 📇 复习页 | `site/review/` |
| 📊 仪表盘 | `site/index.html` |

## 目录结构

```
study-vault/
├── index.md       ← 本文件
├── scripts/       ← 辅助脚本
│   └── review.py  ← 复习引擎 + 注释工具 + 仪表盘
├── site/          ← 复习小站前端
│   ├── review/    ← SM-2 复习页面
│   └── index.html ← 仪表盘
└── .github/       ← CI/CD 工作流
```

## 本地私有内容（不上传）

```
knowledge/        ← 知识文档
memory/           ← 每日复盘
plan/             ← 学习规划
review/           ← 复习卡片
annotations/      ← 注释
references/       ← 参考资源
glossary/         ← 术语表
project-refs/     ← 项目参考
```

数据积累途径：写知识文档 → `review.py import` → `review.py export` → `review.py deploy`

## 脚本

```bash
python3 scripts/review.py                # 复习到期卡片
python3 scripts/review.py import         # 从 knowledge/ 提取卡片
python3 scripts/review.py export         # 导出到 site/data/cards.json
python3 scripts/review.py deploy         # 导出 + 提交 + 推送（一键上线）
python3 scripts/review.py stats          # 查看统计
```

无需第三方依赖，Python 3.7+ 即可。
