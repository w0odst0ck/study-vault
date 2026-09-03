以下是常见的二叉树操作框架：

### 1. 定义二叉树节点结构,创建二叉树节点

1. **C 语言定义二叉树节点结构**：
    
    - 在 C 语言中，我们通常使用结构体来定义二叉树节点。
    

```c
#include <stdio.h>
#include <stdlib.h>

// 定义二叉树节点结构
typedef struct TreeNode {
    int val;
    struct TreeNode *left;
    struct TreeNode *right;
} TreeNode;

// 创建新节点的辅助函数
TreeNode* createNode(int val) {
    TreeNode* newNode = (TreeNode*)malloc(sizeof(TreeNode));
    newNode->val = val;
    newNode->left = NULL;
    newNode->right = NULL;
    return newNode;
}
```

2. **C++ 定义二叉树节点结构**：
    
    - C++ 中可以使用类来定义二叉树节点结构，相比 C 语言结构体更加面向对象。
    

```cpp
#include <iostream>

// 定义二叉树节点结构
class TreeNode {
public:
    int val;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
};

// 创建新节点的辅助函数 
TreeNode* createNode(int val) { 
	return new TreeNode(val); 
}
```

3. **Python 定义二叉树节点结构**：
    
    - 在 Python 中，我们使用类来定义二叉树节点，Python 中没有指针的概念，但通过对象引用来实现类似的功能。
    

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
# 创建新节点的辅助函数
def createNode(val):
    return TreeNode(val)
```

### 2. 插入节点（以二叉搜索树为例）

以下是在二叉搜索树中插入节点的 C、C++ 和 Python 代码：

```c
#include <stdio.h>
#include <stdlib.h>

struct TreeNode* insertNode(struct TreeNode* root, int val) {
    if (root == NULL) {
        struct TreeNode* newNode = (struct TreeNode*)malloc(sizeof(struct TreeNode));
        newNode->val = val;
        newNode->left = newNode->right = NULL;
        return newNode;
    }
    if (val < root->val) {
        root->left = insertNode(root->left, val);
    } else {
        root->right = insertNode(root->right, val);
    }
    return root;
}
```

```cpp
TreeNode* insertNode(TreeNode* root, int val) {
    if (root == nullptr) {
        TreeNode* newNode = new TreeNode(val);
        return newNode;
    }
    if (val < root->val) {
        root->left = insertNode(root->left, val);
    } else {
        root->right = insertNode(root->right, val);
    }
    return root;
}
```

```python
def insertNode(root, val):
    if root is None:
        return TreeNode(val)
    if val < root.val:
        root.left = insertNode(root.left, val)
    else:
        root.right = insertNode(root.right, val)
    return root
```

### 3. 删除节点（以二叉搜索树为例）

```c
#include <stdio.h>
#include <stdlib.h>

struct TreeNode* findMin(struct TreeNode* node) {
    while (node->left!= NULL) {
        node = node->left;
    }
    return node;
}

struct TreeNode* deleteNode(struct TreeNode* root, int key) {
    if (root == NULL) return root;

    if (key < root->val) {
        root->left = deleteNode(root->left, key);
    } else if (key > root->val) {
        root->right = deleteNode(root->right, key);
    } else {
        // 节点有一个或没有子节点
        if (root->left == NULL) {
            struct TreeNode* temp = root->right;
            free(root);
            return temp;
        } else if (root->right == NULL) {
            struct TreeNode* temp = root->left;
            free(root);
            return temp;
        }

        // 节点有两个子节点，找到右子树的最小节点
        struct TreeNode* temp = findMin(root->right);
        root->val = temp->val;
        root->right = deleteNode(root->right, temp->val);
    }
    return root;
}
```

```cpp
TreeNode* findMin(TreeNode* node) {
    while (node->left!= nullptr) {
        node = node->left;
    }
    return node;
}

TreeNode* deleteNode(TreeNode* root, int key) {
    if (root == nullptr) return root;

    if (key < root->val) {
        root->left = deleteNode(root->left, key);
    } else if (key > root->val) {
        root->right = deleteNode(root->right, key);
    } else {
        // 节点有一个或没有子节点
        if (root->left == nullptr) {
            TreeNode* temp = root->right;
            delete root;
            return temp;
        } else if (root->right == nullptr) {
            TreeNode* temp = root->left;
            delete root;
            return temp;
        }

        // 节点有两个子节点，找到右子树的最小节点
        TreeNode* temp = findMin(root->right);
        root->val = temp->val;
        root->right = deleteNode(root->right, temp->val);
    }
    return root;
}
```

```python
def findMin(node):
    while node.left:
        node = node.left
    return node


def deleteNode(root, key):
    if root is None:
        return root

    if key < root.val:
        root.left = deleteNode(root.left, key)
    elif key > root.val:
        root.right = deleteNode(root.right, key)
    else:
        # 节点有一个或没有子节点
        if root.left is None:
            temp = root.right
            return temp
        elif root.right is None:
            temp = root.left
            return temp

        # 节点有两个子节点，找到右子树的最小节点
        temp = findMin(root.right)
        root.val = temp.val
        root.right = deleteNode(root.right, temp.val)
    return root
```

### 4. 查找节点

```c
struct TreeNode* searchNode(struct TreeNode* root, int val) {
    if (root == NULL || root->val == val) {
        return root;
    }
    if (val < root->val) {
        return searchNode(root->left, val);
    }
    return searchNode(root->right, val);
}
```

```cpp
TreeNode* searchNode(TreeNode* root, int val) {
    if (root == nullptr || root->val == val) {
        return root;
    }
    if (val < root->val) {
        return searchNode(root->left, val);
    }
    return searchNode(root->right, val);
}
```

```python
def searchNode(root, val):
    if root is None or root.val == val:
        return root
    if val < root.val:
        return searchNode(root.left, val)
    return searchNode(root.right, val)
```

### 5. 遍历二叉树

#### 前序遍历（根 - 左 - 右）

```c
#include <stdio.h>

void preorderTraversal(struct TreeNode* root) {
    if (root!= NULL) {
        printf("%d ", root->val);
        preorderTraversal(root->left);
        preorderTraversal(root->right);
    }
}
```

```cpp
#include <iostream>
#include <vector>

// 假设TreeNode结构体已经定义
void preorderTraversal(TreeNode* root, std::vector<int>& result) {
    if (root!= nullptr) {
        result.push_back(root->val);
        preorderTraversal(root->left, result);
        preorderTraversal(root->right, result);
    }
}

std::vector<int> preorderTraversal(TreeNode* root) {
    std::vector<int> result;
    preorderTraversal(root, result);
    return result;
}
```

```python
def preorderTraversal(root):
    result = []
    if root:
        result.append(root.val)
        result.extend(preorderTraversal(root.left))
        result.extend(preorderTraversal(root.right))
    return result
```

#### 中序遍历（左 - 根 - 右）

```c
#include <stdio.h>

void inorderTraversal(struct TreeNode* root) {
    if (root!= NULL) {
        inorderTraversal(root->left);
        printf("%d ", root->val);
        inorderTraversal(root->right);
    }
}
```

```cpp
#include <iostream>
#include <vector>

void inorderTraversal(TreeNode* root, std::vector<int>& result) {
    if (root!= nullptr) {
        inorderTraversal(root->left, result);
        result.push_back(root->val);
        inorderTraversal(root->right, result);
    }
}

std::vector<int> inorderTraversal(TreeNode* root) {
    std::vector<int> result;
    inorderTraversal(root, result);
    return result;
}
```

```python
def inorderTraversal(root):
    result = []
    if root:
        result.extend(inorderTraversal(root.left))
        result.append(root.val)
        result.extend(inorderTraversal(root.right))
    return result
```

#### 后序遍历（左 - 右 - 根）

```c
#include <stdio.h>

void postorderTraversal(struct TreeNode* root) {
    if (root!= NULL) {
        postorderTraversal(root->left);
        postorderTraversal(root->right);
        printf("%d ", root->val);
    }
}
```

```cpp
#include <iostream>
#include <vector>

void postorderTraversal(TreeNode* root, std::vector<int>& result) {
    if (root!= nullptr) {
        postorderTraversal(root->left, result);
        postorderTraversal(root->right, result);
        result.push_back(root->val);
    }
}

std::vector<int> postorderTraversal(TreeNode* root) {
    std::vector<int> result;
    postorderTraversal(root, result);
    return result;
}
```

```python
def postorderTraversal(root):
    result = []
    if root:
        result.extend(postorderTraversal(root.left))
        result.extend(postorderTraversal(root.right))
        result.append(root.val)
    return result
```

### 6. 获取二叉树高度

```c
int getHeight(struct TreeNode* root) {
    if (root == NULL) {
        return 0;
    }
    int leftHeight = getHeight(root->left);
    int rightHeight = getHeight(root->right);
    return (leftHeight > rightHeight? leftHeight : rightHeight) + 1;
}
```

```cpp
int getHeight(TreeNode* root) {
    if (root == nullptr) {
        return 0;
    }
    int leftHeight = getHeight(root->left);
    int rightHeight = getHeight(root->right);
    return std::max(leftHeight, rightHeight) + 1;
}
```

```python
def getHeight(root):
    if root is None:
        return 0
    leftHeight = getHeight(root.left)
    rightHeight = getHeight(root.right)
    return max(leftHeight, rightHeight) + 1
```

### 7. 计算二叉树节点数量

```c
// 假设TreeNode结构体已定义
int countNodes(struct TreeNode* root) {
    if (root == NULL) {
        return 0;
    }
    return 1 + countNodes(root->left) + countNodes(root->right);
}
```

```cpp
int countNodes(TreeNode* root) {
    if (root == nullptr) {
        return 0;
    }
    return 1 + countNodes(root->left) + countNodes(root->right);
}
```

```python
def countNodes(root):
    if root is None:
        return 0
    return 1 + countNodes(root.left) + countNodes(root.right)
```

### 8. 计算二叉树叶子节点数量

```c
// 假设TreeNode结构体已经定义
int countLeafNodes(struct TreeNode* root) {
    if (root == NULL) {
        return 0;
    }
    if (root->left == NULL && root->right == NULL) {
        return 1;
    }
    return countLeafNodes(root->left) + countLeafNodes(root->right);
}
```

```cpp
int countLeafNodes(TreeNode* root) {
    if (root == nullptr) {
        return 0;
    }
    if (root->left == nullptr && root->right == nullptr) {
        return 1;
    }
    return countLeafNodes(root->left) + countLeafNodes(root->right);
}
```

```python
# 假设TreeNode类已经定义
def countLeafNodes(root):
    if root is None:
        return 0
    if root.left is None and root.right is None:
        return 1
    return countLeafNodes(root.left) + countLeafNodes(root.right)

```

### 9. 销毁二叉树

```c
void destroyTree(struct TreeNode* root) {
    if (root!= NULL) {
        destroyTree(root->left);
        destroyTree(root->right);
        free(root);
    }
}
```

```cpp
void destroyTree(TreeNode* root) {
    if (root!= nullptr) {
        destroyTree(root->left);
        destroyTree(root->right);
        delete root;
    }
}
```