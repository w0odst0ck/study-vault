在 C 语言中，虽然没有像 C++ `std::stack` 那样的标准库容器，但可以通过自定义数据结构和函数来实现栈的功能。以下是一个基于数组或链表实现栈的常见操作框架：

### 基于数组实现栈

1. **栈的定义与初始化**
    
    - **定义栈的结构体**：
        
        ```c
        typedef struct Stack {
            int *data;  // 用于存储栈中元素的数组
            int top;    // 栈顶指针，指示栈顶元素位置
            int capacity; // 栈的容量
        } Stack;
        ```
        
    - **初始化栈**：分配内存空间给存储元素的数组，初始化栈顶指针和容量。
        
        ```c
        Stack* createStack(int capacity) {
            Stack *stack = (Stack*)malloc(sizeof(Stack));
            stack->data = (int*)malloc(capacity * sizeof(int));
            stack->top = -1;
            stack->capacity = capacity;
            return stack;
        }
        ```
        
    
2. **入栈操作**
    
    - **检查栈是否已满**：若栈顶指针等于容量减 1，则栈满，返回相应错误提示。
    - **将元素压入栈顶**：栈顶指针加 1，将元素存入栈顶位置。
        
        ```c
        void push(Stack *stack, int value) {
            if (stack->top == stack->capacity - 1) {
                // 处理栈满情况，如打印错误信息
                return;
            }
            stack->data[++(stack->top)] = value;
        }
        ```
        
    
3. **出栈操作**
    
    - **检查栈是否为空**：若栈顶指针为 -1，则栈空，返回相应错误提示。
    - **弹出栈顶元素**：获取栈顶元素，栈顶指针减 1。
        
        ```c
        int pop(Stack *stack) {
            if (stack->top == -1) {
                // 处理栈空情况，如打印错误信息并返回特定值
                return -1; // 假设 -1 表示错误
            }
            return stack->data[(stack->top)--];
        }
        ```
        
    
4. **获取栈顶元素**
    
    - **检查栈是否为空**：若栈空，返回相应错误提示。
    - **返回栈顶元素**：不改变栈顶指针。
        
        ```c
        int peek(Stack *stack) {
            if (stack->top == -1) {
                // 处理栈空情况，如打印错误信息并返回特定值
                return -1; // 假设 -1 表示错误
            }
            return stack->data[stack->top];
        }
        ```
        
    
5. **检查栈是否为空**
    
    - **判断栈顶指针的值**：若栈顶指针为 -1，返回 1（表示空），否则返回 0（表示非空）。
        
        ```c
        int isEmpty(Stack *stack) {
            return stack->top == -1;
        }
        ```
        
    
6. **获取栈的大小**
    
    - **返回栈顶指针加 1 的值**：因为栈顶指针从 -1 开始，加 1 后即为栈中元素个数。
        
        ```c
        int size(Stack *stack) {
            return stack->top + 1;
        }
        ```
        
    
7. **销毁栈**
    
    - **释放存储元素的数组所占用的内存**：
    - **释放栈结构体所占用的内存**：
        
        ```c
        void destroyStack(Stack *stack) {
            free(stack->data);
            free(stack);
        }
        ```
        
    

### 基于链表实现栈

1. **栈节点定义与栈的初始化**
    
    - **定义栈节点的结构体**：
        
        ```c
        typedef struct StackNode {
            int data;
            struct StackNode *next;
        } StackNode;
        
        typedef struct Stack {
            StackNode *top;
        } Stack;
        ```
        
    - **初始化栈**：将栈顶指针设为 NULL。
        
        ```c
        Stack* createStack() {
            Stack *stack = (Stack*)malloc(sizeof(Stack));
            stack->top = NULL;
            return stack;
        }
        ```
        
    
2. **入栈操作**
    
    - **创建新节点**：分配内存给新节点，将元素存入新节点。
    - **将新节点插入栈顶**：新节点的 next 指针指向当前栈顶，更新栈顶指针为新节点。
        
        ```c
        void push(Stack *stack, int value) {
            StackNode *newNode = (StackNode*)malloc(sizeof(StackNode));
            newNode->data = value;
            newNode->next = stack->top;
            stack->top = newNode;
        }
        ```
        
    
3. **出栈操作**
    
    - **检查栈是否为空**：若栈顶指针为 NULL，则栈空，返回相应错误提示。
    - **弹出栈顶元素**：保存栈顶元素，保存栈顶节点指针，更新栈顶指针为栈顶节点的下一个节点，释放栈顶节点内存，返回保存的栈顶元素。
        
        ```c
        int pop(Stack *stack) {
            if (stack->top == NULL) {
                // 处理栈空情况，如打印错误信息并返回特定值
                return -1; // 假设 -1 表示错误
            }
            int popped = stack->top->data;
            StackNode *temp = stack->top;
            stack->top = stack->top->next;
            free(temp);
            return popped;
        }
        ```
        
    
4. **获取栈顶元素**
    
    - **检查栈是否为空**：若栈空，返回相应错误提示。
    - **返回栈顶元素**：不改变栈顶指针。
        
        ```c
        int peek(Stack *stack) {
            if (stack->top == NULL) {
                // 处理栈空情况，如打印错误信息并返回特定值
                return -1; // 假设 -1 表示错误
            }
            return stack->top->data;
        }
        ```
        
    
5. **检查栈是否为空**
    
    - **判断栈顶指针的值**：若栈顶指针为 NULL，返回 1（表示空），否则返回 0（表示非空）。
        
        ```c
        int isEmpty(Stack *stack) {
            return stack->top == NULL;
        }
        ```
        
    
6. **获取栈的大小**
    
    - **遍历链表并计数**：从栈顶开始，逐个遍历节点，直到节点为 NULL，每遍历一个节点，计数器加 1，返回计数器的值。
        
        ```c
        int size(Stack *stack) {
            int count = 0;
            StackNode *current = stack->top;
            while (current != NULL) {
                count++;
                current = current->next;
            }
            return count;
        }
        ```
        
    
7. **销毁栈**
    
    - **遍历链表并释放每个节点的内存**：从栈顶开始，逐个释放节点内存，更新栈顶指针为下一个节点，直到所有节点都被释放。
    - **释放栈结构体所占用的内存**：
        
        ```c
        void destroyStack(Stack *stack) {
            StackNode *current = stack->top;
            StackNode *next;
            while (current != NULL) {
                next = current->next;
                free(current);
                current = next;
            }
            free(stack);
        }
        ```