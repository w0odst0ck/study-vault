# ======================================================
# Numpy实现两个二维数组的矩阵乘法，以及两个一维数组的点积，
# ======================================================
import numpy as np

arr1 = np.array([[1,2],[3,4]])
arr2 = np.array([[5,6],[7,8]])

result = np.dot(arr1,arr2)
print(result)

arr3 = np.array([1,2,3])
arr4 = np.array([4,5,6])

result2 = np.dot(arr3,arr4)
print(result2)

# ================================================================================
# （1）查看数据集的缺失值比例；
# （2）删除重复行（保留第一次出现的行）；
# （3）用“中位数”填充数值型字段的缺失值，用“众数”填充分类型字段的缺失值；
# （4）用IQR方法识别并处理数值型字段的异常值（将异常值替换为该字段的上四分位/下四分位）。
# ================================================================================
import pandas as pd
import numpy as np

# 1. 模拟数据集（贴合数据治理实际，包含数值型、分类型字段，故意设置缺失值、重复值、异常值）
data = pd.DataFrame({
    "user_id": [1, 2, 2, 3, 4, 5, 6, 7, 8, 9],  # 重复值（user_id=2）
    "age": [25, 32, None, 40, 100, 35, None, 28, 36, 31],  # 缺失值、异常值（100）
    "gender": ["男", "女", "女", None, "男", "女", "男", None, "女", "男"],  # 缺失值
    "salary": [8000, 9500, 9500, None, 15000, 8500, 12000, 7800, 9000, 20000]  # 缺失值、异常值（20000）
})

# 查看缺失率
print("===== 缺失值占比 =====")
missing_rate = data.isnull().sum() / len(data)
print(missing_rate)

# 2. 去除重复值
data = data.drop_duplicates(keep="first")
print("\n===== 去重后数据 =====")
print(data)

# 3. 处理缺失值（修复 ChainedAssignmentError 警告）
numeric_cols = data.select_dtypes(include=[np.number]).columns
# 数值型用中位数填充
for col in numeric_cols:
    median_val = data[col].median()
    # 不使用 inplace，直接赋值，避免链式赋值错误
    data[col] = data[col].fillna(median_val)

# 分类型字段（修复 object 警告，使用 str 类型）
category_cols = data.select_dtypes(include=["object", "string"]).columns
# 分类型用众数填充
for col in category_cols:
    mode_val = data[col].mode()[0]
    data[col] = data[col].fillna(mode_val)

print("\n===== 缺失值填充后 =====")
print(data)

# 4. 异常值处理（IQR法，修复类型错误：统一转为float）
def handle_outliers_iqr(df, col):
    # 先转为浮点型，避免 int 无法存储小数边界值
    df[col] = df[col].astype(float)
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    # 截断异常值
    df.loc[df[col] < lower_bound, col] = lower_bound
    df.loc[df[col] > upper_bound, col] = upper_bound
    return df

# 只对业务数值列处理异常值（排除 user_id，更合理）
for col in ["age", "salary"]:
    data = handle_outliers_iqr(data, col)

print("\n===== 最终清洗后数据 =====")
print(data)

# ===============================================================================================================
# 现有两张表：表1（user_info）包含user_id（用户ID）、user_name（用户名）、register_time（注册时间）；
# 表2（user_behavior）包含user_id（用户ID）、behavior_type（行为类型：浏览/下单/支付）、behavior_time（行为时间）。
# 请实现：
# （1）将两张表通过user_id进行内连接，得到“用户信息+用户行为”的完整数据；
# （2）统计每个用户的行为总数，新增“behavior_count”字段；
# （3）筛选出“注册时间在2024-01-01之后，且有支付行为”的用户数据。
# ===============================================================================================================
import pandas as pd
from datetime import datetime

# 1. 模拟两张表数据
user_info = pd.DataFrame({
    "user_id": [101, 102, 103, 104, 105],
    "user_name": ["张三", "李四", "王五", "赵六", "孙七"],
    "register_time": ["2023-12-25", "2024-01-05", "2024-02-10", "2023-11-30", "2024-03-01"]
})

user_behavior = pd.DataFrame({
    "user_id": [101, 101, 102, 103, 103, 104, 105, 105],
    "behavior_type": ["浏览", "下单", "支付", "浏览", "支付", "浏览", "下单", "支付"],
    "behavior_time": ["2024-01-02", "2024-01-03", "2024-01-06", "2024-02-11", "2024-02-15", "2024-01-01", "2024-03-02", "2024-03-03"]
})

merge_data = pd.merge(user_info,user_behavior,on="user_id",how="inner")

behavior_count = merge_data.groupby("user_id").size().reset_index(name="behavior_count") # 聚合
