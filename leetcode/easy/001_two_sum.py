"""
1. 两数之和 (Two Sum)
难度：简单
链接：https://leetcode.cn/problems/two-sum/

题目描述：
给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出和为目标值 target 的那两个整数，
并返回它们的数组下标。你可以假设每种输入只会对应一个答案。且同样的元素不能重复出现。

思路：
用哈希表记录「已遍历过的值 -> 下标」，遍历时检查 target - num 是否在表中。
"""

from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen = {}  # 值 -> 下标
        for i, x in enumerate(nums):
            need = target - x
            if need in seen:
                return [seen[need], i]
            seen[x] = i
        return []


# ========== 本地测试 ==========
if __name__ == "__main__":
    s = Solution()
    assert s.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert s.twoSum([3, 2, 4], 6) == [1, 2]
    assert s.twoSum([3, 3], 6) == [0, 1]
    print("All passed.")
