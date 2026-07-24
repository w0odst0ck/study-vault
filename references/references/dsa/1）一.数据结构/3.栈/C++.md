在 C++ 中，栈操作主要通过 `std::stack` 类模板来实现，它定义在 `<stack>` 头文件中。`std::stack` 是一个容器适配器，默认基于 `std::deque` 实现，也可以使用其他支持 `back()`、`push_back()` 和 `pop_back()` 操作的容器（如 `std::vector`、`std::list`）来实现。以下是 `std::stack` 的常见操作：

1. **声明与初始化**
    
    - **默认初始化**：创建一个空栈，`std::stack<Type> stackName;`，其中 `Type` 是栈中元素的数据类型。
    - **使用已有容器初始化**：`std::stack<Type, Container> stackName(container);`，这里 `Container` 是底层容器（如 `std::deque`、`std::vector`、`std::list`），`container` 是该类型的容器对象。
    
2. **元素访问**
    
    - **获取栈顶元素**：`stackName.top();` 返回栈顶元素的引用，但不删除该元素。需注意在调用此方法前，应确保栈不为空。
    
3. **元素操作**
    
    - **入栈**：`stackName.push(element);` 将 `element` 压入栈顶，栈的大小增加 1。
    - **出栈**：`stackName.pop();` 移除栈顶元素，栈的大小减少 1。此操作不返回被移除的元素，调用前需确保栈不为空。
    
4. **状态查询**
    
    - **检查栈是否为空**：`stackName.empty();` 如果栈为空返回 `true`，否则返回 `false`。
    - **获取栈的大小**：`stackName.size();` 返回栈中元素的个数。
    
5. **其他操作**
    
    - **交换两个栈的内容**：`stackName1.swap(stackName2);` 交换 `stackName1` 和 `stackName2` 的内容，这两个栈的类型必须相同。也可以使用全局函数 `std::swap(stackName1, stackName2);` 实现相同功能。