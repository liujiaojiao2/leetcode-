"""
LeetCode 做题模板
复制此文件后，修改下方的题目信息与解题代码即可。

题目编号：104
题目名称：二叉树的最大深度
难度：简单
链接：https://leetcode.cn/problems/maximum-depth-of-binary-tree/

题目描述：
给定一个二叉树，找出其最大深度。

思路：
最大深度定义为：从根节点到最远叶子节点的最长路径上的节点数量。
递归地看：一棵树的深度 = 1 + max(左子树深度, 右子树深度)，空节点深度为 0。

知识点 / 模版：
- 二叉树递归 DFS 模版（后序）：  
  depth(root) = 0 if root is None  
  depth(root) = 1 + max(depth(root.left), depth(root.right))
- LeetCode 输入数组是「层序表示」，平台会先帮你构建 TreeNode 结构，函数直接接收 root。
- 也可以用 BFS（层序遍历）按层数累加求深度，本质是统计二叉树层数。
"""

from typing import Optional  # 按需导入


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None, right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0
        left_depth = self.maxDepth(root.left)
        right_depth = self.maxDepth(root.right)
        return 1 + max(left_depth, right_depth)


def build_example_tree() -> TreeNode:
    """
    示例树：[3,9,20,null,null,15,7]
           3
          / \
         9  20
           /  \
          15   7
    最大深度为 3。
    """
    n15 = TreeNode(15)
    n7 = TreeNode(7)
    n9 = TreeNode(9)
    n20 = TreeNode(20, n15, n7)
    root = TreeNode(3, n9, n20)
    return root



# ========== 本地测试 ==========
if __name__ == "__main__":
    root = build_example_tree()
    s = Solution()
    assert s.maxDepth(root) == 3
    print("All passed.")
