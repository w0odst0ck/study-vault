#
# @lc app=leetcode.cn id=128 lang=python3
#
# [128] 最长连续序列
#

# @lc code=start
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0
        sorted_num = list(sorted(set(nums)))
        sorted_num_reverse =  list(sorted(set(nums),reverse=True))
        print(sorted_num)
        print(sorted_num_reverse)
        i = 1
        length = 0
        for num in sorted_num:
            if i == len(sorted_num) or (sorted_num[i] - 1) != sorted_num[i-1] :
                length = i
                break
            else:
                i += 1
        length = i
        i = 1
        reversed_length = 0
        for num in sorted_num_reverse:
            if i == len(sorted_num_reverse) or (sorted_num_reverse[i] + 1) != sorted_num_reverse[i-1]:
                reversed_length = i
                break
            else:
                i += 1
        reversed_length = i

        return length if length > reversed_length else reversed_length

# @lc code=end

