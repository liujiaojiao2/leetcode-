"""
LeetCode 做题模板
复制此文件后，修改下方的题目信息与解题代码即可。

题目编号：3
题目名称：无重复字符的最长子串
难度：中等
链接：https://leetcode.cn/problems/length-of-longest-substring/

题目描述：
给定一个字符串 s ，请你找出其中不含有重复字符的 最长子串 的长度。

思路：
通过滑动双指针，固定左指针，滑动右指针，记录最长子串长度。
"""

from typing import List  # 按需导入


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        # 哈希集合，记录每个字符是否出现过
        occ = set()
        n = len(s)
        # 右指针，初始值为 -1，相当于我们在字符串的左边界的左侧，还没有开始移动
        r, ans = -1, 0
        for i in range(n):
            # 左指针右移时，从集合中移除上一个左端点字符（i=0 时没有上一个字符，不能 remove）
            if i > 0:
                occ.remove(s[i - 1])
            while r + 1 < n and s[r + 1] not in occ:
                # 不断地移动右指针
                occ.add(s[r + 1])
                r += 1
            # 第 i 到 r 个字符是一个极长的无重复字符子串
            ans = max(ans, r - i + 1)
        return ans



# ========== 本地测试 ==========
if __name__ == "__main__":
    s = Solution()
    # 添加测试用例
    # print(s.method_name(...))
    assert s.lengthOfLongestSubstring("abcabcbb") == 3
    assert s.lengthOfLongestSubstring("bbbbb") == 1
    assert s.lengthOfLongestSubstring("pwwkew") == 3
    print("All passed.")


# ========== 本题模板与知识点总结 ==========
"""
【题型】子串/子数组 + 满足某条件的最长长度 → 滑动窗口（双指针）

【滑动窗口模板】
  - 左指针 i：枚举「以 i 为左端点的极长合法窗口」
  - 右指针 r：当前窗口的右端点，窗口内容为 s[i..r]
  - 集合/哈希：维护窗口内已有字符，用于 O(1) 判重

   for i in range(n):
       if i > 0:
           从集合中移除 s[i-1]   # 左指针右移，收缩窗口
       while r+1 < n and 可扩展:  # 右指针尽量右移，扩展窗口
           加入 s[r+1]，r += 1
       ans = max(ans, 窗口长度)   # 更新答案

【重要知识点】
  1. 双指针含义：i 是左边界，r 是右边界，窗口 [i, r] 内始终无重复。
  2. 集合 set：用来存「当前窗口内出现的字符」，查重 O(1)。
  3. 窗口长度：r - i + 1（闭区间 [i,r] 的个数）。
  4. 易错点：i=0 时不能 remove(s[i-1])，因为 s[-1] 不在窗口内，且集合为空会 KeyError。

【复杂度】每个字符最多进、出集合各一次，时间 O(n)，空间 O(字符集大小)。

【可复用场景】「最长无重复子串」「最多含 k 个某字符的最长子串」等子串最值问题。
"""
