---
status: active
created: 2026-07-18
updated: 2026-07-20
tags:
  - 编程
  - 项目管理
  - 项目整合
  - 仓库管理
cards: []
---

# 子项目整合进父仓库的策略

> 来源：PageHarvest/PH 项目整合（factory-monitor + price-compare 移入 PH）
> 日期：2026-07-18

## 背景

多个独立小项目各自有独立目录、独立 `.venv`、独立 `.git`，维护成本高。需要整合进父项目（PageHarvest/PH），统一管理。

## 整合步骤

```
① 子项目整体移入父项目目录（保留独立目录结构）
② 各自的 .venv 删除，统一使用父项目的 venv
③ 各自的 .git 清除（独立提交历史不再保留）
④ 父项目的 .guard.md[ⓘ] 标注子目录为自由开发区域
⑤ 父项目的 .gitignore 加入子目录的敏感数据排除条目
⑥ 提交两次：隐私安全 → 功能变更
```

## .guard.md 自由开发区标注

`.guard.md` 是项目目录的访问权限标注文件。整合后标注方式：

```markdown
## 自由开发目录[ⓘ]

以下目录团队成员可自由修改，无需审核：
- factory-monitor/
- price-compare/
```

作用：明确告知团队（或 AI Agent）哪些目录可以直接改，哪些需要审核。

## .gitignore 分层策略

父项目的 `.gitignore` 需要覆盖所有子项目的敏感数据模式：

```gitignore
# Cookies & 登录态
cookies/

# 数据库
*.db

# 数据文件
*.xlsx
cache/

# Python
__pycache__/
*.pyc
.venv/[ⓘ]

# 配置（含敏感 token）
*.env
config/local.yaml
```

原则：宁多勿漏，敏感数据一概不入库。

## 提交策略

```
第一轮 commit[ⓘ]：隐私安全
  清理敏感数据、更新 .gitignore、确认无 token/key 泄露
  
第二轮 commit：功能变更
  整合代码、更新文档、标注 .guard.md
```

两轮拆分确保安全审查和功能变更可独立追溯。

## 虚拟环境统一

- 子项目各自的 `.venv` 废除
- 统一使用父项目的虚拟环境
- 子项目的 `requirements.txt` 合并到父项目
- 统一 `python -m` 调用路径，避免跨环境依赖问题

## 项目目录建议

整合后的父项目结构：

```
PageHarvest/
├── .guard.md              ← 访问权限标注
├── .gitignore             ← 全局敏感数据排除
├── .venv/                 ← 统一虚拟环境
├── factory-monitor/       ← 子项目 1（自由开发）
│   ├── core/
│   ├── collector/
│   ├── engine/
│   ├── cli/
│   └── README.md
├── price-compare/         ← 子项目 2（自由开发）
│   ├── ...
├── shared/                ← 公共模块（可选）
└── docs/                  ← 整合文档
```

## 踩坑：`git mv` 链条中断恢复（2026-07-20）

### 场景

在项目目录重构（如大迁移 25→9 顶层目录）时，使用 `git mv` 移动未跟踪（untracked）的文件/目录会导致 `mv` 链条中断。

**表现：** `git status` 显示文件已被 staged（索引中有新路径），但物理文件并未移动（旧路径依然存在），提交后出现文件内容缺失。

### 恢复方法

```bash
# 从 git 的 HEAD 版本恢复文件到新位置
git show HEAD:old/path > new/path
# 逐个文件恢复
```

逐文件从 git 历史中取出内容写入新路径。

**预防：** 先用 `mv file new/path/`（物理移动）+ `git add` 再提交，而非直接 `git mv` 未跟踪的文件。

## 回顾

- Q: 子项目整合进父项目的标准步骤是什么？
  A: ①移入父项目目录 ②删除独立 .venv ③清除独立 .git ④更新父项目 .guard.md ⑤更新 .gitignore ⑥分两轮提交（隐私安全→功能变更）。
- Q: .guard.md 在项目整合中起什么作用？
  A: 标注哪些目录是自由开发区域（可直接修改无需审核），明确告知团队或 AI Agent 的权限边界。
- Q: 整合时 .gitignore 的维护原则是什么？
  A: 宁多勿漏——覆盖所有子项目的敏感数据模式（cookies/*.db/*.xlsx/cache/.env 等），敏感数据一概不入库。
- Q: 整合时的两轮提交策略分别是什么？
  A: 第一轮提交隐私安全（清理敏感数据、更新 .gitignore），第二轮提交功能变更（整合代码、更新文档）。
