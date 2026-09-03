---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - Python
  - 多任务
  - asyncio
  - 线程
  - 进程
  - GIL
cards: []
---

# Python 多任务编程

> 进程 / 线程 / 协程 + GIL + asyncio
> 来源：旧知识库「编程语言基础/Python/5.多任务编程」

---

## 1. 进程、线程、协程

| 维度 | 进程 | 线程 | 协程 |
|------|------|------|------|
| 资源 | 独立内存空间 | 共享进程内存 | 共享线程内存 |
| 切换 | 内核态，开销大 | 内核态，中等 | 用户态，极轻量 |
| 并发 | 真并行（多核） | GIL 限制（Python） | 单线程内并发 |
| 适用 | CPU 密集 | I/O 密集 | 高并发 I/O |
| 通信 | IPC（队列/管道） | 共享变量（需加锁） | 直接 await |

---

## 2. GIL 全局解释器锁

**Python 的 GIL（Global Interpreter Lock）**：同一时刻只有一个线程执行 Python 字节码。

### 影响

- **CPU 密集**：多线程反而慢（切换开销 > 并行收益）
- **I/O 密集**：多线程有用（I/O 等待时释放 GIL）

### 绕开 GIL 的方案

```python
# 1. 多进程（每个进程独立 GIL）
from multiprocessing import Pool

# 2. C 扩展（释放 GIL）
# numpy / pandas 底层 C 代码自行释放 GIL

# 3. 协程（根本不需要 GIL）
import asyncio
```

---

## 3. threading 多线程

```python
import threading
import time

def worker(name):
    print(f"线程 {name} 开始")
    time.sleep(1)
    print(f"线程 {name} 结束")

threads = []
for i in range(3):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()  # 等待所有线程结束
```

### 线程安全：锁

```python
lock = threading.Lock()
shared = 0

def safe_add():
    global shared
    with lock:          # 自动 acquire/release
        shared += 1
```

---

## 4. multiprocessing 多进程

```python
from multiprocessing import Pool

def square(x):
    return x * x

with Pool(4) as p:
    result = p.map(square, [1, 2, 3, 4, 5])
    print(result)  # [1, 4, 9, 16, 25]
```

**模式识别**：CPU 密集用 `multiprocessing.Pool`，I/O 密集用 `threading` 或 `asyncio`

---

## 5. asyncio 异步协程

```python
import asyncio

async def fetch_data(url):
    print(f"开始请求: {url}")
    await asyncio.sleep(1)  # 模拟 I/O 等待
    print(f"完成请求: {url}")
    return f"数据_{url}"

async def main():
    tasks = [
        fetch_data("A"),
        fetch_data("B"),
        fetch_data("C"),
    ]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())
```

### async/await 关键概念

| 概念 | 说明 |
|------|------|
| `async def` | 定义协程函数 |
| `await` | 挂起当前协程，让出控制权 |
| `asyncio.run()` | 入口，运行顶层协程 |
| `asyncio.gather()` | 并发执行多个协程 |
| 事件循环 | 调度协程的核心（单线程） |

**模式识别**：`async def` + `await` = Python 协程标准写法。`await` 只能在 `async` 函数内使用。

---

## 选择策略

```python
# CPU 密集 → multiprocessing
# I/O 密集 → asyncio（优先）或 threading
# 简易并行 → concurrent.futures
```

```python
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as ex:
    futures = [ex.submit(worker, i) for i in range(4)]
    for f in futures:
        print(f.result())
```

---

## 回顾

- Q: GIL 是什么？对多线程有什么影响？
  A: Global Interpreter Lock，同一时刻只有一个线程执行 Python 字节码。CPU 密集任务多线程反而慢，I/O 密集任务多线程可用（I/O 等待时释放 GIL）

- Q: 协程相比线程的优势是什么？
  A: 协程用户态切换，无内核开销，内存占用极小（几千协程 vs 几千线程不可行），适合高并发 I/O 场景

- Q: `asyncio.gather()` 的作用？
  A: 并发执行多个 awaitable 对象，返回所有结果列表。任一协程异常则全部取消（可用 `return_exceptions=True` 避免）

- Q: CPU 密集任务在 Python 中应该用什么？
  A: `multiprocessing.Pool` — 多进程绕开 GIL，利用多核并行

- Q: `threading.Lock` 的 with 语句用法？
  A: `with lock:` 自动 `acquire()`，离开 with 块自动 `release()`，避免忘记释放导致死锁
