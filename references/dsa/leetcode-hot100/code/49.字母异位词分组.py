#
# @lc app=leetcode.cn id=49 lang=python3
#
# [49] 字母异位词分组
#

# @lc code=start
class Solution:
    from collections import defaultdict
    from typing import List
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        groupDict = defaultdict(list)
        for str in strs:
            sorted_str = "".join(sorted(str))
            groupDict[sorted_str].append(str)
        return list(groupDict.values())
# @lc code=end

