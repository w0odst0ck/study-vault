栈是一种后进先出（LIFO, Last In First Out）的数据结构，在 Python 中可以通过列表（`list`）或`collections.deque`来实现栈的功能。以下是栈框架的常见操作：

### 1. 初始化

- **基于列表实现**：创建一个空列表来表示栈，如 `stack = []`。
- **基于 `collections.deque` 实现**：使用 `deque` 类创建一个空的双端队列，并利用其一端模拟栈，如 `from collections import deque; stack = deque()`。

### 2. 入栈操作

- **基于列表实现**：使用列表的 `append()` 方法将元素添加到列表末尾，即栈顶位置。
- **基于 `collections.deque` 实现**：使用 `deque` 的 `append()` 方法将元素添加到双端队列的右端（作为栈顶）。

### 3. 出栈操作

- **基于列表实现**：使用列表的 `pop()` 方法移除并返回列表的最后一个元素，即栈顶元素。如果栈为空，调用 `pop()` 会引发 `IndexError` 异常。
- **基于 `collections.deque` 实现**：使用 `deque` 的 `pop()` 方法移除并返回双端队列的右端元素（栈顶元素）。如果双端队列为空，调用 `pop()` 会引发 `IndexError` 异常。

### 4. 获取栈顶元素

- **基于列表实现**：通过访问列表的最后一个元素（索引为 -1）来获取栈顶元素，但不会移除该元素。如果栈为空，直接访问会引发 `IndexError` 异常。
- **基于 `collections.deque` 实现**：访问双端队列的右端元素（索引为 -1）来获取栈顶元素，同样不会移除该元素。若双端队列为空，访问会引发 `IndexError` 异常。

### 5. 判断栈是否为空

- **基于列表实现**：检查列表的长度是否为 0，即 `if not stack:` 或 `if len(stack) == 0:`。
- **基于 `collections.deque` 实现**：检查双端队列的长度是否为 0，即 `if not stack:` 或 `if len(stack) == 0:`。

### 6. 获取栈的大小

- **基于列表实现**：使用 `len()` 函数获取列表的长度，即栈中元素的个数。
- **基于 `collections.deque` 实现**：使用 `len()` 函数获取双端队列的长度，也就是栈的大小。