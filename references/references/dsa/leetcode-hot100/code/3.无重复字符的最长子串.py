#
# @lc app=leetcode.cn id=3 lang=python3
#
# [3] 无重复字符的最长子串
#

# @lc code=start
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        if not s:
            return 0
        left = 0
        win = 1
        substr = s[0]
        longest_substr = s[0]
        for right in range(1,len(s)):
            if s[right] in substr:
                while s[right] in substr: 
                    left +=1
                    substr = substr[1:]
            substr += s[right]
            if len(substr) > len(longest_substr):
                longest_substr = substr
            win = max(win,right - left + 1)
        return win
# @lc code=end

