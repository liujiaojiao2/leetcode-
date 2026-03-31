"""
LeetCode 做题模板
复制此文件后，修改下方的题目信息与解题代码即可。

题目编号：20
题目名称：有效的括号
难度：简单
链接：https://leetcode.cn/problems/valid-parentheses/

题目描述：
给定一个只包括 '('，')'，'{'，'}'，'['，']' 的字符串 s ，判断字符串是否有效。

思路：
使用栈存储括号，遇到左括号入栈，遇到右括号则和栈顶元素匹配，匹配则出栈；不匹配或栈空则无效；遍历结束栈非空则无效。

知识点/模版：
- 括号匹配 → 栈（LIFO），左括号入栈，右括号与栈顶配对。
- 用字典维护 右括号→左括号 的映射，可避免多个 if-elif，易扩展多种括号。
- 边界：空串有效；奇数长度可直接 False；仅右括号（栈空遇右括号）无效；仅左括号（最后栈非空）无效。
"""

from typing import List  # 按需导入

# 右括号 -> 左括号，便于统一判断「栈顶是否与当前右括号配对」
PAIR = {")": "(", "]": "[", "}": "{"}


class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        for char in s:
            if char in "([{":
                stack.append(char)
            else:
                # 右括号：栈空 或 栈顶不配对 → 无效
                if not stack or stack[-1] != PAIR[char]:
                    return False
                stack.pop()
        return not stack  # 有效 ⟺ 栈为空


# ========== 本地测试 ==========
if __name__ == "__main__":
    s = Solution()
    assert s.isValid("()") is True
    assert s.isValid("()[]{}") is True
    assert s.isValid("(]") is False
    assert s.isValid("([)]") is False
    assert s.isValid("{[]}") is True
    assert s.isValid("") is True
    assert s.isValid("(") is False
    assert s.isValid(")") is False
    print("All passed.")