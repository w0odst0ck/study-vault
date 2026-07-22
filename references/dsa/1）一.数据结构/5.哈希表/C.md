在 C 语言中没有标准库提供哈希表实现，但可以通过自定义数据结构和函数来构建哈希表。以下是一个简单哈希表框架的常见操作：

### 1. 定义哈希表结构

首先需要定义哈希表的结构，通常包括一个数组用于存储键值对，以及哈希表的大小。还可以定义一个节点结构来表示每个键值对。

```c
// 定义哈希表节点
typedef struct HashNode {
    char *key;
    void *value;
    struct HashNode *next;
} HashNode;

// 定义哈希表
typedef struct HashTable {
    HashNode **table;
    int size;
} HashTable;
```

### 2. 初始化哈希表

初始化哈希表时，需要分配内存给哈希表结构以及存储节点的数组，并将数组元素初始化为 `NULL`。

```c
HashTable* createHashTable(int initialSize) {
    HashTable *hashTable = (HashTable*)malloc(sizeof(HashTable));
    hashTable->size = initialSize;
    hashTable->table = (HashNode**)malloc(initialSize * sizeof(HashNode*));
    for (int i = 0; i < initialSize; i++) {
        hashTable->table[i] = NULL;
    }
    return hashTable;
}
```

### 3. 哈希函数

哈希函数用于将键映射到哈希表的索引。一个简单的哈希函数可以基于键的字符编码求和并对哈希表大小取模。

```c
unsigned long hashFunction(const char *key, int tableSize) {
    unsigned long hash = 0;
    while (*key) {
        hash += *key++;
    }
    return hash % tableSize;
}
```

### 4. 插入键值对

插入操作首先计算键的哈希值，找到对应的桶（数组位置）。如果桶为空，直接插入新节点；如果桶不为空，遍历链表找到合适位置插入，避免键冲突。

```c
void insert(HashTable *hashTable, const char *key, void *value) {
    unsigned long index = hashFunction(key, hashTable->size);
    HashNode *node = hashTable->table[index];
    while (node) {
        if (strcmp(node->key, key) == 0) {
            // 键已存在，更新值
            node->value = value;
            return;
        }
        node = node->next;
    }
    // 键不存在，插入新节点
    HashNode *newNode = (HashNode*)malloc(sizeof(HashNode));
    newNode->key = strdup(key);
    newNode->value = value;
    newNode->next = hashTable->table[index];
    hashTable->table[index] = newNode;
}
```

### 5. 查询值

查询操作同样计算键的哈希值，找到对应的桶，然后遍历链表查找键，若找到则返回对应的值。

```c
void* search(HashTable *hashTable, const char *key) {
    unsigned long index = hashFunction(key, hashTable->size);
    HashNode *node = hashTable->table[index];
    while (node) {
        if (strcmp(node->key, key) == 0) {
            return node->value;
        }
        node = node->next;
    }
    return NULL; // 未找到
}
```

### 6. 删除键值对

删除操作先找到键所在的桶，然后遍历链表找到要删除的节点，调整链表结构并释放节点内存。


```c
void deleteKey(HashTable *hashTable, const char *key) {
    unsigned long index = hashFunction(key, hashTable->size);
    HashNode *prev = NULL;
    HashNode *node = hashTable->table[index];
    while (node) {
        if (strcmp(node->key, key) == 0) {
            if (prev) {
                prev->next = node->next;
            } else {
                hashTable->table[index] = node->next;
            }
            free(node->key);
            free(node);
            return;
        }
        prev = node;
        node = node->next;
    }
}
```

### 7. 销毁哈希表

销毁哈希表时，需要释放每个节点的内存以及哈希表结构本身的内存。

```c
void destroyHashTable(HashTable *hashTable) {
    for (int i = 0; i < hashTable->size; i++) {
        HashNode *node = hashTable->table[i];
        while (node) {
            HashNode *next = node->next;
            free(node->key);
            free(node);
            node = next;
        }
    }
    free(hashTable->table);
    free(hashTable);
}
```

上述框架提供了一个基本的哈希表实现，包括初始化、插入、查询、删除和销毁等操作。在实际应用中，可能需要根据具体需求进一步优化，比如改进哈希函数以减少冲突，或者采用更复杂的冲突解决策略。