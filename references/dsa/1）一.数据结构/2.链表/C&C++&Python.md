### 单链表

1. **节点定义**
    
    - 定义一个结构体来表示链表节点，结构体中包含数据成员和指向下一个节点的指针成员。例如：
    	
	```c
// 定义单链表节点结构体
typedef struct ListNode {
    int data; // 节点存储的数据，这里假设为整型，实际可根据需求更改
    struct ListNode *next; // 指向下一个节点的指针
} ListNode;
	```
    
    ```cpp
    template <typename T>
    struct ListNode {
        T data;
        ListNode<T>* next;
        ListNode(const T& value) : data(value), next(nullptr) {}
    };
    ```

	```python
	class ListNode:
	    def __init__(self, val=0, next=None):
	        self.val = val
	        self.next = next
	```


在这个定义中：
1. **链表初始化**
    
    - 创建一个链表头指针，通常初始化为 `nullptr`，表示空链表。例如：`ListNode<T>* head = nullptr;`
    
2. **插入节点**
    
    - **头插法**：创建新节点，将新节点的 `next` 指针指向原头节点，然后更新头指针指向新节点。
    - **尾插法**：遍历链表找到尾节点（即 `next` 为 `nullptr` 的节点），创建新节点，将尾节点的 `next` 指针指向新节点。
    - **在指定节点后插入**：找到指定节点，创建新节点，将新节点的 `next` 指针指向指定节点的 `next`，然后将指定节点的 `next` 指针指向新节点。
    
3. **删除节点**
    
    - **删除头节点**：保存头节点指针，将头指针更新为头节点的 `next`，然后释放头节点内存。
    - **删除指定节点**：遍历链表找到指定节点的前一个节点，将前一个节点的 `next` 指针指向指定节点的 `next`，然后释放指定节点内存。
    - **删除尾节点**：遍历链表找到尾节点的前一个节点，将其 `next` 指针设为 `nullptr`，然后释放尾节点内存。
    
4. **查找节点**
    
    - 从链表头开始，逐个比较节点的数据与目标数据，若相等则返回该节点指针，否则继续遍历，直到链表结束（节点为 `nullptr`），若未找到则返回 `nullptr`。
    
5. **遍历链表**
    
    - 使用一个指针从链表头开始，通过 `next` 指针依次访问每个节点，直到节点为 `nullptr`。在访问每个节点时可以对节点数据进行相应操作。
    
6. **获取链表长度**
    
    - 从链表头开始遍历，每访问一个节点，长度计数器加 1，直到链表结束，返回计数器的值。
    
7. **链表反转**
    
    - 定义三个指针，分别指向当前节点、前一个节点和后一个节点。遍历链表，在遍历过程中调整节点的 `next` 指针方向，使其指向前一个节点，最终实现链表反转。
    

### 双链表

1. **节点定义**
    
    - 定义一个结构体来表示双链表节点，结构体中除了数据成员，还包含指向前一个节点和后一个节点的指针成员。例如：
	
	```c
	// 定义双链表节点结构体
	typedef struct DoubleListNode {
	    int data; // 假设存储整数，可根据实际需求更改
	    struct DoubleListNode *prev; // 指向前一个节点的指针
	    struct DoubleListNode *next; // 指向后一个节点的指针
	} DoubleListNode;
	```

    ```cpp
    template <typename T>
    struct DoubleListNode {
        T data;
        DoubleListNode<T>* prev;
        DoubleListNode<T>* next;
        DoubleListNode(const T& value) : data(value), prev(nullptr), next(nullptr) {}
    };
    ```
    
    ```python
    class DoubleListNode:
	    def __init__(self, val=0, prev=None, next=None):
	        self.val = val
	        self.prev = prev
	        self.next = next
    ```

1. **链表初始化**
    
    - 创建一个链表头指针和尾指针，通常初始化为 `nullptr`，表示空链表。例如：`DoubleListNode<T>* head = nullptr;` 和 `DoubleListNode<T>* tail = nullptr;`
    
2. **插入节点**
    
    - **头插法**：创建新节点，若链表为空，头指针和尾指针都指向新节点；否则，将新节点的 `next` 指向原头节点，原头节点的 `prev` 指向新节点，然后更新头指针指向新节点。
    - **尾插法**：创建新节点，若链表为空，头指针和尾指针都指向新节点；否则，将新节点的 `prev` 指向原尾节点，原尾节点的 `next` 指向新节点，然后更新尾节点指向新节点。
    - **在指定节点后插入**：找到指定节点，创建新节点，将新节点的 `prev` 指向指定节点，`next` 指向指定节点的 `next`，若指定节点的 `next` 不为 `nullptr`，则将其 `prev` 指向新节点，最后更新指定节点的 `next` 指向新节点。
    - **在指定节点前插入**：找到指定节点，创建新节点，将新节点的 `next` 指向指定节点，`prev` 指向指定节点的 `prev`，若指定节点的 `prev` 不为 `nullptr`，则将其 `next` 指向新节点，最后更新指定节点的 `prev` 指向新节点。
    
3. **删除节点**
    
    - **删除头节点**：保存头节点指针，若头节点的 `next` 不为 `nullptr`，将其 `prev` 设为 `nullptr`，然后更新头指针为头节点的 `next`，释放头节点内存。若链表只有一个节点，头指针和尾指针都设为 `nullptr`。
    - **删除尾节点**：保存尾节点指针，若尾节点的 `prev` 不为 `nullptr`，将其 `next` 设为 `nullptr`，然后更新尾节点为尾节点的 `prev`，释放尾节点内存。若链表只有一个节点，头指针和尾指针都设为 `nullptr`。
    - **删除指定节点**：找到指定节点，若指定节点的 `prev` 不为 `nullptr`，将其 `next` 指向指定节点的 `next`；若指定节点的 `next` 不为 `nullptr`，将其 `prev` 指向指定节点的 `prev`，然后释放指定节点内存。
    
4. **查找节点**
    
    - 与单链表类似，可从链表头或链表尾开始，逐个比较节点的数据与目标数据，若相等则返回该节点指针，否则继续遍历，直到链表结束（头到尾遍历节点为 `nullptr`，尾到头遍历节点为 `nullptr`），若未找到则返回 `nullptr`。
    
5. **遍历链表**
    
    - 可以从链表头开始，通过 `next` 指针依次访问每个节点，直到节点为 `nullptr`；也可以从链表尾开始，通过 `prev` 指针依次访问每个节点，直到节点为 `nullptr`。在访问每个节点时可以对节点数据进行相应操作。
    
6. **获取链表长度**
    
    - 从链表头开始遍历（也可从尾开始），每访问一个节点，长度计数器加 1，直到链表结束，返回计数器的值。
    
7. **链表反转**
    - 从链表头开始遍历，交换每个节点的 `prev` 和 `next` 指针方向，同时更新头指针和尾指针。遍历结束后，链表的方向即被反转。