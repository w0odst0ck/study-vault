下午好！经过上午对 Selenium + CDP 的“开颅手术”，你已经亲眼见过 1688 详情页的 DOM 结构了。现在我们要**把“眼睛看到的”变成“代码写死的”**。

`alibaba_parser.py` 这个文件，本质上是一份 **“1688 详情页的拆迁地图”**。它没有任何机器学习，全是“硬编码”（Hard-coded）的 XPath 路径。今天下午，你就是这份地图的测绘员，不仅要看懂它，还要修补它。

---

# 📖 第二天·下午讲义：攻克 `AlibabaParser` —— 硬编码逻辑与 SKU 拆解术

## 🎯 学习目标（3小时后达成）
1. 彻底看懂 `alibaba_parser.py` 的“套路”：**基于固定 Class 的 XPath 锚点定位**。
2. 亲手为解析器增加一个“材质”提取字段，补齐缺失数据。
3. 揭开 `get_sku_matrix()` 的面纱：理解 `split()` + `zip()` 如何把混乱的字符串变成结构化的规格矩阵。

---

## Part 1：认识 `AlibabaParser` 的“三大硬编码武器”（30 分钟）

打开 `1688/utils/parsers/alibaba_parser.py`，不要被几百行代码吓到。我们只看它的**核心骨架**。

### 1.1 解析器的“瑞士军刀”：`self.xpath()`
在文件里疯狂搜索 `self.xpath`，你会看到这样的代码：

```python
# 典型用法
brand = self.xpath('//div[@class="product-attributes"]//li[@title="品牌"]/span/text()')
detail_images = self.xpath('//div[@class="detail-wrap"]//img/@src')
```

**底层实现（解密）**：
虽然这个库可能用了 `lxml` 或 `BeautifulSoup`，但在爬虫工程师眼里，`self.xpath()` 就是封装好的**快捷取数器**。它的内部逻辑无非是：
1. 接收一个字符串表达式。
2. 在预先加载好的 HTML DOM 树里执行查找。
3. 如果找到，返回文本或属性；如果找不到，返回 `None` 或 `[]`（空列表）。

### 1.2 为什么叫“硬编码”？
因为 `//div[@class="product-attributes"]` 这个路径，是开发者**在 1688 没改版的时候，用肉眼盯着 F12 抄下来的**。
- **优点**：极速、精准、无需额外计算。
- **致命弱点**：一旦 1688 前端重构，把 `product-attributes` 改名为 `module-attributes`，整个解析器立刻瘫痪（这就是为什么有时采集会全盘失败）。

> **今天你的核心任务**：扮演“人肉 XPath 修复器”。

---

## Part 2：核心实战 —— 为解析器新增“材质”字段（90 分钟）

假设你之前的采集里，`材质` 这个字段经常为空或乱码。我们现在给它加一条专线。

### 2.1 第一步：找一份“失败的详情页 HTML”
- 去你的 `data/投光灯/products_detail/{offer_id}/` 目录下，找一个之前解析结果不完整的 `.html` 文件。
- **用记事本（或 VS Code）打开它**。**不要用浏览器双击打开**，因为浏览器会执行 JS 改变 DOM 结构。我们必须看**服务器返回的原始静态源码**。

### 2.2 第二步：手动定位“材质”文本（Ctrl+F）
在记事本里按 `Ctrl+F`，搜索 `材质` 或 `Material`。

**场景 A：找到了“材质”两个字**
假设源码里有这一段：
```html
<div class="attributes-list">
  <dl>
    <dt>品牌</dt><dd>飞利浦</dd>
    <dt>材质</dt><dd>压铸铝 + 钢化玻璃</dd>
    <dt>货号</dt><dd>XL-2025</dd>
  </dl>
</div>
```

**场景 B：只有“规格参数”表格**
```html
<table class="product-properties">
  <tr><td>品牌</td><td>飞利浦</td></tr>
  <tr><td>材质</td><td>压铸铝</td></tr>
</table>
```

### 2.3 第三步：编写专属 XPath（利用上午的“复制”技能）
根据上述结构，我们要写出**既精准又鲁棒**的 XPath：

**针对场景 A（定义列表 dl）**：
```xpath
//dl[dt/text()='材质']/dd/text()
```
解读：找到 `dt` 文本正好是“材质”的 `dl` 标签，取它兄弟 `dd` 里的文本。

**针对场景 B（表格）**：
```xpath
//table[@class="product-properties"]//tr[td[1]/text()='材质']/td[2]/text()
```

### 2.4 第四步：把 XPath 塞进 `alibaba_parser.py`

找到 `alibaba_parser.py` 中的 `get_attributes` 函数（或者搜索 `def parse`）。你通常会发现它返回一个大字典。

**修改策略**：在函数底部，新增一个键值对。

```python
def get_attributes(self):
    # ... 原有代码 ...
    result = {
        'brand': brand,
        'model': model,
        # ... 其他字段
    }
    
    # ========== 新增代码：提取材质 ==========
    # 先写一个稳妥的提取，带 Try-Except 防止崩溃
    material = None
    try:
        # 你刚写的 XPath
        material = self.xpath('//dl[dt/text()="材质"]/dd/text()')
        if isinstance(material, list) and material:
            material = material[0].strip()  # 取第一个，去空格
    except Exception:
        pass  # 找不到就维持 None
    
    result['material'] = material  # 添加新字段
    return result
```

**⚠️ 关键工程原则**：一定要加 `try-except`！因为 1688 某些详情页可能没有“材质”这一行，如果 `self.xpath` 返回 `None` 导致 `.strip()` 报错，整个爬虫就中断了。我们要做到“缺字段不崩”。

### 2.5 第五步：跑个单页测试
不要跑全量。在你的测试脚本里单独加载这个 HTML，调用修改后的解析器，打印 `material` 的值，看能不能打出“压铸铝”。

---

## Part 3：硬骨头 —— 拆解 `get_sku_matrix()` 的字符串魔术（60 分钟）

这个函数是整个解析器里最“算法向”的部分。1688 的 SKU（规格）在源码里通常不是漂亮的 JSON，而是一坨用 **`;`**、**`:`**、**`,`** 拼凑的字符串。

### 3.1 原始数据的模样（从 1688 源码里扒出来）
假设 `alibaba_parser.py` 通过 XPath 拿到了一段文本：
```text
"颜色:红色,蓝色,绿色;尺码:S,M,L;功率:10W,20W"
```

### 3.2 魔法步骤拆解（这是重点！）

**Step 1：按 `;` 拆分规格组**
```python
raw = "颜色:红色,蓝色,绿色;尺码:S,M,L;功率:10W,20W"
groups = raw.split(';')
print(groups)
# 输出: ['颜色:红色,蓝色,绿色', '尺码:S,M,L', '功率:10W,20W']
```

**Step 2：按 `:` 拆出“键”和“值字符串”**
```python
parsed_specs = []
for group in groups:
    key, values_str = group.split(':')
    values_list = values_str.split(',')  # 再按逗号拆成列表
    parsed_specs.append({
        'key': key,
        'values': values_list
    })
# 现在 parsed_specs = [
#   {'key': '颜色', 'values': ['红色','蓝色','绿色']},
#   {'key': '尺码', 'values': ['S','M','L']},
#   {'key': '功率', 'values': ['10W','20W']}
# ]
```

**Step 3：生成笛卡尔积（SKU 矩阵的核心逻辑）**
有了上述规格，需要组合出所有可能的 SKU（比如 `红色-S-10W`）。
这里通常用到 Python 的 `itertools.product`（但很多老脚本喜欢用嵌套循环）。

```python
import itertools

keys = [item['key'] for item in parsed_specs]  # ['颜色', '尺码', '功率']
values_list = [item['values'] for item in parsed_specs]  # [['红色','蓝色'], ['S','M','L'], ['10W','20W']]

# product 生成笛卡尔积
for combination in itertools.product(*values_list):
    # combination 举例: ('红色', 'S', '10W')
    # 用 zip 把键和值捏在一起
    sku_detail = dict(zip(keys, combination))
    print(sku_detail)
    # 输出: {'颜色': '红色', '尺码': 'S', '功率': '10W'}
```

### 3.3 关键配角：`zip()` 的妙用
在你的项目里，你可能还会看到这种写法：
```python
spec_names = ['颜色', '尺码']
spec_values = [['红','蓝'], ['S','M']]
# 如果已经拿到了一个具体的组合 (红, S)
combination = ('红', 'S')
sku_dict = dict(zip(spec_names, combination))
# 结果: {'颜色': '红', '尺码': 'S'}
```
**`zip` 就像一个拉链**，把两个列表按索引一一配对。这对于拼接 SKU 的“属性名”和“属性值”至关重要。

### 3.4 如果解析器里还藏了“价格”和“库存”怎么办？
1688 的 SKU 有时会附带价格。假设还有两个平行列表：
```text
prices = ['100', '120', '100']  # 对应每个 SKU
stocks = ['999', '0', '500']
```
那代码里经常会用 **`for i, sku in enumerate(sku_list)`**，然后用 `prices[i]` 去匹配。或者直接用 `zip(sku_list, prices, stocks)` 一次性打包。

---

## 📌 下午 3 小时后的产出物清单

1. **[✅] 加固后的 `alibaba_parser.py`**：成功添加了 `material`（材质）字段提取逻辑，代码加入了错误处理（Try-Except）。
2. **[✅] 一个成功的单页测试结果**：你手里那份“失败详情页”现在能正确输出材质了。
3. **[✅] 一张手撕 SKU 的流程图**：在你笔记里画一下 `字符串.split(';')` → `split(':')` → `split(',')` → `itertools.product` → `zip` 的流转过程。

---

## 🚨 翻车预警（改代码时的常见症状）

| 现象 | 原因 | 急救方案 |
| :--- | :--- | :--- |
| 添加 XPath 后跑出 `None`，但明明网页里有“材质” | 你查看的是 **浏览器动态渲染后** 的 DOM（F12），但解析器读取的是 **原始 HTML 源码（Ctrl+U）**。 | 回到记事本看源码，源码里的 class 可能跟 F12 里不一样（因为 JS 改了）。以 **Ctrl+U 的源码** 为准。 |
| 报错 `IndexError: list index out of range` | `split(':')` 只拆出了 1 段（说明原始数据格式变了）。 | 打印 `raw` 变量看看实际内容，如果变成了 JSON，那可能需要换 `json.loads` 而不是字符串切分。 |
| 修改后整个脚本跑不动，报语法错误 | 可能是中文字符（材质）写进了 Python 文件，但文件头没有 `# -*- coding: utf-8 -*-`。 | 确保 `material` 等中文字符串在代码里加了 `u"材质"` 或文件首行声明编码。 |

---

晚上我们将进入 **`subprocess` 与资源下载（aria2c）** 的世界，看看解析出来的图片 URL 是怎么被 Python 扔给外部工具批量拉取的。你已经成功跨过了爬虫工程里最恶心的“字段提取沼泽地”，下午的硬仗打得漂亮！如果你在添加“材质”时卡在 XPath 上，把那段 HTML 源码贴出来，我帮你写一条一击必中的规则。