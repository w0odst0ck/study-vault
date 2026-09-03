#
# @lc app=leetcode.cn id=34 lang=python3
#
# [34] 在排序数组中查找元素的第一个和最后一个位置
#

# @lc code=start
class Solution:
    def searchRange(self, nums: List[int], target: int) -> List[int]:
        start = end = -1
        if not nums:
            return [start,end]
        left , right = 0 , len(nums) - 1
        
        while left <= right:
            mid = (left+right)//2
            if nums[mid] == target:
                start = end = mid
                right = mid -1
            elif nums[mid] > target:
                right = mid -1
            else:
                left = mid + 1
        if start == -1:
            return [start,end]
        #print(start,end)
        while end < len(nums) and nums[end] == target :
            end += 1
            #print(end)
        return [start,end - 1]

# @lc code=end

