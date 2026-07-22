在 C++ 中，哈希表相关操作主要通过`std::unordered_map`和`std::unordered_set`实现，它们定义在`<unordered_map>`和`<unordered_set>`头文件中。以下是它们常见的操作：

### `std::unordered_map`（用于存储键值对）

#### 声明与初始化

1. **默认初始化**：创建一个空的`std::unordered_map`，`std::unordered_map<Key, Value> mapName;`，其中`Key`是键的类型，`Value`是值的类型。
2. **使用初始化列表初始化**：`std::unordered_map<Key, Value> mapName = {{key1, value1}, {key2, value2},...};`
3. **使用另一个`std::unordered_map`初始化**：`std::unordered_map<Key, Value> mapName(otherMap);`，这里`otherMap`是同类型的`std::unordered_map`对象。

#### 元素访问与修改

1. **通过键访问值**：`mapName[key];`，如果键存在，返回对应的值；如果键不存在，会插入一个默认值的键值对，并返回这个默认值。使用`at(key)`也可通过键访问值，但键不存在时会抛出`std::out_of_range`异常。
2. **赋值**：`mapName[key] = newValue;`，若键存在，更新对应的值；若不存在，则插入新的键值对。

#### 元素操作

1. **插入键值对**：
    
    - `mapName.insert({key, value});`，插入一个新的键值对，若键已存在，插入操作失败，不会修改原有值。
    - `mapName.insert(std::make_pair(key, value));`，功能同上，`std::make_pair`用于创建一个键值对。
    
2. **删除键值对**：`mapName.erase(key);`，删除指定键的键值对，返回删除的元素个数（0 或 1）。也可以通过迭代器删除，`mapName.erase(it);`，`it`是指向要删除元素的迭代器，返回指向下一个元素的迭代器；还可以删除一个范围，`mapName.erase(beginIt, endIt);`，删除从`beginIt`到`endIt`（不包含`endIt`指向的元素）的所有元素，返回指向下一个元素的迭代器。
3. **查找键值对**：`auto it = mapName.find(key);`，查找指定键的元素，若找到，`it`指向该元素；若未找到，`it`等于`mapName.end()`。

#### 状态查询

1. **检查哈希表是否为空**：`mapName.empty();`，如果哈希表为空返回`true`，否则返回`false`。
2. **获取哈希表大小**：`mapName.size();`，返回哈希表中键值对的数量。
3. **获取桶的数量**：`mapName.bucket_count();`，返回哈希表中桶的数量。不同的桶用于存储不同哈希值的元素。
4. **获取某个键所在的桶**：`mapName.bucket(key);`，返回指定键所在的桶的索引。
5. **获取桶中元素的最大数量**：`mapName.max_bucket_count();`，返回哈希表单个桶能容纳的最大元素数量。

#### 哈希策略相关

1. **获取负载因子**：`mapName.load_factor();`，返回哈希表当前的负载因子，负载因子是元素数量与桶数量的比值，反映哈希表的填充程度。
2. **获取最大负载因子**：`mapName.max_load_factor();`，返回哈希表的最大负载因子，当负载因子达到这个值时，哈希表可能会自动调整大小以提高性能。
3. **设置最大负载因子**：`mapName.max_load_factor(factor);`，设置哈希表的最大负载因子为`factor`。

### `std::unordered_set`（用于存储唯一元素）

#### 声明与初始化

1. **默认初始化**：创建一个空的`std::unordered_set`，`std::unordered_set<Key> setName;`，其中`Key`是元素的类型。
2. **使用初始化列表初始化**：`std::unordered_set<Key> setName = {element1, element2,...};`
3. **使用另一个`std::unordered_set`初始化**：`std::unordered_set<Key> setName(otherSet);`，这里`otherSet`是同类型的`std::unordered_set`对象。

#### 元素操作

1. **插入元素**：`setName.insert(element);`，插入一个元素，若元素已存在，插入操作失败，不会重复插入。返回一个`std::pair`，`first`是指向插入元素（或已存在元素）的迭代器，`second`是一个`bool`值，表示插入是否成功。
2. **删除元素**：`setName.erase(element);`，删除指定元素，返回删除的元素个数（0 或 1）。也可通过迭代器删除，`setName.erase(it);`，`it`是指向要删除元素的迭代器，返回指向下一个元素的迭代器；还可以删除一个范围，`setName.erase(beginIt, endIt);`，删除从`beginIt`到`endIt`（不包含`endIt`指向的元素）的所有元素，返回指向下一个元素的迭代器。
3. **查找元素**：`auto it = setName.find(element);`，查找指定元素，若找到，`it`指向该元素；若未找到，`it`等于`setName.end()`。

#### 状态查询

1. **检查哈希表是否为空**：`setName.empty();`，如果哈希表为空返回`true`，否则返回`false`。
2. **获取哈希表大小**：`setName.size();`，返回哈希表中元素的数量。
3. **获取桶的数量**：`setName.bucket_count();`，返回哈希表中桶的数量。
4. **获取某个元素所在的桶**：`setName.bucket(element);`，返回指定元素所在的桶的索引。
5. **获取桶中元素的最大数量**：`setName.max_bucket_count();`，返回哈希表单个桶能容纳的最大元素数量。

#### 哈希策略相关

1. **获取负载因子**：`setName.load_factor();`，返回哈希表当前的负载因子。
2. **获取最大负载因子**：`setName.max_load_factor();`，返回哈希表的最大负载因子。
3. **设置最大负载因子**：`setName.max_load_factor(factor);`，设置哈希表的最大负载因子为`factor`。