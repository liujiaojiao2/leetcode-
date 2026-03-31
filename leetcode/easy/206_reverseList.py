"""
LeetCode 做题模板
复制此文件后，修改下方的题目信息与解题代码即可。

题目编号：206
题目名称：反转链表
难度：简单
链接：https://leetcode.cn/problems/reverse-linked-list/

题目描述：
给你单链表的头节点 head ，请你反转链表，并返回反转后的链表。

思路：
反转本质是把链表中每条边的指向「掉头」，使 next 指回前一个节点。

常见两种写法：
- 迭代双指针：pre 指向前一个节点，cur 指向当前节点，在循环中不断「断开 → 掉头 → 前进」。
- 递归：假设 head.next 之后的链表已经反转完成，利用子结果把 head 接到尾部。

知识点 / 模版：
- 迭代模版（推荐优先记）：  
  pre = None, cur = head  
  while cur:  
      nex = cur.next  
      cur.next = pre  
      pre = cur  
      cur = nex  
  return pre
- 递归模版：  
  if head is None or head.next is None: return head  
  new_head = reverse(head.next)  
  head.next.next = head  
  head.next = None  
  return new_head
"""

from typing import Optional  # 按需导入


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next


class IterSolution:
    """迭代双指针版，作为主模版更好记。"""

    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        pre: Optional[ListNode] = None
        cur: Optional[ListNode] = head
        while cur:
            nex = cur.next
            cur.next = pre
            pre = cur
            cur = nex
        return pre


class RecSolution:
    """递归版，利用子问题结果反接指针。"""

    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        new_head = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return new_head


# ========== 本地测试 ==========
if __name__ == "__main__":
    # 构造示例链表 [1,2,3,4,5]
    n5 = ListNode(5)
    n4 = ListNode(4, n5)
    n3 = ListNode(3, n4)
    n2 = ListNode(2, n3)
    head = ListNode(1, n2)

    # 迭代版测试
    it = IterSolution()
    new_head_it = it.reverseList(head)
    vals_it = []
    while new_head_it:
        vals_it.append(new_head_it.val)
        new_head_it = new_head_it.next
    assert vals_it == [5, 4, 3, 2, 1]

    # 递归版测试（重新构造一次链表）
    n5 = ListNode(5)
    n4 = ListNode(4, n5)
    n3 = ListNode(3, n4)
    n2 = ListNode(2, n3)
    head = ListNode(1, n2)

    rec = RecSolution()
    new_head_rec = rec.reverseList(head)
    vals_rec = []
    while new_head_rec:
        vals_rec.append(new_head_rec.val)
        new_head_rec = new_head_rec.next
    assert vals_rec == [5, 4, 3, 2, 1]

    print("All passed.")