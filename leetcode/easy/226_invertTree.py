"""
LeetCode 做题模板
复制此文件后，修改下方的题目信息与解题代码即可。

题目编号：226
题目名称：翻转二叉树
难度：
链接：https://leetcode.cn/problems/invert-binary-tree/

题目描述：
给你一棵二叉树的根节点 root ，翻转这棵二叉树，并返回其根节点。

思路：
翻转本质上是：对每个节点，把它的左子树和右子树交换。
递归地看：先处理当前节点（交换左右孩子），再递归处理左右子树即可，遍历顺序可以是前序 / 后序，只要保证对每个节点都交换一次左右子树。

知识点 / 模版：
- 二叉树递归操作的通用思路：对当前节点做「局部操作」，再递归左右子树。
- 本题的「局部操作」就是：`root.left, root.right = root.right, root.left`。
- LeetCode 会负责把数组（层序表示）构造成 TreeNode 形式，并在内部比较树结构是否正确，函数只需返回根节点，不需要自己输出数组。
"""

from typing import Optional  # 按需导入


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None, right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def invertTree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        if not root:
            return None
        root.left, root.right = root.right, root.left
        self.invertTree(root.left)
        self.invertTree(root.right)
        return root


def build_example_tree() -> TreeNode:
    """
    示例树：[4,2,7,1,3,6,9]
            4
           / \
          2   7
         / \ / \
        1  3 6  9
    翻转后为：[4,7,2,9,6,3,1]
    """
    n1 = TreeNode(1)
    n3 = TreeNode(3)
    n6 = TreeNode(6)
    n9 = TreeNode(9)
    n2 = TreeNode(2, n1, n3)
    n7 = TreeNode(7, n6, n9)
    root = TreeNode(4, n2, n7)
    return root


def level_order_values(root: Optional[TreeNode]) -> list[int]:
    """辅助函数：层序遍历返回节点值列表，便于本地对比结果。"""
    if not root:
        return []
    from collections import deque

    res: list[int] = []
    queue: deque[TreeNode] = deque([root])
    while queue:
        node = queue.popleft()
        res.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return res


# ========== 本地测试 ==========
if __name__ == "__main__":
    root = build_example_tree()
    s = Solution()
    inverted = s.invertTree(root)
    assert level_order_values(inverted) == [4, 7, 2, 9, 6, 3, 1]
    print("All passed.")
