完美！上午我们建立了“DOM 树”和“渲染流水线”的认知，下午直接进入 **“代码实战”** 与 **“字节级调试”**。你懂 Pandas 和 Numpy，这让你在理解 `DataFrame` 构造时毫无压力，我们把 4 小时拆成 **编码原理（2h）** + **BS4 拆解（2h）**，全程高能实操。

---

# 📖 第一天·下午讲义：解码 `02_parse.py` —— 编码战争与 DOM 狩猎

## 🎯 学习目标（4小时后达成）
1. 彻底看透 `bytes` ↔ `str` 转换，面对乱码能秒级定位是 `decode` 环节还是 `print` 环节出错。
2. 能独立在 Jupyter Notebook 中交互式调试 `BeautifulSoup`，不再依赖“盲写脚本 + 跑全量”。
3. 精准区分 `.text`、`.string`、`.get('data-xxx')`、`.attrs` 的返回类型。

---

## Part 1：编码深潜 —— 攻克 `response.content.decode('gbk')`（2 小时）

### 1.1 先做“破坏性实验”（20 分钟）
打开你的 `pipeline/02_parse.py`，找到读取 HTML 的那几行（大概是 `with open` 或 `requests.get` 后接 `.content`）。

**原代码逻辑（正确）**：
```python
# 假设 html_bytes 是从文件或网络读取的 bytes
html_bytes = open(file_path, 'rb').read()  # 注意 'rb' 模式
soup = BeautifulSoup(html_bytes.decode('gbk'), 'lxml')
```

**你的任务（故意搞破坏）**：
把这行改成 `.decode('utf-8')`，然后运行 `run1.py --cat 投光灯`。

**预期灾难现场**：
- 如果运气好（纯英文数字多），会看到一堆像 `çƒæŠ•å…‰ç¯®` 的“锟斤拷”风格乱码。
- 如果运气不好，Python 直接抛出 **`UnicodeDecodeError: 'utf-8' codec can't decode byte 0xcd in position 0: invalid continuation byte`**。

> **🔥 底层原理推导**：`0xCD 0xB6` 在 GBK 里是两个字节构成一个汉字“投”。而 UTF-8 规定中文字符必须占 3~4 个字节。当 Python 的 `utf-8` 解码器读到 `0xCD` 时，它期待接下来的字节是 `0x80-0xBF` 范围，结果看到了 `0xB6`（不符合规则），立刻报错。这就是字节流（Byte Stream）与编码方案（Encoding Scheme）的“契约破裂”。

---

### 1.2 理解 `bytes` 与 `str` 的“楚河汉界”（40 分钟）
打开你的 Jupyter Notebook，新建一个 Cell，逐行运行以下代码，亲眼观察底层字节：

```python
# 实验 1：看透中文字符的字节本质
text = "投光灯"

# 编码为 GBK（1688 的母语）
gbk_bytes = text.encode('gbk')
print(f"GBK 字节: {gbk_bytes}")  
# 输出: b'\xcd\xb6\xb9\xe2\xb5\xc6'（注意每个汉字 2 字节）

# 编码为 UTF-8（全球通用）
utf8_bytes = text.encode('utf-8')
print(f"UTF-8 字节: {utf8_bytes}")  
# 输出: b'\xe6\x8a\x95\xe5\x85\x89\xe7\x81\xaf'（每个汉字 3 字节）

# 实验 2：解码时的“密钥”必须匹配
print(gbk_bytes.decode('gbk'))   # 正常打印 "投光灯"
# print(gbk_bytes.decode('utf-8')) # 如果取消注释，必报 UnicodeDecodeError
```

**爬虫工程启示**：
- **1688 页面返回的原始 `bytes` 是 GBK**，你的 `decode('gbk')` 就是“翻译密钥”。一旦搞错，整棵 DOM 树的文本节点全会变成无意义字符，后续 `find_all('div', string='投光灯')` 永远匹配不上。
- **`BeautifulSoup` 的万能补救**：如果你实在不确定编码，可以不在 `decode` 环节处理，直接写 `soup = BeautifulSoup(html_bytes, 'lxml')`，BS4 内部会调用 `chardet` 自动探测编码（但会消耗额外性能，且对 1688 的 GBK 偶尔误判）。

---

### 1.3 实战：在你的 `02_parse.py` 里增加“编码防御”（60 分钟）
打开你的代码，找到 `parse_html` 函数，我们给它加一道保险：

```python
import chardet  # 需要 pip install chardet

def safe_decode(html_bytes):
    # 1. 先尝试用 GBK 硬解码（最快）
    try:
        return html_bytes.decode('gbk')
    except UnicodeDecodeError:
        # 2. 如果报错，用 chardet 自动识别（兜底）
        result = chardet.detect(html_bytes)
        encoding = result['encoding'] or 'utf-8'
        print(f"⚠️ 检测到非GBK编码：{encoding}，尝试解码...")
        return html_bytes.decode(encoding)
```

**任务**：把这段代码插入 `02_parse.py`，然后把原来写死的 `decode('gbk')` 替换成 `safe_decode` 调用。运行一遍，你会发现绝大多数 1688 页面依然走 GBK 分支，但你的脚本现在能兼容其他平台的 HTML 了——这是工程师思维的“防御性编程”。

---

## Part 2：在 Jupyter Notebook 里拆解 BeautifulSoup（2 小时）

### 2.1 为什么要在 Jupyter 里做？（15 分钟）
在 `.py` 脚本里改一行、跑一遍全流程太慢了。**Jupyter 的交互式 Cell 允许你把 `soup` 对象存在内存里，反复用不同选择器“钓”数据**，直到你找到最精准的定位规则，再把最终版本拷贝回 `02_parse.py`。

---

### 2.2 搭建你的“BS4 解剖台”（30 分钟）
新建一个 Jupyter Notebook，命名为 `debug_1688_parser.ipynb`。输入以下**常驻内存的加载代码**：

```python
from bs4 import BeautifulSoup
import pandas as pd
import os

# 1. 加载一个 1688 搜索页的本地 HTML（你之前油猴下载的）
# 注意：这里读取模式用 'rb' 拿 bytes，然后交给 BeautifulSoup 自动处理编码，或者手动 decode('gbk')
html_path = 'data/投光灯/page_1.html'  # 改成你实际的文件名

with open(html_path, 'rb') as f:
    raw_bytes = f.read()

# 技巧：这里我们故意不 decode，直接喂 bytes，让 BS4 自己猜（但你心里清楚它是 GBK）
soup = BeautifulSoup(raw_bytes, 'lxml')  # lxml 解析器比 html.parser 快 10 倍

print(f"✅ 页面标题: {soup.title.text}")
print(f"✅ 页面共有 {len(soup.find_all())} 个节点")  # 感受 DOM 树规模
```

---

### 2.3 狩猎“17 个字段”——手把手找“年销量”和“回头率”（60 分钟）

1688 的页面结构会变，但方法论永恒。我们不背 XPath，而是学**“特征定位法”**。

**步骤 1：先定位所有商品卡片（Container）**
在 Jupyter 里输入：
```python
# 方法 A：根据 class（1688 通常用 'offer-item' 或 'smb-common-ui'）
items = soup.find_all('div', class_='offer-item')  
print(f"找到 {len(items)} 个商品卡片")

# 如果上面输出 0，说明 class 名字变了，用方法 B：找包含特定属性的 div
items = soup.find_all('div', attrs={'data-trace-id': True})  # 找所有带 data-trace-id 的 div
print(f"用 data-trace-id 找到 {len(items)} 个卡片")
```

**步骤 2：解剖第一个卡片的所有属性（关键技巧）**
```python
first_item = items[0]

# 打印这个卡片的所有 HTML（太长了，只打前 1000 字符）
# print(first_item.prettify()[:1000]) 

# 🔥 核心大招：打印这个标签上的所有 data-* 属性
print("【该卡片上的自定义属性】")
for key, value in first_item.attrs.items():
    if key.startswith('data-'):
        print(f"  {key}: {value}")
```

你会看到类似 `data-repurchase-rate="35%"` 或 `data-total-sales="1200件"` 的输出。**这就是“回头率”和“年销量”最干净的来源！** 它们不在文本节点里，而是作为 `div` 标签的属性存在。

**步骤 3：提取具体值的方法对比**
```python
# 正确姿势（属性提取）
repurchase = first_item.get('data-repurchase-rate', '0%')
sales = first_item.get('data-sales-volume', '0')

# 错误姿势（试图用 .text 去拿属性——拿不到的）
# repurchase_wrong = first_item.find('data-repurchase-rate')  # 这会报错

print(f"回头率: {repurchase} (类型: {type(repurchase)})")  # 注意，get 返回的是字符串！
print(f"年销量: {sales}")
```

**步骤 4：如果属性里没有，再去文本节点里捞（兜底方案）**
万一 `data-repurchase-rate` 为空，说明数据在子标签里：
```python
# 在 first_item 内部搜索包含“回头率”文本的节点
rate_tag = first_item.find(string=lambda t: t and '回头率' in t)
if rate_tag:
    # 找到它的父级兄弟节点提取数值
    parent = rate_tag.parent
    value_tag = parent.find('span', class_='rate-value')
    if value_tag:
        print(f"从文本节点捞到的回头率: {value_tag.text}")
```

---

### 2.4 批量验证 + 构造 DataFrame（30 分钟）
在 Jupyter 里跑通单个字段后，直接批量生成预览 DataFrame：

```python
data_rows = []
for item in items[:10]:  # 只取前 10 个测试
    row = {
        'title': item.find('a', class_='title').text.strip() if item.find('a', class_='title') else None,
        'price': item.get('data-price', ''),
        'shop_name': item.get('data-shop-name', ''),
        'repurchase_rate': item.get('data-repurchase-rate', ''),
        'yearly_sales': item.get('data-total-sales', ''),
    }
    data_rows.append(row)

df_preview = pd.DataFrame(data_rows)
print(df_preview)
```

**检查输出**：
- 如果 `title` 列全是乱码 → 说明你的 `BeautifulSoup` 没正确识别编码（回头检查 `raw_bytes` 的 `decode`）。
- 如果 `repurchase_rate` 全是空值 → 说明属性名猜错了，回到 `first_item.attrs` 的输出结果里复制精确的键名（比如可能是 `data-repurchase` 而不是 `data-repurchase-rate`）。

---

## 📌 下午 4 小时后的产出物清单
1. **加固后的 `02_parse.py`**：加入了 `safe_decode` 自动兜底逻辑。
2. **`debug_1688_parser.ipynb`**：一个可复用的交互式解剖工具，以后遇到任何新品类（比如“筒灯”），只需把 HTML 拖进来改个路径，分分钟摸清新页面的字段位置。
3. **手写笔记**：你所在 1688 版本的“年销量”和“回头率”到底来自 `data-xxx` 还是 `div.text`（记下来，因为 1688 大促期间会改版，留着作为历史参照）。

---

## 🚨 常见 Debug 场景（如果代码报错）

| 报错信息 | 原因 | 解决方案 |
| :--- | :--- | :--- |
| `AttributeError: 'NoneType' object has no attribute 'text'` | `find` 没找到元素，返回了 `None` | 改用 `if tag:` 判断，或用 `tag.text if tag else ""` |
| `KeyError: 'data-repurchase-rate'` | 属性名拼写错误或不存在 | 用 `.get()` 代替 `[]`，或者先去 `attrs` 字典里看一眼真实键名 |
| `UnicodeEncodeError` 在打印时 | Windows 终端不支持 GBK 显示 | 在代码头加 `import sys; sys.stdout.reconfigure(encoding='utf-8')` |

---

**今晚的过渡作业**：打开你的 `03_clean.py`，看看里面用 Pandas 的 `drop_duplicates` 和 `fillna` 时，有没有因为“编码问题”导致同一商品被误判为不同商品（比如乱码导致去重失效）。明天我们将进入 **Selenium 操控 Chrome** 的动态渲染世界！有任何 Jupyter 跑不通的地方，把报错截图发我，我陪你改到通。