在 C++ 中，字符串操作主要涉及 C 风格字符串（以空字符 `'\0'` 结尾的字符数组）和 C++ 标准库中的 `std::string` 类。以下是常见的字符串操作：

### C 风格字符串操作

1. **字符串初始化与赋值**
    
    - 直接初始化字符数组：`char str[] = "hello";`
    - 动态分配内存并赋值：`char *str = new char[6]; strcpy(str, "hello");` （需包含 `<cstring>` 头文件）
    
2. **字符串长度计算**
    
    - `strlen(const char *s)`：返回字符串 `s` 的长度（不包括终止空字符）。需 `<cstring>` 头文件。
    
3. **字符串拼接**
    
    - `strcat(char *dest, const char *src)`：将 `src` 字符串追加到 `dest` 字符串的末尾，`dest` 必须有足够的空间。需 `<cstring>` 头文件。
    - `strncat(char *dest, const char *src, size_t n)`：将 `src` 的前 `n` 个字符追加到 `dest` 末尾。需 `<cstring>` 头文件。
    
4. **字符串比较**
    
    - `strcmp(const char *s1, const char *s2)`：比较两个字符串，返回值小于 0 表示 `s1` 小于 `s2`，等于 0 表示相等，大于 0 表示 `s1` 大于 `s2`。需 `<cstring>` 头文件。
    - `strncmp(const char *s1, const char *s2, size_t n)`：比较两个字符串的前 `n` 个字符。需 `<cstring>` 头文件。
    
5. **字符串查找**
    
    - `strchr(const char *s, int c)`：在字符串 `s` 中查找字符 `c` 首次出现的位置，返回指向该位置的指针，若未找到则返回 `nullptr`。需 `<cstring>` 头文件。
    - `strrchr(const char *s, int c)`：在字符串 `s` 中查找字符 `c` 最后一次出现的位置。需 `<cstring>` 头文件。
    - `strstr(const char *haystack, const char *needle)`：在字符串 `haystack` 中查找子字符串 `needle` 首次出现的位置。需 `<cstring>` 头文件。
    
6. **字符串转换**
    
    - `atoi(const char *nptr)`：将字符串转换为 `int` 类型。需 `<cstdlib>` 头文件。
    - `atol(const char *nptr)`：将字符串转换为 `long` 类型。需 `<cstdlib>` 头文件。
    - `atof(const char *nptr)`：将字符串转换为 `double` 类型。需 `<cstdlib>` 头文件。
    - `itoa(int value, char *str, int base)`：将整数 `value` 转换为字符串 `str`，以 `base` 进制表示（非标准库函数，某些编译器提供）。
    
7. **内存操作（与字符串相关）**
    
    - `memcpy(void *dest, const void *src, size_t n)`：从 `src` 复制 `n` 个字节到 `dest`。需 `<cstring>` 头文件。
    - `memmove(void *dest, const void *src, size_t n)`：功能类似 `memcpy`，但能处理重叠内存区域。需 `<cstring>` 头文件。
    

### `std::string` 类操作

1. **字符串初始化与赋值**
    
    - 默认构造：`std::string s;`
    - 用字符串字面量构造：`std::string s("hello");`
    - 用字符个数构造：`std::string s(5, 'a');` （创建包含 5 个 'a' 的字符串）
    - 赋值操作：`s = "world";`
    
2. **字符串长度与容量**
    
    - `s.length()` 或 `s.size()`：返回字符串的长度。
    - `s.capacity()`：返回当前分配的内存可容纳的字符数（不包括终止空字符）。
    - `s.resize(size_t n)`：调整字符串大小为 `n` 个字符，若 `n` 小于当前长度则截断，若大于则用空字符填充。
    - `s.reserve(size_t n)`：预留至少能容纳 `n` 个字符的空间，避免频繁重新分配内存。
    
3. **字符串拼接**
    
    - `s += "suffix";`：在字符串 `s` 末尾追加字符串字面量。
    - `s.append("suffix");`：功能同上，更灵活，可追加多种类型的数据。
    - `s.append(otherString);`：追加另一个 `std::string` 对象。
    
4. **字符串比较**
    
    - `s.compare(otherString)`：比较两个 `std::string` 对象，返回值与 `strcmp` 类似。
    - 可以直接使用关系运算符（`<`, `>`, `<=`, `>=`, `==`, `!=`）进行比较。
    
5. **字符串查找**
    
    - `s.find("substring")`：查找子字符串首次出现的位置，返回索引，若未找到返回 `std::string::npos`。
    - `s.rfind("substring")`：查找子字符串最后一次出现的位置。
    - `s.find_first_of("chars")`：查找 `chars` 中任意字符首次出现的位置。
    - `s.find_last_of("chars")`：查找 `chars` 中任意字符最后一次出现的位置。
    - `s.find_first_not_of("chars")`：查找第一个不在 `chars` 中的字符位置。
    - `s.find_last_not_of("chars")`：查找最后一个不在 `chars` 中的字符位置。
    
6. **字符串提取与修改**
    
    - `s.substr(pos, len)`：返回从位置 `pos` 开始，长度为 `len` 的子字符串。
    - `s.replace(pos, len, "newstring")`：从位置 `pos` 开始，替换 `len` 个字符为 `newstring`。
    - `s.erase(pos, len)`：删除从位置 `pos` 开始的 `len` 个字符。
    - `s.insert(pos, "newstring")`：在位置 `pos` 插入 `newstring`。
    
7. **字符串流操作**
    
    - 包含 `<sstream>` 头文件，可用于字符串与其他数据类型的转换。
    - `std::istringstream`：从字符串读取数据，类似从输入流读取。
    - `std::ostringstream`：向字符串写入数据，类似向输出流写入。
    
8. **遍历字符串**
    - 可以使用迭代器遍历 `std::string`：`for (std::string::iterator it = s.begin(); it != s.end(); ++it)`
    - 基于范围的 `for` 循环：`for (char c : s)` 。