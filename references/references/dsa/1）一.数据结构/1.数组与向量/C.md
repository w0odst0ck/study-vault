### C 语言数组

1. **声明与初始化**
    
    - **声明**：指定数组类型和大小，格式为 `type arrayName[size];`，其中 `type` 是数组元素的数据类型，`size` 必须是常量表达式。
    - **初始化**：
        
        - 完全初始化：`type arrayName[size] = {value1, value2,..., valueN};`，这里 `N` 等于 `size`，按顺序将值赋给数组元素。
        - 部分初始化：`type arrayName[size] = {value1, value2};`，剩余元素根据数组类型默认初始化，数值类型初始化为 0，字符类型初始化为 `'\0'`，指针类型初始化为 `NULL`。
        - 省略大小初始化：`type arrayName[] = {value1, value2, value3};`，数组大小由初始化列表中的元素个数决定。
        
    
2. **访问元素**
    
    - 通过索引访问，索引从 0 开始，格式为 `arrayName[index];`，`index` 必须在 0 到 `size - 1` 范围内，否则会导致未定义行为。
    
3. **确定数组大小**
    
    - 使用 `sizeof` 运算符，通过 `sizeof(arrayName) / sizeof(arrayName[0])` 计算数组元素的个数。
    
4. **遍历数组**
    
    - 通常使用 `for` 循环，如 `for (int i = 0; i < size; i++) { /* 操作 arrayName[i] */ }`。
    - 也可使用 `while` 循环，如 `int i = 0; while (i < size) { /* 操作 arrayName[i] */ i++; }`。
    
5. **数组赋值**
    
    - 逐个元素赋值：`arrayName[index] = value;`。
    - 对于同类型数组间的赋值，需逐个元素复制，不能直接用一个数组给另一个数组整体赋值。例如，要将 `srcArray` 赋值给 `destArray`，可使用 `for` 循环：`for (int i = 0; i < size; i++) { destArray[i] = srcArray[i]; }`。
    
6. **数组插入与删除**
    
    - **插入**：在数组中间插入元素，需要将插入位置及之后的元素向后移动。例如，要在索引 `index` 处插入 `newValue`，先将 `arrayName[size - 1]` 到 `arrayName[index]` 的元素依次向后移动一位，然后 `arrayName[index] = newValue;`。但要注意数组大小固定，插入后可能需要调整数组大小（如重新分配内存）。
    - **删除**：删除数组某位置元素，需将该位置之后的元素向前移动。例如，删除索引 `index` 处元素，从 `arrayName[index + 1]` 开始，将后续元素依次向前移动一位。同样，数组大小固定，删除后可能需要调整数组大小。
    

### C 语言动态数组

1. **内存分配与初始化**
    
    - 使用 `malloc` 函数分配内存，格式为 `type *arrayName = (type *)malloc(size * sizeof(type));`，`malloc` 函数分配指定字节数的内存，并返回指向该内存起始地址的指针，需进行类型转换。
    - 若要初始化分配的内存，可使用 `calloc` 函数，`type *arrayName = (type *)calloc(size, sizeof(type));`，`calloc` 函数不仅分配内存，还将其初始化为 0。
    
2. **访问元素**
    
    - 同样通过索引访问，格式为 `arrayName[index];`，因为动态数组本质也是指针，索引方式与普通数组相同，但需确保 `index` 在有效范围内。
    
3. **确定数组大小**
    
    - 由于动态数组大小不固定，需要在代码中自行记录数组大小信息。例如，定义一个变量 `int arraySize = size;` 来跟踪数组大小。
    
4. **遍历数组**
    
    - 与普通数组类似，可使用 `for` 循环：`for (int i = 0; i < arraySize; i++) { /* 操作 arrayName[i] */ }`，或 `while` 循环：`int i = 0; while (i < arraySize) { /* 操作 arrayName[i] */ i++; }`。
    
5. **数组扩容与缩容**
    
    - **扩容**：使用 `realloc` 函数，格式为 `arrayName = (type *)realloc(arrayName, newSize * sizeof(type));`，`realloc` 函数尝试重新分配内存块，`newSize` 为新的大小。如果新大小大于原大小，可能会移动内存块并扩展；如果新大小小于原大小，可能会截断内存块。需检查返回指针是否为 `NULL`，以判断内存分配是否成功。
    - **缩容**：原理与扩容类似，只是 `newSize` 小于当前数组大小，使用 `realloc` 调整内存大小。
    
6. **数组赋值**
    
    - 逐个元素赋值：`arrayName[index] = value;`。
    - 可使用 `memcpy` 函数进行整块内存复制（需包含 `<string.h>` 头文件），例如将 `srcArray` 复制到 `destArray`，`memcpy(destArray, srcArray, numElements * sizeof(type));`，其中 `numElements` 是要复制的元素个数。
    
7. **内存释放**
    - 使用 `free` 函数释放动态分配的内存，格式为 `free(arrayName);`，释放后应将指针设置为 `NULL`，防止悬空指针，即 `arrayName = NULL;`。