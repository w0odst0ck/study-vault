在 C 语言中没有像 C++ 那样标准的队列库，通常需要自己实现队列数据结构。常见的实现方式有基于数组和基于链表两种，以下分别介绍这两种实现方式下队列的所有操作：

### 基于数组实现队列（循环队列）

1. **队列结构体定义与初始化**
    
    - **定义队列结构体**：
    
```c
typedef struct {
    int *data; // 存储队列元素的数组
    int front; // 队首指针
    int rear;  // 队尾指针
    int capacity; // 队列容量
} Queue;
```

- **初始化队列**：分配内存给存储元素的数组，初始化队首、队尾指针和容量。

```c
Queue* createQueue(int capacity) {
    Queue *queue = (Queue*)malloc(sizeof(Queue));
    queue->data = (int*)malloc(capacity * sizeof(int));
    queue->front = 0;
    queue->rear = 0;
    queue->capacity = capacity;
    return queue;
}
```

2. **入队操作**
    
    - **检查队列是否已满**：通过计算 (`rear + 1) % capacity` 是否等于 `front` 来判断队列是否已满，如果满则返回错误提示或处理方式。
    - **将元素添加到队尾**：将元素存入 `rear` 指向的位置，然后 `rear = (rear + 1) % capacity` 更新队尾指针。
    

```c
void enqueue(Queue *queue, int value) {
    if ((queue->rear + 1) % queue->capacity == queue->front) {
        // 处理队列已满的情况，如打印错误信息
        return;
    }
    queue->data[queue->rear] = value;
    queue->rear = (queue->rear + 1) % queue->capacity;
}
```

3. **出队操作**
    
    - **检查队列是否为空**：如果 `front` 等于 `rear`，则队列空，返回错误提示或处理方式。
    - **移除队首元素**：获取 `front` 指向的元素，然后 `front = (front + 1) % capacity` 更新队首指针。
    

```c
int dequeue(Queue *queue) {
    if (queue->front == queue->rear) {
        // 处理队列空的情况，如打印错误信息并返回特定值
        return -1; // 假设 -1 表示错误
    }
    int dequeued = queue->data[queue->front];
    queue->front = (queue->front + 1) % queue->capacity;
    return dequeued;
}
```

4. **获取队首元素**
    
    - **检查队列是否为空**：若队列空，返回错误提示或处理方式。
    - **返回队首元素**：不改变队首指针，直接返回 `data[front]`。
    

```c
int front(Queue *queue) {
    if (queue->front == queue->rear) {
        // 处理队列空的情况，如打印错误信息并返回特定值
        return -1; // 假设 -1 表示错误
    }
    return queue->data[queue->front];
}
```

5. **检查队列是否为空**
    
    - **判断队首和队尾指针是否相等**：若 `front` 等于 `rear`，返回 1（表示空），否则返回 0（表示非空）。
    

```c
int isQueueEmpty(Queue *queue) {
    return queue->front == queue->rear;
}
```

6. **获取队列的大小**
    
    - **通过队首和队尾指针计算**：返回 `(queue->rear - queue->front + queue->capacity) % queue->capacity`。
    

```c
int queueSize(Queue *queue) {
    return (queue->rear - queue->front + queue->capacity) % queue->capacity;
}
```

7. **销毁队列**
    
    - **释放存储元素的数组所占用的内存**：
    - **释放队列结构体所占用的内存**：
    

```c
void destroyQueue(Queue *queue) {
    free(queue->data);
    free(queue);
}
```

### 基于链表实现队列

1. **队列节点与队列结构体定义及初始化**
    
    - **定义队列节点结构体**：
    

```c
typedef struct QueueNode {
    int data;
    struct QueueNode *next;
} QueueNode;

typedef struct {
    QueueNode *front; // 队首指针
    QueueNode *rear;  // 队尾指针
} Queue;
```

- **初始化队列**：将队首和队尾指针都设为 `NULL`。

```c
Queue* createQueue() {
    Queue *queue = (Queue*)malloc(sizeof(Queue));
    queue->front = NULL;
    queue->rear = NULL;
    return queue;
}
```

2. **入队操作**
    
    - **创建新节点**：分配内存给新节点，将元素存入新节点，新节点 `next` 设为 `NULL`。
    - **将新节点添加到队尾**：如果队列为空，队首和队尾都指向新节点；否则，将队尾节点的 `next` 指向新节点，然后更新队尾指针为新节点。
    

```c
void enqueue(Queue *queue, int value) {
    QueueNode *newNode = (QueueNode*)malloc(sizeof(QueueNode));
    newNode->data = value;
    newNode->next = NULL;
    if (queue->rear == NULL) {
        queue->front = newNode;
        queue->rear = newNode;
    } else {
        queue->rear->next = newNode;
        queue->rear = newNode;
    }
}
```

3. **出队操作**
    
    - **检查队列是否为空**：如果队首指针为 `NULL`，则队列为空，返回错误提示或处理方式。
    - **移除队首元素**：保存队首元素，保存队首节点指针，更新队首指针为队首节点的 `next`，释放队首节点内存，返回保存的队首元素。如果此时队列为空（队首指针变为 `NULL`），同时更新队尾指针为 `NULL`。
    

```c
int dequeue(Queue *queue) {
    if (queue->front == NULL) {
        // 处理队列空的情况，如打印错误信息并返回特定值
        return -1; // 假设 -1 表示错误
    }
    int dequeued = queue->front->data;
    QueueNode *temp = queue->front;
    queue->front = queue->front->next;
    free(temp);
    if (queue->front == NULL) {
        queue->rear = NULL;
    }
    return dequeued;
}
```

4. **获取队首元素**
    
    - **检查队列是否为空**：若队列空，返回错误提示或处理方式。
    - **返回队首元素**：不改变队首指针，直接返回 `front->data`。
    

```c
int front(Queue *queue) {
    if (queue->front == NULL) {
        // 处理队列空的情况，如打印错误信息并返回特定值
        return -1; // 假设 -1 表示错误
    }
    return queue->front->data;
}
```

5. **检查队列是否为空**
    
    - **判断队首指针是否为 `NULL`**：若队首指针为 `NULL`，返回 1（表示空），否则返回 0（表示非空）。
    

```c
int isQueueEmpty(Queue *queue) {
    return queue->front == NULL;
}
```

6. **获取队列的大小**
    
    - **遍历链表并计数**：从队首开始，逐个遍历节点，直到节点为 `NULL`，每遍历一个节点，计数器加 1，返回计数器的值。
    

```c
int queueSize(Queue *queue) {
    int count = 0;
    QueueNode *current = queue->front;
    while (current != NULL) {
        count++;
        current = current->next;
    }
    return count;
}
```

7. **销毁队列**
    
    - **遍历链表并释放每个节点的内存**：从队首开始，逐个释放节点内存，更新队首指针为下一个节点，直到所有节点都被释放。
    - **释放队列结构体所占用的内存**：
    

```c
void destroyQueue(Queue *queue) {
    QueueNode *current = queue->front;
    QueueNode *next;
    while (current != NULL) {
        next = current->next;
        free(current);
        current = next;
    }
    free(queue);
}
```