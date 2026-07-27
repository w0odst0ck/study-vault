# Python 纯手写代码面试卷

# 算法挖掘 纯 Python 手撕代码面试卷

全部**无调包高阶 API**，只用基础 Python/Numpy，面试现场可直接手写，贴合数据挖掘 / 算法岗手撕要求。

## 1. 手撕：类别特征频率编码 标签编码

**题目**
不调用 sklearn，手写实现：标签编码 LabelEncoder、类别特征频率编码。

```python
import numpy as np

# 1. 手写标签编码
def label_encode(cat_list):
    unique_cat = sorted(list(set(cat_list)))
    cat2idx = {cat:i for i, cat in enumerate(unique_cat)}
    return [cat2idx[item] for item in cat_list]

# 2. 手写频率编码
def freq_encode(cat_list):
    # 统计每个类别出现频率
    freq_dict = {}
    for cat in cat_list:
        freq_dict[cat] = freq_dict.get(cat, 0) + 1
    # 转为频率占比
    total = len(cat_list)
    freq_dict = {k: v/total for k,v in freq_dict.items()}
    return [freq_dict[item] for item in cat_list]

# 测试
if __name__ == "__main__":
    data = ["北京","上海","北京","广州","上海","北京"]
    print("标签编码：", label_encode(data))
    print("频率编码：", freq_encode(data))
```

**面试考点**
频率编码能保留类别分布信息，比普通标号更适合树模型；高基数类别常用频率 / 目标均值编码。

---

## 2\. 手撕：手写 TF\-IDF 完整实现

**题目**
不用 sklearn，手写 TF、IDF、TF\-IDF 计算。

```python
import math

# 计算词频TF
def calc_tf(word, doc):
    return doc.count(word) / len(doc)

# 计算逆文档频率IDF
def calc_idf(word, corpus):
    # 包含该词的文档数
    doc_cnt = sum(1 for doc in corpus if word in doc)
    # 平滑避免除0
    return math.log((len(corpus) + 1) / (doc_cnt + 1)) + 1

# 计算单文档TF-IDF
def tf_idf(doc, corpus):
    words = set(doc)
    res = {}
    for word in words:
        tf = calc_tf(word, doc)
        idf = calc_idf(word, corpus)
        res[word] = tf * idf
    return res

# 测试
if __name__ == "__main__":
    corpus = [
        ["机器学习", "算法", "特征工程"],
        ["算法", "挖掘", "聚类"],
        ["RAG", "检索", "算法"]
    ]
    print(tf_idf(corpus[0], corpus))
```

**面试考点**
BM25 是 TF\-IDF 的升级版，解决长文档偏袒、词频无上限问题。

---

## 3\. 手撕：余弦相似度 \+ 向量 TopK 检索

**题目**
手写余弦相似度，实现给定查询向量，从库中召回 TopK 相似向量（RAG 底层基础）。

```python
import numpy as np

# 余弦相似度
def cosine_sim(vec1, vec2):
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot / (norm1 * norm2)

# TopK向量检索
def topk_retrieval(query_vec, vec_lib, k=3):
    sim_list = []
    for idx, vec in enumerate(vec_lib):
        sim = cosine_sim(query_vec, vec)
        sim_list.append((idx, sim))
    # 按相似度降序排序
    sim_list.sort(key=lambda x:x[1], reverse=True)
    return sim_list[:k]

# 测试
if __name__ == "__main__":
    # 向量库：5条文档向量
    vec_lib = np.random.randn(5, 8)
    query = np.random.randn(8)
    print(topk_retrieval(query, vec_lib, k=2))
```

**面试考点**
向量检索底层就是余弦相似度；高维向量常用归一化后余弦替代欧氏距离。

---

## 4\. 手撕：PCA 最简手写（纯 Numpy）

**题目**
不调 PCA 库，手写核心降维流程。

```python
import numpy as np

def my_pca(X, n_components):
    # 1. 去中心化
    mean = np.mean(X, axis=0)
    X_center = X - mean
    
    # 2. 协方差矩阵
    cov = np.cov(X_center.T)
    
    # 3. 特征值分解
    eig_val, eig_vec = np.linalg.eig(cov)
    
    # 4. 排序选主成分
    idx = np.argsort(eig_val)[::-1]
    top_vec = eig_vec[:, idx[:n_components]]
    
    # 5. 投影降维
    X_pca = np.dot(X_center, top_vec)
    return X_pca

# 测试
if __name__ == "__main__":
    # 10个样本，5维特征
    X = np.random.randn(10, 5)
    res = my_pca(X, 2)
    print("降维后shape：", res.shape)
```

**面试考点**
PCA 必须去中心化；工程中常用 SVD 替代特征值分解，数值更稳定。

---

## 5\. 手撕：数据集分层抽样（建模必用）

**题目**
手写实现按标签分层抽样，保证训练集测试集类别分布一致，防止数据泄露。

```python
import numpy as np

def stratified_split(X, y, test_ratio=0.2):
    # 按类别分组
    label_dict = {}
    for idx, label in enumerate(y):
        if label not in label_dict:
            label_dict[label] = []
        label_dict[label].append(idx)
    
    train_idx = []
    test_idx = []
    # 每层按比例抽样
    for label, idx_list in label_dict.items():
        n_test = int(len(idx_list) * test_ratio)
        # 随机打乱
        np.random.shuffle(idx_list)
        test_idx.extend(idx_list[:n_test])
        train_idx.extend(idx_list[n_test:])
    
    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]

# 测试
if __name__ == "__main__":
    X = np.random.randn(100, 4)
    y = np.random.randint(0, 2, 100)
    X_train, X_test, y_train, y_test = stratified_split(X, y)
    print("训练集大小", len(X_train), "测试集大小", len(X_test))
```

**面试考点**
分类任务不能随机切分，必须分层抽样；时序数据要用**时间切分**不能随机。

---

> 
# Python 代码题集

# 纯面试手撕 Python 代码题

---

## 一、Pandas 高频基础手撕（6 题）

### 手撕 1

给定 df，**删除全为空值的行和全为空值的列**，手写代码。
**参考答案**

```python
import pandas as pd

# 删除全空行
df = df.dropna(how='all')
# 删除全空列
df = df.dropna(axis=1, how='all')
```

### 手撕 2

手写代码：按 `dept` 分组，求 `salary` 均值、最大值、最小值，并重命名列。
**参考答案**

```python
res = df.groupby('dept')['salary'].agg(
    avg_sal='mean',
    max_sal='max',
    min_sal='min'
).reset_index()
```

### 手撕 3

手写：将 `create_time` 字符串列转为日期格式，**提取年、月、日**新增三列。
**参考答案**

```python
df['create_time'] = pd.to_datetime(df['create_time'])
df['year'] = df['create_time'].dt.year
df['month'] = df['create_time'].dt.month
df['day'] = df['create_time'].dt.day
```

### 手撕 4

手写：筛选 **年龄 20\-35 岁、城市为北京 / 上海、薪资大于 8000** 的数据。
**参考答案**

```python
cond = (df['age'].between(20,35)) & 
       (df['city'].isin(['北京','上海'])) & 
       (df['salary'] > 8000)
res = df[cond]
```

### 手撕 5

手写：对 `score` 列做分箱：60 不及格、60-80 及格、80 优秀，新增 `level` 列。
**参考答案**

```python
bins = [0,60,80,100]
labels = ['不及格','及格','优秀']
df['level'] = pd.cut(df['score'], bins=bins, labels=labels)
```

### 手撕 6

手写：替换列中异常值，将 `salary` 小于 0 或大于 50000 的值改为中位数。
**参考答案**

```python
med = df['salary'].median()
df.loc[(df['salary']<0)|(df['salary']>50000), 'salary'] = med
```

---

## 二、Pandas 数据清洗综合手撕（2 题）

### 手撕 7 经典数据治理清洗

需求：

1. 按 `user_id` 去重，保留最新 `login_time`

2. 性别缺失用众数填充，薪资缺失用中位数填充

3. 过滤 `age` 不在 18\-65 之间的异常行

4. 重置行索引

**手写答案**

```python
# 1 去重
df['login_time'] = pd.to_datetime(df['login_time'])
df = df.sort_values('login_time').drop_duplicates('user_id', keep='last')

# 2 缺失填充
df['gender'] = df['gender'].fillna(df['gender'].mode()[0])
df['salary'] = df['salary'].fillna(df['salary'].median())

# 3 过滤年龄
df = df[df['age'].between(18,65)]

# 4 重置索引
df = df.reset_index(drop=True)
```

### 手撕 8 批量字段类型转换

需求：
把 `id、order_num` 转为字符串；
把 `amount、num` 转为浮点；
把所有时间字段统一转为 datetime。

**手写答案**

```python
# 转字符串
df[['id','order_num']] = df[['id','order_num']].astype(str)

# 转浮点
df[['amount','num']] = df[['amount','num']].astype(float)

# 时间批量转换
time_cols = ['create_time','pay_time','login_time']
for col in time_cols:
    df[col] = pd.to_datetime(df[col], errors='coerce')
```

---

## 三、多表关联 ,中台指标手撕

### 手撕 9 两表关联宽表构建

user 表：user\_id, name, city
order 表：user\_id, order\_amt, order\_dt

需求：

1. 左连接，保留全部用户

2. 统计每个用户订单总金额、订单次数

3. 无订单用户金额、次数填充为 0

**手写答案**

```python
# 分组聚合
order_agg = df_order.groupby('user_id').agg(
    total_amt=('order_amt','sum'),
    order_cnt=('order_amt','count')
).reset_index()

# 左连接
df_merge = pd.merge(df_user, order_agg, on='user_id', how='left')

# 空值填充0
df_merge[['total_amt','order_cnt']] = df_merge[['total_amt','order_cnt']].fillna(0)
```

### 手撕 10 每日 UV、PV 统计

行为表：dt, user\_id, page\_url
需求：按日期统计：每日访问人数 UV、访问次数 PV、独立页面数。

**手写答案**

```python
res = df.groupby('dt').agg(
    uv=('user_id','nunique'),
    pv=('user_id','count'),
    page_cnt=('page_url','nunique')
).reset_index()
```

---

## 四、Numpy 手撕代码

### 手撕 11

创建 5 行 4 列 随机整数数组（10\-100），手写：

1. 每行最大值、每列最小值

2. 所有大于 50 的元素改为 0

**手写答案**

```python
import numpy as np

arr = np.random.randint(10,100,size=(5,4))
# 每行最大
row_max = arr.max(axis=1)
# 每列最小
col_min = arr.min(axis=0)
# 大于50改0
arr[arr > 50] = 0
```

### 手撕 12

手写实现数组归一化到 \[0,1\]（按全局归一化）
**手写答案**

```python
def min_max_norm(arr):
    min_val = arr.min()
    max_val = arr.max()
    return (arr - min_val) / (max_val - min_val)
```

---

## 五、Sklearn 特征工程手撕

### 手撕 13

手写：数值列标准化、类别列 OneHot 编码，拼接特征。
**手写答案**

```python
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import pandas as pd

num_cols = ['age','salary']
cat_cols = ['city','gender']

scaler = StandardScaler()
num_feat = scaler.fit_transform(df[num_cols])

ohe = OneHotEncoder(drop='first', sparse_output=False)
cat_feat = ohe.fit_transform(df[cat_cols])

# 拼接
all_feat = np.hstack([num_feat, cat_feat])
```

### 手撕 14

手写：划分训练集测试集，测试集 20%，固定随机种子，分层抽样。
**手写答案**

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)
```

---

## 六、数据中台真实业务手撕真题

### 手撕 15 数据质量校验手撕

需求：手写函数，输入 df，输出：

- 每列缺失率

- 重复行数量

- 异常金额（amount\&lt;0）条数

**手写答案**

```python
def data_quality_check(df):
    # 缺失率
    missing_rate = df.isnull().sum() / len(df)
    # 重复行数
    dup_num = df.duplicated().sum()
    # 负金额条数
    amt_err = (df['amount'] < 0).sum()
    return missing_rate, dup_num, amt_err
```

### 手撕 16 大表内存优化手撕

手写代码：对 df 做内存精简优化，把对象列转 category，数值列降精度。
**手写答案**

```python
# 类别列优化
cat_cols = ['city','channel','status']
df[cat_cols] = df[cat_cols].astype('category')

# 数值降精度
df['age'] = df['age'].astype('int32')
df['amount'] = df['amount'].astype('float32')
```

---

> 
