"""
LeetCode 做题模板
复制此文件后，修改下方的题目信息与解题代码即可。

题目编号：102   
题目名称：二叉树的层序遍历
难度：中等
链接：https://leetcode.cn/problems/binary-tree-level-order-traversal/

题目描述：
给你二叉树的根节点 root ，返回其节点值的 层序遍历 。 （即逐层地，从左到右访问所有节点）。

思路：
层序遍历一棵树需要用到队列，先将根结点入队，然后不断出队当前层的节点，并将其左右孩子依次入队，直到队列为空。

知识点 / 模版：
- 层序遍历（BFS）核心：使用队列，按层逐批处理节点。
- 典型模版：
  1. 判断 root 是否为空，空则返回 []。
  2. `queue = [root]` 或 `deque([root])`。
  3. `while queue:` 时，先记录当前层大小 `size = len(queue)`。
  4. 循环 `size` 次：依次弹出本层节点，记录其值并把左右子节点入队。
  5. 本层收集完后，将 `level`（当前层的值列表）加入 `result`。
"""

from collections import deque
from typing import List, Optional  # 按需导入


class TreeNode:
    def __init__(self, val: int = 0, left: "Optional[TreeNode]" = None, right: "Optional[TreeNode]" = None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        result: List[List[int]] = []
        queue: deque[TreeNode] = deque([root])

        while queue:
            level: List[int] = []
            # 当前循环中处理完这一层的所有节点
            for _ in range(len(queue)):
                node = queue.popleft()
                level.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(level)
        return result


def build_example_tree() -> TreeNode:
    """
    示例树：[3,9,20,null,null,15,7]
           3
          / \
         9  20
           /  \
          15   7
    对应该题典型样例，层序遍历结果为 [[3], [9,20], [15,7]]。
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
    assert s.levelOrder(root) == [[3], [9, 20], [15, 7]]
    print("All passed.")
