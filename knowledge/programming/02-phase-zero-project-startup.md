---
{
  "status": "active",
  "created": "2026-07-17",
  "updated": "2026-07-18",
  "tags": [
    "编程",
    "项目管理",
    "项目启动"
  ],
  "cards": [
    "programming-GitHubAPI同-006",
    "programming-Phase0阶段的四-004",
    "programming-关系引擎中规则[ⓘ]和AI-005"
  ]
}
---

# 阶段化项目启动（Phase 0) 实战

> 来源：StarLink 项目
> 日期：2026-07

## Phase 0 执行策略

### 核心理念
- **设计文档先行[ⓘ]** — 先写设计文档再写代码
- **成本优化** — 默认 gpt-4o-mini + 缓存 + `--limit`
- **增量同步[ⓘ]** — 用 `starred_at[ⓘ]` + `sha` 对比，不做全量
- **配置与骨架一体化** — 启动即跑，不需要先配环境

### Phase 0 任务拆分示例（StarLink 15 子任务）

```
0.1 项目骨架 + 配置 + 状态管理  ✅
0.2 数据模型（Pydantic v2）    ✅
0.3 同步引擎（GitHub API）      ✅
0.4 笔记模板（Jinja2）          ✅
0.5 Vault 写入                  ✅
0.6 索引生成（INDEX.md）        ✅
0.7 关系骨架                    ✅
0.8 规则引擎                    ✅
0.9 AI 客户端 + 缓存            📋
0.10 Prompt 调试                ✅
0.11 CLI 入口                   📋
```

## 同步引擎设计

### 增量同步

```python
def sync(mode: Literal["full", "incremental"] = "incremental"):
    """增量/全量双模式同步"""
    if mode == "incremental":
        cutoff = state.get_last_sync_time()
        repos = fetch_starred(cutoff=cutoff)  # 只取新增
    else:
        repos = fetch_starred()               # 全量拉取
```

### GitHub API 调用

```python
def fetch_starred(token: str, cutoff: datetime = None, limit: int = None):
    """分页 + cutoff 增量 + limit 控制"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.star+json",
    }
    # 发现：star+json header 是必须的，否则不返回 starred_at
    # 发现：Lists API 404（非个人账号不可用）
    # 发现：README 返回 base64 编码，需额外解码
```

## 关系引擎设计

### 规则引擎架构

```python
class BaseRelationRule(ABC):
    """规则基类，子类实现 analyze()"""
    
class TopicOverlapRule(BaseRelationRule):
    """话题重叠规则：检测 repos 间共同 topic"""
    
class LanguageDomainRule(BaseRelationRule):
    """语言领域规则：检测同语言项目聚类"""

class BuiltinEngine:
    """内置引擎，组合多条规则"""
    rules: list[BaseRelationRule]
```

### 规则 vs AI 的关系
- **规则**：即时的、确定性的、零成本的聚类（话题重叠、语言分类）
- **AI**：灵活的、语义的、高成本的深层分析
- **混合模式**：AI 只做规则无法覆盖的范围

## 索引生成设计

```python
def generate_index(repos: list[RepoData]) -> str:
    """分组自动生成 INDEX.md"""
    # 按 list_name 分组
    # 每个组内按字母序排列
    # 空 TODO.md 显示 "暂无 TODO 项"
    # 只按 list_name 分组，不做交叉索引（省 2/3 输出量）
```

## 实用技巧

### Jinja2 模板
```python
# templates/repo.md.j2 — 笔记模板
## {{ repo.name }}
- **描述**: {{ repo.description }}
- **语言**: {{ repo.language }}
- **Topics**: {{ ", ".join(repo.topics) }}
```

### 原子写入
```python
# 避免写入中断导致文件损坏
import os
os.replace[ⓘ](temp_path, target_path)
```

### 模块路径自动定位
```python
# 通过 __file__ 自动定位模板目录，可注入覆盖
TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
```

## 关键决策记录

1. **配置搜索路径砍到 2 级** — `--config` / `./star-vault.yaml` / 内置默认值
2. **空 token 零容忍** — 启动即报错，不优雅降级
3. **state.path 在 StateManager 内拼接** — 外部不关心路径计算
4. **`find_config` 纯函数** — 支持 cwd 注入测试
5. **砍掉 VaultManager 类** — 改为 `write_note()` / `slug_for_repo()` 函数
6. **砍掉 RepoRelations** — `GlobalGraph.relations_for()` 替代

## 回顾
<!-- cards: programming-GitHubAPI同-006, programming-Phase0阶段的四-004, programming-关系引擎中规则和AI-005 -->
<!-- cards: programming-GitHubAPI同-006, programming-Phase0阶段的四-004, programming-关系引擎中规则和AI-005 -->
- Q: Phase 0 阶段的四个核心理念是什么？
  A: ①设计文档先行——先写设计文档再写代码；②成本优化——默认 gpt-4o-mini + 缓存 + `--limit`；③增量同步——用 `starred_at` + `sha` 对比，不做全量；④配置与骨架一体化——启动即跑，不需要先配环境。
- Q: 关系引擎中规则和 AI 的分工策略是什么？
  A: 规则做即时、确定性、零成本的聚类（话题重叠、语言分类），AI 做灵活、语义、高成本的深层分析。混合模式下 AI 只做规则覆盖不到的范围。
- Q: GitHub API 同步中的三个重要发现是什么？
  A: ①`star+json` header 必须带，否则不返回 `starred_at`；② Lists API 返回 404（非个人账号不可用）；③ README 返回 base64 编码，需额外解码。
