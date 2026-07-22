1. **使用 `list` 实现栈框架操作**
    
    - **初始化**：通过 `stack = []` 创建一个空栈。
    - **入栈（Push）**：使用 `append()` 方法将元素添加到列表末尾，即 `stack.append(element)`，其中 `element` 是要入栈的元素。
    - **出栈（Pop）**：使用 `pop()` 方法移除并返回列表的最后一个元素，即 `popped_element = stack.pop()`。若栈为空时调用 `pop()`，会引发 `IndexError` 异常。
    - **查看栈顶元素（Peek）**：通过访问列表的最后一个元素来查看栈顶元素，即 `top_element = stack[-1]`，若栈为空会引发 `IndexError` 异常。
    - **判断栈是否为空**：使用 `len()` 函数检查列表长度是否为 0，即 `is_empty = len(stack) == 0`。
    - **获取栈的大小**：使用 `len()` 函数获取列表的长度，即 `stack_size = len(stack)`。
    
2. **使用 `collections.deque` 实现栈框架操作**
    
    - **导入模块**：首先需要导入 `collections` 模块，即 `from collections import deque`。
    - **初始化**：通过 `stack = deque()` 创建一个空栈。
    - **入栈（Push）**：使用 `append()` 方法将元素添加到双端队列的右端（等同于栈顶），即 `stack.append(element)`，其中 `element` 是要入栈的元素。
    - **出栈（Pop）**：使用 `pop()` 方法移除并返回双端队列的右端元素，即 `popped_element = stack.pop()`。若栈为空时调用 `pop()`，会引发 `IndexError` 异常。
    - **查看栈顶元素（Peek）**：通过访问双端队列的最后一个元素来查看栈顶元素，即 `top_element = stack[-1]`，若栈为空会引发 `IndexError` 异常。
    - **判断栈是否为空**：使用 `len()` 函数检查双端队列长度是否为 0，即 `is_empty = len(stack) == 0`。
    - **获取栈的大小**：使用 `len()` 函数获取双端队列的长度，即 `stack_size = len(stack)`。
    

在实际应用中，`collections.deque` 在两端操作元素时效率更高，对于栈操作（主要在一端进行），如果性能要求较高，`collections.deque` 是更好的选择，而 `list` 实现栈相对更简洁直观，适用于简单场景。