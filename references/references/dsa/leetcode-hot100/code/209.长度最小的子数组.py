#
# @lc app=leetcode.cn id=209 lang=python3
#
# [209] 长度最小的子数组
#

# @lc code=start
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        if not nums:
            return 0
        left = 0
        current_sum = 0
        min_len =  len(nums) + 1 if sum(nums) >= target else 0
        for right in range(len(nums)):
            current_sum += nums[right]
            if current_sum >= target:
                while current_sum >= target:
                    #print(sum(nums[left:right]) + nums[right])
                    min_len = min(min_len,right - left +1)
                    current_sum -= nums[left]
                    left += 1
            #print(min_len)
        return min_len 
            


# @lc code=end

