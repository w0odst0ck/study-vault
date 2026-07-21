# Literal（字面量类型）

Python 的 `typing.Literal`，限制变量只能取指定值。

```python
from typing import Literal

status: Literal["unreviewed", "reviewed", "archived"]
# status 只能取这三个值之一
```

**优势**：轻量、可序列化、API 友好，比枚举类简单。
