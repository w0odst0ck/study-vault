---
{
  "status": "active",
  "created": "2026-07-17",
  "updated": "2026-07-21",
  "tags": [
    "编程",
    "Pydantic",
    "数据建模"
  ],
  "cards": [
    "programming-Pydanticv2-001",
    "programming-Pydantic中-003",
    "programming-配置管理的三层搜索路径优-002"
  ]
}
---

# Pydantic v2 数据模型设计实战

> 来源：StarLink 项目
> 日期：2026-07

## 核心模型体系

### Repo / Note / Relation 三层模型

```python
# 仓库数据
class RepoData(BaseModel):
    owner: str = Field(min_length=1)
    name: str = Field(min_length=1)
    full_name: str                                    # model_validator[ⓘ] 自动校验
    description: Optional[str] = None
    topics: list[str] = Field(default_factory=list)
    readme_snippet: Optional[str] = Field(None, max_length=2000)
    starred_at: Optional[datetime] = None
    language: Optional[str] = None
    html_url: HttpUrl

# 笔记数据
class NoteData(BaseModel):
    repo: str
    list_name: str = Field(default="未分类")
    status: Literal["unreviewed", "reviewed", "archived"] = "unreviewed"
    relations: list[RelationRef] = Field(default_factory=list)   # 升格为 Ref 对象
    created_at: datetime = Field(default_factory=datetime.now)

# 关系 / 聚类 / 全局图
class Relation(BaseModel):
    source: str
    target: str
    relation_type: str = "related"
    confidence: float = Field(default=0.5, ge=0, le=1)

class Cluster(BaseModel):
    id: str
    name: str
    repos: list[str] = Field(min_length=2)
    common_topics: list[str] = Field(default_factory=list)
    # average_confidence 移除（衍生值不存文件[ⓘ]）

class GlobalGraph(BaseModel):
    nodes: dict[str, RepoData] = Field(default_factory=dict)
    edges: list[Relation] = Field(default_factory=list)
    cluster_map: dict[str, list[str]] = Field(default_factory=dict)
    # orphans 移除，改为 compute_orphans() 方法
```

### 设计要点

```python
# 1. model_validator 确保数据一致性
@model_validator(mode="after")
def check_full_name(cls, v):
    expected = f"{v.owner}/{v.name}"
    assert v.full_name == expected, f"full_name must be {expected}"
    return v

# 2. Literal 约束有限状态
status: Literal["unreviewed", "reviewed", "archived"]

# 3. Priority 范围约束
priority: int = Field(default=3, ge=1, le=5)

# 4. MaxLength[ⓘ] 防止内存爆炸
readme_snippet: Optional[str] = Field(None, max_length=2000)
```

## 配置管理设计

### 三层搜索路径

```python
def find_config(cwd: Path = None) -> Path:
    """配置搜索路径：--config > ./star-vault.yaml > 内置默认值"""
    cwd = cwd or Path.cwd()
    # 1. 命令行指定
    if cli_config:
        return cli_config
    # 2. 当前目录
    yaml_path = cwd / "star-vault.yaml"
    if yaml_path.exists():
        return yaml_path
    # 3. 内置默认值（无 config 也能启动，但 token 必填）
    return None
```

### 变量优先级
```
环境变量 > config.yaml > 代码默认值
```

### 安全
```python
def mask[ⓘ](value: str) -> str:
    """脱敏函数，Token 只显示首尾"""
    if len(value) <= 8:
        return value[:2] + "****" + value[-2:]
    return value[:4] + "****" + value[-4:]
```

## 状态管理

```python
class StateManager:
    """基于 JSON 文件的增量同步状态"""
    
    def needs_sync(self, repo_full_name: str, sha: str) -> bool:
        """starred_at + sha 对比判断是否需要同步"""
    
    def get_new_repos_since(self, cutoff: datetime) -> list[str]:
        """获取截止时间后的新 repo"""
```

## 设计教训

1. **衍生值不存文件** — `average_confidence` 改为方法而非字段
2. **orphans 不持久化** — 改为 `compute_orphans()` 方法计算
3. **GitHub API snake_case 天然匹配** — Pydantic 无需 `Field(alias=...)`
4. **Full name 校验器保底** — 避免 owner/name 不一致
5. **Literal 类型优于枚举** — 轻量、可序列化、API 友好
6. **MinLength/MaxLength 防御式编程** — 尽早失败，不要等内存爆炸

## 回顾
<!-- cards: programming-Pydanticv2-001, programming-Pydantic中-003, programming-配置管理的三层搜索路径优-002 -->
<!-- cards: programming-Pydanticv2-001, programming-Pydantic中-003, programming-配置管理的三层搜索路径优-002 -->
<!-- cards: programming-Pydanticv2-001, programming-Pydantic中-003, programming-配置管理的三层搜索路径优-002 -->
- Q: Pydantic v2 中 `model_validator` 的主要用途是什么？
  A: 在数据验证通过后执行额外逻辑，如校验 `full_name` 必须等于 `owner/name` 格式，确保数据一致性。
- Q: 配置管理的三层搜索路径优先级是什么？
  A: `--config` 命令行指定 > `./star-vault.yaml` 配置文件 > 内置默认值。环境变量进一步覆盖配置值。
- Q: Pydantic 中 `Literal` 类型相比枚举有什么优势？
  A: 轻量（无需定义类）、天然可序列化为 JSON、API 友好，适合有限状态如 `status: Literal["unreviewed", "reviewed", "archived"]`。
