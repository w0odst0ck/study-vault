---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - Python
  - FastAPI
  - Web
  - API
cards: []
---

# FastAPI 实战入门

> 核心概念 + 项目骨架 + 依赖注入 + 异步支持
> 来源：旧知识库「编程语言基础/Python/Fastapi」

---

## 1. 最小服务

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}
```

启动：`uvicorn main:app --reload` → 浏览器 `http://localhost:8000/docs`（自动 Swagger UI）

---

## 2. 路径参数与查询参数

```python
@app.get("/items/{item_id}")
def get_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

| 参数位置 | 声明方式 | 示例 |
|---------|---------|------|
| 路径参数 | 函数参数同名 | `item_id: int` |
| 查询参数 | 非路径参数 | `q: str = None` |
| 请求体 | `pydantic.BaseModel` | `item: Item` |

---

## 3. Pydantic 模型作为请求体

```python
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    price: float
    is_offer: bool = False

@app.post("/items/")
def create_item(item: Item):
    return {"name": item.name, "price": item.price * 0.9}
```

**核心优势**：自动校验 + 自动生成 API 文档 + IDE 类型提示

---

## 4. 依赖注入

```python
from fastapi import Depends

def pagination(page: int = 1, size: int = 20):
    return {"page": page, "size": size}

@app.get("/items/")
def list_items(p: dict = Depends(pagination)):
    return p
```

**用途**：共享逻辑（分页/认证/数据库会话）无需重复编写

### 类作为依赖（可复用带状态）

```python
class CommonParams:
    def __init__(self, page: int = 1, size: int = 20):
        self.page = page
        self.size = size

@app.get("/items/")
def list_items(params: CommonParams = Depends()):
    return {"page": params.page, "size": params.size}
```

---

## 5. 异步处理

```python
@app.get("/async-data")
async def get_async():
    # await 外部 API / 数据库查询
    result = await fetch_some_data()
    return result
```

**何时用 `async def` 而非 `def`**？

| 场景 | 推荐 |
|------|------|
| 数据库查询（async ORM） | `async def` |
| HTTP 请求（httpx/aiohttp） | `async def` |
| CPU 计算 | `def`（否则阻塞事件循环） |
| 简单 CRUD（同步 ORM） | `def`（FastAPI 自动放线程池） |

---

## 6. 项目目录建议

```
project/
├── main.py              # 应用入口 + 路由注册
├── routers/             # 路由模块
│   ├── items.py
│   └── users.py
├── models.py            # Pydantic 模型
├── database.py          # 数据库连接
├── dependencies.py      # 公共依赖
└── config.py            # 配置
```

---

## 回顾

- Q: FastAPI 如何自动生成 API 文档？
  A: 启动后自动在 `/docs`（Swagger UI）和 `/redoc`（ReDoc）提供交互式文档

- Q: FastAPI 依赖注入（Depends）的优势？
  A: 自动解析参数、可复用共享逻辑、支持类/函数作为依赖、自动注入到 Swagger 文档

- Q: FastAPI 的 `async def` 和 `def` 如何选择？
  A: I/O 密集（async ORM/HTTP 请求）用 `async def`；CPU 密集或同步数据库用 `def`（FastAPI 自动放线程池执行）

- Q: FastAPI 请求体验证的底层是什么？
  A: Pydantic v2 模型定义 → 自动解析 JSON 请求体 → 类型校验 + 字段验证 → 返回 422 或处理后数据

- Q: FastAPI 主项目结构的最佳实践？
  A: routers/ 分离路由、models.py 放 Pydantic 模型、dependencies.py 放公共依赖、config.py 放配置
