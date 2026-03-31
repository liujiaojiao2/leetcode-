"""
LeetCode 146. LRU 缓存

题目编号：146
题目名称：LRU 缓存
难度：中等
链接：https://leetcode.cn/problems/lru-cache/

题目描述：
实现 LRU (Least Recently Used) 缓存：
- get(key)：若 key 存在则返回对应值并视为「最近使用」，否则返回 -1。
- put(key, value)：若 key 已存在则更新值并视为「最近使用」；否则插入。
  若插入前已达容量上限，则先淘汰「最近最少使用」的键再插入。
get/put 均需 O(1) 时间复杂度。

思路：
- 需要 O(1) 查找 → 哈希表 key -> 节点或值。
- 需要 O(1) 维护「最近使用」顺序、O(1) 淘汰最久未用 → 双向链表（头=最近，尾=最久）。
- 组合：哈希表存 key -> 链表节点；链表按访问顺序排列，get/put 时把节点移到头，满时删尾。

知识点 / 模版：
- LRU = 哈希表 + 双向链表（或 OrderedDict）。哈希保证 O(1) 查找，链表保证 O(1) 调整顺序与删尾。
- 双向链表模版：虚拟头 head、虚拟尾 tail，head.next 为最近，tail.prev 为最久。新增/访问时「删节点再插到头」；满时删 tail.prev 并删哈希表对应项。
- OrderedDict 模版：Python 的 OrderedDict 底层即哈希+双向链表，move_to_end(key) 表示最近使用，popitem(last=False) 表示删最久未用。
- 面试可先写 OrderedDict 版，再按面试官要求手写「哈希 + 双向链表」。
"""

from collections import OrderedDict
from typing import Optional


# ==================== 写法一：OrderedDict（推荐先写，代码最短） ====================

class LRUCache:
    """
    使用 OrderedDict：内部维护插入/访问顺序，move_to_end=最近使用，popitem(last=False)=删最久。
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: OrderedDict[int, int] = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)  # 标记为最近使用
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key)
            return
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)  # 删除最久未使用的项（在头部）


# ==================== 写法二：手写哈希 + 双向链表（面试可能要求） ====================

class DLinkedNode:
    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev: Optional[DLinkedNode] = None
        self.next: Optional[DLinkedNode] = None


class LRUCacheHandWritten:
    """
    手写：dict 存 key -> DLinkedNode；双向链表头=最近使用，尾=最久未用。
    """

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[int, DLinkedNode] = {}
        self.head = DLinkedNode()
        self.tail = DLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove_node(self, node: DLinkedNode) -> None:
        """从链表中移除节点（不删哈希表）。"""
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_head(self, node: DLinkedNode) -> None:
        """把节点插到头部（最近使用）。"""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _move_to_head(self, node: DLinkedNode) -> None:
        """先删再插到头 = 视为最近使用。"""
        self._remove_node(node)
        self._add_to_head(node)

    def _remove_tail(self) -> DLinkedNode:
        """删除并返回尾节点（最久未用）。"""
        node = self.tail.prev
        self._remove_node(node)
        return node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._move_to_head(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
            return
        node = DLinkedNode(key, value)
        self.cache[key] = node
        self._add_to_head(node)
        if len(self.cache) > self.capacity:
            tail = self._remove_tail()
            del self.cache[tail.key]


# ========== 本地测试 ==========

def _test_lru(cache_class, capacity: int) -> None:
    """LeetCode 示例：capacity=2 时的标准流程。"""
    obj = cache_class(capacity)
    obj.put(1, 1)
    obj.put(2, 2)
    assert obj.get(1) == 1
    obj.put(3, 3)  # 淘汰 key=2
    assert obj.get(2) == -1
    obj.put(4, 4)  # 淘汰 key=1
    assert obj.get(1) == -1
    assert obj.get(3) == 3
    assert obj.get(4) == 4


if __name__ == "__main__":
    _test_lru(LRUCache, 2)
    _test_lru(LRUCacheHandWritten, 2)
    print("All passed.")
