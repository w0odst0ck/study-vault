在 C 语言中，字符串操作主要围绕以空字符`'\0'`结尾的字符数组展开，这些操作大多定义在`<string.h>`和`<stdlib.h>`头文件中。以下是常见的字符串操作：

### 1. 字符串初始化与赋值

- 直接初始化字符数组：`char str[] = "string literal";`
- 使用`strcpy`函数进行赋值（目标数组需足够大）：`strcpy(destination, source);`，其中`destination`是目标字符数组，`source`是源字符串。需包含`<string.h>`头文件。

### 2. 字符串长度计算

- `strlen(const char *s)`：返回字符串`s`的长度，不包括终止空字符`'\0'`。需`<string.h>`头文件。

### 3. 字符串拼接

- `strcat(char *dest, const char *src)`：将`src`字符串追加到`dest`字符串的末尾，`dest`必须有足够的空间容纳连接后的字符串。需`<string.h>`头文件。
- `strncat(char *dest, const char *src, size_t n)`：将`src`的前`n`个字符追加到`dest`末尾，确保`dest`有足够空间。需`<string.h>`头文件。

### 4. 字符串比较

- `strcmp(const char *s1, const char *s2)`：比较两个字符串`s1`和`s2`。返回值小于 0 表示`s1`小于`s2`，等于 0 表示`s1`等于`s2`，大于 0 表示`s1`大于`s2`。需`<string.h>`头文件。
- `strncmp(const char *s1, const char *s2, size_t n)`：比较`s1`和`s2`的前`n`个字符。需`<string.h>`头文件。

### 5. 字符串查找

- `strchr(const char *s, int c)`：在字符串`s`中查找字符`c`首次出现的位置，返回指向该位置的指针，若未找到则返回`NULL`。需`<string.h>`头文件。
- `strrchr(const char *s, int c)`：在字符串`s`中查找字符`c`最后一次出现的位置。需`<string.h>`头文件。
- `strstr(const char *haystack, const char *needle)`：在字符串`haystack`中查找子字符串`needle`首次出现的位置，返回指向该位置的指针，若未找到则返回`NULL`。需`<string.h>`头文件。

### 6. 字符串转换

- **数值转字符串**：
    
    - `itoa(int value, char *str, int base)`：将整数`value`转换为字符串`str`，以`base`进制表示（某些系统中可能不是标准库函数）。
    - `ltoa(long value, char *str, int base)`：将长整数`value`转换为字符串`str`，以`base`进制表示。
    - `ultoa(unsigned long value, char *str, int base)`：将无符号长整数`value`转换为字符串`str`，以`base`进制表示。
    
- **字符串转数值**：
    
    - `atoi(const char *nptr)`：将字符串转换为`int`类型。需`<stdlib.h>`头文件。
    - `atol(const char *nptr)`：将字符串转换为`long`类型。需`<stdlib.h>`头文件。
    - `atof(const char *nptr)`：将字符串转换为`double`类型。需`<stdlib.h>`头文件。
    

### 7. 内存操作（与字符串相关）

- `memcpy(void *dest, const void *src, size_t n)`：从`src`复制`n`个字节到`dest`，常用于复制字符串或部分字符串。需`<string.h>`头文件。
- `memmove(void *dest, const void *src, size_t n)`：功能与`memcpy`类似，但能处理重叠内存区域。需`<string.h>`头文件。
- `memset(void *s, int c, size_t n)`：将`s`指向的内存区域的前`n`个字节设置为字符`c`，可用于初始化字符串。需`<string.h>`头文件。