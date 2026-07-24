#### 数组

1. **声明与初始化**
    
    - **静态数组**：声明特定类型和大小的数组，如`type arrayName[size];`，可同时进行初始化，如`type arrayName[size] = {value1, value2,...};`，若初始化值个数少于数组大小，剩余元素默认初始化。对于整型数组，剩余元素初始化为 0；对于指针数组，初始化为`nullptr`等。
    - **动态数组**：使用`new`运算符在堆上分配内存创建数组，如`type *arrayName = new type[size];`，需手动使用`delete[]`释放内存，即`delete[] arrayName;`。
    
2. **访问元素**
    
    - 通过索引访问数组元素，索引从 0 开始，如`arrayName[index];`，需确保索引在有效范围内（0 到 size - 1），否则会导致未定义行为。
    
3. **数组大小**
    
    - 对于静态数组，可通过`sizeof(arrayName) / sizeof(arrayName[0])`计算数组元素个数。动态数组由于其内存分配的灵活性，需在代码中自行记录数组大小信息。
    
4. **遍历数组**
    
    - 通常使用`for`循环，如`for (int i = 0; i < size; ++i) { /* 访问或操作 arrayName[i] */ }`。也可使用`while`循环实现类似功能。
    
5. **数组赋值**
    
    - 可逐个为数组元素赋值，如`arrayName[i] = value;`。对于同类型数组间的赋值，需逐个元素复制，不能直接用一个数组给另一个数组整体赋值（静态数组）。对于动态数组，可使用`memcpy`函数进行整块内存复制，但需确保目标数组有足够空间，`memcpy(destArray, srcArray, sizeof(type) * size);`（需包含`<cstring>`头文件）。
    
6. **数组插入与删除**
    
    - **插入**：在数组中间插入元素，需将插入位置及之后的元素向后移动，为新元素腾出空间。如要在索引`index`处插入`newValue`，则从数组末尾开始，将`arrayName[size - 1]`到`arrayName[index]`的元素依次向后移动一位，然后`arrayName[index] = newValue;`，同时数组大小加 1（若为动态数组，需重新分配内存）。
    - **删除**：删除数组某位置元素，需将该位置之后的元素向前移动。如删除索引`index`处元素，从`arrayName[index + 1]`开始，将后续元素依次向前移动一位，数组大小减 1（若为动态数组，可考虑重新分配内存以释放多余空间）。
    

#### 向量（`std::vector`）

1. **声明与初始化**
    
    - **默认初始化**：`std::vector<type> vectorName;`，创建一个空向量。
    - **带初始大小初始化**：`std::vector<type> vectorName(size);`，创建一个大小为`size`的向量，元素默认初始化。
    - **带初始大小和初始值初始化**：`std::vector<type> vectorName(size, value);`，创建一个大小为`size`的向量，所有元素初始化为`value`。
    - **用初始化列表初始化**：`std::vector<type> vectorName = {value1, value2,...};`。
    - **用其他向量初始化**：`std::vector<type> vectorName(otherVector);` 或 `std::vector<type> vectorName(otherVector.begin(), otherVector.end());`，复制`otherVector`的内容。
    
2. **访问元素**
    
    - **通过索引访问**：`vectorName[index];`，索引从 0 开始，若索引越界，会导致未定义行为。可使用`at(index)`成员函数访问元素，该函数在索引越界时会抛出`std::out_of_range`异常。
    - **访问第一个和最后一个元素**：`vectorName.front();`获取第一个元素，`vectorName.back();`获取最后一个元素。
    
3. **向量大小与容量**
    
    - **大小**：`vectorName.size();`返回向量中当前元素的个数。
    - **容量**：`vectorName.capacity();`返回向量在不重新分配内存的情况下可容纳的最大元素数。
    - **调整大小**：`vectorName.resize(newSize);`调整向量大小为`newSize`，若`newSize`大于当前大小，新元素默认初始化；若`newSize`小于当前大小，超出部分元素被删除。`vectorName.resize(newSize, value);`在调整大小时，用`value`初始化新增元素。
    - **预留空间**：`vectorName.reserve(newCapacity);`预留至少能容纳`newCapacity`个元素的空间，可减少动态内存分配次数，提高性能。
    
4. **遍历向量**
    
    - **使用迭代器**：可使用`for`循环结合迭代器遍历，如`for (auto it = vectorName.begin(); it != vectorName.end(); ++it) { /* 访问或操作 *it */ }`。`begin()`返回指向第一个元素的迭代器，`end()`返回指向最后一个元素之后位置的迭代器。还可使用`rbegin()`和`rend()`进行反向遍历。
    - **基于范围的`for`循环**：`for (const auto& element : vectorName) { /* 访问或操作 element */ }`，更简洁地遍历向量。
    
5. **元素修改与操作**
    
    - **赋值**：可通过索引或迭代器修改元素值，如`vectorName[index] = newValue;` 或 `*it = newValue;`。
    - **添加元素**：
        
        - `vectorName.push_back(value);`在向量末尾添加一个元素，若当前容量不足，会自动重新分配内存并复制原有元素。
        - `vectorName.insert(it, value);`在迭代器`it`指向的位置插入`value`，返回指向新插入元素的迭代器。`vectorName.insert(it, count, value);`插入`count`个`value`。`vectorName.insert(it, otherVector.begin(), otherVector.end());`在`it`位置插入另一个向量的内容。
        
    - **删除元素**：
        
        - `vectorName.pop_back();`删除向量末尾的元素。
        - `vectorName.erase(it);`删除迭代器`it`指向的元素，返回指向被删除元素之后位置的迭代器。`vectorName.erase(beginIt, endIt);`删除从`beginIt`到`endIt`（不包含`endIt`指向的元素）之间的所有元素，返回指向被删除元素之后位置的迭代器。
        
    - **清空向量**：`vectorName.clear();`移除向量中的所有元素，使向量大小变为 0，但容量不变。
    
6. **其他操作**
    - **向量比较**：可使用关系运算符（`==`, `!=`, `<`, `>` 等）按字典序比较两个向量，比较基于元素的比较。
    - **交换向量内容**：`vectorName.swap(otherVector);`交换`vectorName`和`otherVector`的内容。