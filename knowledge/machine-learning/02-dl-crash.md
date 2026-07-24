---
status: active
created: 2026-07-22
updated: 2026-07-22
tags:
  - DL
  - 深度学习
  - NLP
  - 激活函数
  - Transformer
cards: []
---

# 深度学习面试速查

> 核心概念 / 激活函数 / 网络结构 / NLP 基础
> 来源：旧知识库「Knowledge-Base-for-Interviews」

---

## 1. 前向传播与反向传播

```
前向：x → Wx+b → σ → output → Loss
反向：Loss → dL/dW → 梯度更新
```

| 概念 | 说明 |
|------|------|
| 前向 | 输入逐层计算到输出，产生预测 |
| 反向 | 链式法则计算各层梯度 |
| 梯度消失 | 浅层梯度趋近 0（Sigmoid 饱和区） |
| 梯度爆炸 | 梯度指数增长（RNN 常见） |

---

## 2. 激活函数

| 函数 | 公式 | 优点 | 缺点 |
|------|------|------|------|
| Sigmoid | 1/(1+e⁻ˣ) | 输出 0-1，适合二分类 | 梯度消失、非零中心 |
| Tanh | (eˣ-e⁻ˣ)/(eˣ+e⁻ˣ) | 零中心 | 梯度消失 |
| ReLU | max(0, x) | 计算快、缓解梯度消失 | Dead ReLU |
| LeakyReLU | max(αx, x) | 解决 Dead ReLU | α 需要调参 |

**经验**：默认用 ReLU，输出层按任务选（二分类→Sigmoid，多分类→Softmax）

---

## 3. 优化器

| 优化器 | 特点 |
|--------|------|
| SGD | 基础，收敛慢，需手动调 lr |
| Momentum | 加速 SGD，越过局部最优 |
| Adam | 自适应 lr + Momentum，默认首选 |
| AdamW | Adam + 正确的权重衰减 |

---

## 4. 常用网络结构

| 结构 | 用途 | 核心思想 |
|------|------|---------|
| CNN | 图像/文本 | 局部连接 + 权值共享 + 池化 |
| RNN/LSTM | 序列/时间序列 | 门控机制解决长期依赖 |
| Transformer | NLP/CV/多模态 | 自注意力 + 位置编码，并行计算 |
| ResNet | 深层网络 | 残差连接解决退化问题 |

### Transformer 核心

```
Self-Attention: Q × K^T → softmax → × V
Multi-Head: 多个自注意力头拼接
位置编码: 让模型感知序列位置
LayerNorm + FFN: 每个子层后的标配
```

---

## 5. 过拟合解决方法

| 方法 | 原理 |
|------|------|
| Dropout | 训练时随机丢弃神经元，类似模型集成 |
| BatchNorm | 每层归一化 + 微小噪声 |
| 早停 | 验证集 loss 不降即停 |
| 数据增强 | 增加样本多样性 |
| 正则化 | L1/L2 惩罚大权重 |

---

## 回顾

- Q: ReLU 相比 Sigmoid 的优势？
  A: 计算快、正区间梯度恒为 1 缓解梯度消失、稀疏激活

- Q: 梯度消失和梯度爆炸分别怎么解决？
  A: 消失→ReLU/BatchNorm/残差连接；爆炸→梯度裁剪/权重初始化

- Q: Transformer 为什么比 RNN 好？
  A: 自注意力并行计算（RNN 串行）、全局视野（RNN 逐步遗忘）、多模态适用

- Q: Dropout 为什么能防过拟合？
  A: 每次随机删除神经元 → 相当于训练多个子网络 → 类似 Bagging 集成

- Q: BatchNorm 在训练和推理时的区别？
  A: 训练时用 batch 均值和方差，推理时用全局滑动平均
