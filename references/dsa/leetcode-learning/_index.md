# LeetCode 刷题课程·C++ 参考

> **来源**：旧知识库「编程语言基础/C++/leetcode-Learning」
> **语言**：C++（含少量 Python 参考）
> **结构**：3 个系列共 72 篇 README 讲解 + 数百道 .cpp 题解

---

## 系列概览

| 系列 | 主题数 | 定位 |
|------|--------|------|
| `01_alg/` 算法基础 | 20 章 | 按数据结构/算法为主题的系统讲解 |
| `02_hot100/` 热题 100 | 17 章 | LeetCode 高频面试题题解 |
| `03_algo_note/` 算法笔记 | 4 部分 | 更细分的题型分类笔记 |

---

## 01_alg — 算法基础

| # | 专题 | 包含题解 |
|---|------|---------|
| 01 | [算法与数据结构概述](docs/01_alg/01_overview/README.md) | — |
| 02 | [复杂度分析](docs/01_alg/02_complexity_analysis/README.md) | — |
| 03 | [数组/链表/跳表](docs/01_alg/03_array_list_skiplist/README.md) | 盛水最多容器、LRU、三数之和、反转链表、环形链表等 |
| 04 | [栈与队列](docs/01_alg/04_stack_queue/README.md) | 最小栈、括号匹配、滑动窗口最大值、接雨水 |
| 05 | [哈希表](docs/01_alg/05_hash_map_set/README.md) | 异位词分组、有效异位词 |
| 06 | [树](docs/01_alg/06_tree/README.md) | 三种遍历、N 叉树遍历 |
| 07 | [递归](docs/01_alg/07_recursion/README.md) | 二叉树最大深度、从前序中序构造、全排列、组合 |
| 08 | [分治](docs/01_alg/08_divide/README.md) | 多数元素、Pow(x,n)、N 皇后、子集 |
| 09 | [DFS/BFS](docs/01_alg/09_dfs_bfs/README.md) | 层序遍历、岛屿数量、单词接龙 |
| 10 | [贪心](docs/01_alg/10_greedy/README.md) | 买卖股票、跳跃游戏、分发饼干 |
| 11 | [二分查找](docs/01_alg/11_binary_search/README.md) | 旋转数组、搜索二维矩阵、x 的平方根 |
| 12 | [DP](docs/01_alg/12_dp/README.md) | 斐波那契、打家劫舍、零钱兑换、LCS |
| 13 | [Trie/并查集](docs/01_alg/13_trie_disjoint_set/README.md) | 前缀树、单词搜索 II、省份数量 |
| 14 | [高级搜索](docs/01_alg/14_advanced_search/README.md) | 解数独、滑动谜题 |
| 15 | [AVL 树/红黑树](docs/01_alg/15_avl_tree/README.md) | 理论讲解 |
| 16 | [位运算](docs/01_alg/16_bitwise/README.md) | 位 1 个数、2 的幂、比特位计数 |
| 17 | [布隆过滤器/LRU](docs/01_alg/17_bloom_filter_lru/README.md) | LRU 缓存、Bloom Filter Python 实现 |
| 18 | [排序](docs/01_alg/18_sort/README.md) | 排序数组、合并区间、翻转对 |
| 19 | [高阶 DP](docs/01_alg/19_advice_dp/README.md) | 编辑距离、使用最小花费爬楼梯 |
| 20 | [字符串](docs/01_alg/20_string/README.md) | 反转字符串、最长公共前缀、最长回文子串、正则匹配 |

## 02_hot100 — 热题 100

| # | 专题 | 题数 |
|---|------|------|
| 01 | [哈希](docs/02_hot100/01_hash/README.md) | 3 题 |
| 02 | [双指针](docs/02_hot100/02_double_ptr/README.md) | 5 题 |
| 03 | [滑动窗口](docs/02_hot100/03_slide_windows/README.md) | 2 题 |
| 04 | [字符串/子串](docs/02_hot100/04_string/README.md) | 3 题 |
| 05 | [数组](docs/02_hot100/05_array/README.md) | 5 题 |
| 06 | [矩阵](docs/02_hot100/06_matrix/README.md) | 5 题 |
| 07 | [链表](docs/02_hot100/07_list/README.md) | 14 题 |
| 08 | [树](docs/02_hot100/08_tree/README.md) | 15 题 |
| 09 | [图](docs/02_hot100/09_graph/README.md) | 5 题 |
| 10 | [回溯](docs/02_hot100/10_backtracking/README.md) | 8 题 |
| 11 | [二分查找](docs/02_hot100/11_bin_search/README.md) | 6 题 |
| 12 | [栈](docs/02_hot100/12_stack/README.md) | 5 题 |
| 13 | [堆](docs/02_hot100/13_heap/README.md) | 3 题 |
| 14 | [贪心](docs/02_hot100/14_greedy/README.md) | 5 题 |
| 15 | [DP](docs/02_hot100/15_dp/README.md) | 10 题 |
| 16 | [多维 DP](docs/02_hot100/16_multi_dp/README.md) | 5 题 |
| 17 | [技巧](docs/02_hot100/17_skills/README.md) | 6 题 |

## 03_algo_note — 算法笔记

| 部分 | 章节 | 主题 |
|------|------|------|
| 01_algo_array | 1.1 DSA 入门 / 1.2 数组 / 1.3 排序 / 1.4 二分 / 1.5 双指针 / 1.6 滑动窗口 | 入门+数组题型 |
| 02_basic_ds | 2.1-2.15 链表/栈/队列/优先队列/BFS/DFS/拓扑/哈希/树/BST/字符串 | 基础数据结构全 |
| 03_basic_algo | 3.1 枚举 / 3.2 递归 / 3.3 分治 / 3.4 回溯 / 3.5 贪心 / 3.6 位运算 | 算法思想 |
| 04_dp | 4.1 记忆化 / 4.2 线性DP / 4.3 背包 | DP 专题 |

---

> **说明**：本目录仅包含讲解文档（README.md）。.cpp 题解文件和图片素材在原始仓库中：
> `C:\Users\l\Downloads\编程语言基础\C++\leetcode-Learning`
