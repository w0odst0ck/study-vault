在 Python 中，哈希表主要通过字典（`dict`）来实现。以下是哈希表（字典）框架的常见操作：

### 1. 创建与初始化

- **直接初始化**：使用花括号 `{}` 并在其中指定键值对，如 `hash_table = {'key1': 'value1'}`。
- **使用 `dict()` 函数**：可以通过多种方式使用 `dict()` 函数来创建字典。例如，传入一个包含键值对元组的可迭代对象，如 `dict([('key1', 'value1')])`；或者使用关键字参数，如 `dict(key1='value1')`。

### 2. 访问元素

- **通过键获取值**：使用方括号 `[]` 并传入键，如 `value = hash_table['key']`。如果键不存在，会引发 `KeyError` 异常。
- **使用 `get()` 方法**：`value = hash_table.get('key')`，该方法在键不存在时返回 `None`（也可指定默认返回值，如 `hash_table.get('key', 'default_value')`）。

### 3. 修改元素

- **更新值**：通过键直接赋值来更新对应的值，如 `hash_table['key'] = 'new_value'`。如果键不存在，会创建一个新的键值对。
- **使用 `update()` 方法**：可以使用另一个字典或可迭代对象（包含键值对）来更新当前字典。例如，`hash_table.update({'key2': 'value2'})` 或 `hash_table.update([('key3', 'value3')])`。

### 4. 添加元素

- **直接添加新键值对**：通过给不存在的键赋值来添加新元素，如 `hash_table['new_key'] = 'new_value'`。

### 5. 删除元素

- **使用 `del` 语句**：`del hash_table['key']`，删除指定键及其对应的值。如果键不存在，会引发 `KeyError` 异常。
- **使用 `pop()` 方法**：`value = hash_table.pop('key')`，移除指定键并返回对应的值。如果键不存在，可指定默认返回值避免异常，如 `hash_table.pop('key', 'default_value')`。
- **使用 `popitem()` 方法**：移除并返回一个键值对（通常是最后插入的键值对，在 Python 3.7+ 中字典保持插入顺序）。如果字典为空，会引发 `KeyError` 异常。

### 6. 其他操作

- **获取所有键**：使用 `keys()` 方法，返回一个可迭代对象，包含字典中的所有键，如 `keys = hash_table.keys()`。可以将其转换为列表，如 `list(hash_table.keys())`。
- **获取所有值**：使用 `values()` 方法，返回一个可迭代对象，包含字典中的所有值，如 `values = hash_table.values()`。同样可转换为列表，如 `list(hash_table.values())`。
- **获取所有键值对**：使用 `items()` 方法，返回一个可迭代对象，包含字典中的所有键值对（以元组形式），如 `items = hash_table.items()`。也可转换为列表，如 `list(hash_table.items())`。
- **判断键是否存在**：使用 `in` 关键字，如 `'key' in hash_table`，返回 `True` 或 `False` 表示键是否存在于字典中。
- **获取字典长度**：使用 `len()` 函数，如 `length = len(hash_table)`，返回字典中键值对的数量。
- **清空字典**：使用 `clear()` 方法，如 `hash_table.clear()`，移除字典中的所有元素。