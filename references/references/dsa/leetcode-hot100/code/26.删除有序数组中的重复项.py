#
# @lc app=leetcode.cn id=26 lang=python3
#
# [26] 删除有序数组中的重复项
#

# @lc code=start
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0
        slow=1
        for fast in range(1,len(nums)):
            if nums[fast]!=nums[fast - 1]:
                nums[slow]=nums[fast]
                slow += 1 # slow++
        return slow
        
        #nums[:] = sorted(set(nums))
        #nums=list(set(nums)) #nums=set(nums)
        #return len(nums)                
# @lc code=end

