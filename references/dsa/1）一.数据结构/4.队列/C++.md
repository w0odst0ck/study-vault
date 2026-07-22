在 C++ 中，队列操作主要通过`std::queue`类模板来实现，它定义在`<queue>`头文件中。`std::queue`是一个容器适配器，默认基于`std::deque`实现，也可使用其他满足特定条件（支持`front()`、`back()`、`push_back()` 和 `pop_front()` 操作）的容器，如`std::list`。以下是`std::queue`的常见操作：

### 声明与初始化

1. **默认初始化**：创建一个空队列，`std::queue<Type> queueName;`，其中`Type`是队列中元素的数据类型。
2. **使用已有容器初始化**：`std::queue<Type, Container> queueName(container);`，这里`Container`是底层容器（如`std::deque`、`std::list`），`container`是该类型的容器对象。

### 元素访问

1. **获取队首元素**：`queueName.front();` 返回队首元素的引用，但不删除该元素。在调用此方法前，应确保队列不为空。
2. **获取队尾元素**：`queueName.back();` 返回队尾元素的引用，但不删除该元素。同样，调用前需确保队列不为空。

### 元素操作

1. **入队**：`queueName.push(element);` 将`element`添加到队尾，队列大小增加 1。
2. **出队**：`queueName.pop();` 移除队首元素，队列大小减少 1。此操作不返回被移除的元素，调用前需确保队列不为空。

### 状态查询

1. **检查队列是否为空**：`queueName.empty();` 如果队列为空返回`true`，否则返回`false`。
2. **获取队列的大小**：`queueName.size();` 返回队列中元素的个数。

### 其他操作

1. **交换两个队列的内容**：`queueName1.swap(queueName2);` 交换`queueName1`和`queueName2`的内容，这两个队列的类型必须相同。也可以使用全局函数`std::swap(queueName1, queueName2);` 实现相同功能。