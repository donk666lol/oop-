# -*- coding: utf-8 -*-
"""
双向链表模块 - Doubly Linked List Module

双向链表是一种线性数据结构，每个节点包含三个部分：
1. 数据元素 (_element)
2. 指向前一个节点的指针 (_prev)
3. 指向后一个节点的指针 (_next)

时间复杂度分析：
- 插入（头/尾/中间）：O(1) - 直接修改指针
- 删除（头/尾/中间）：O(1) - 直接修改指针
- 查找：O(n) - 需要遍历
- 访问特定位置：O(n) - 需要从头遍历

空间复杂度：O(n) - 每个节点需要额外存储两个指针

适用场景：
- 需要频繁在两端插入/删除的场景
- 实现栈、队列、双端队列的底层数据结构
- 需要双向遍历的场景
"""

from typing import Optional, Iterator, Any
from core.exceptions import DataStructureException


class _Node:
    """
    双向链表节点类（私有类）
    
    每个节点存储一个元素和两个指针。
    
    属性：
        _element: 存储的数据元素
        _prev: 指向前一个节点的指针
        _next: 指向后一个节点的指针
    
    注意：
        使用 __slots__ 优化内存使用，禁止动态添加属性
    """
    __slots__ = ('_element', '_prev', '_next')
    
    def __init__(self, element: Any, prev: Optional['_Node'] = None, 
                 next_node: Optional['_Node'] = None):
        """
        初始化节点
        
        参数：
            element: 存储的数据元素
            prev: 前驱节点（默认为None）
            next_node: 后继节点（默认为None）
        """
        self._element = element
        self._prev = prev
        self._next = next_node
    
    def __repr__(self) -> str:
        """节点的字符串表示"""
        return f"Node({self._element})"


class DoublyLinkedList:
    """
    双向链表类
    
    使用哨兵节点（sentinel）简化边界条件处理：
    - _header: 头哨兵，不存储实际数据
    - _trailer: 尾哨兵，不存储实际数据
    
    优点：
    1. 插入和删除操作不需要特殊处理头尾边界
    2. 空链表状态更清晰
    3. 代码更简洁，减少bug
    
    示例：
        >>> dll = DoublyLinkedList()
        >>> dll.add_last(1)
        >>> dll.add_last(2)
        >>> dll.add_first(0)
        >>> print(dll)  # [0, 1, 2]
    """
    
    def __init__(self):
        """
        初始化空双向链表
        
        创建头尾哨兵节点，形成循环结构：
        header <-> trailer
        """
        self._header = _Node(None)  # 头哨兵
        self._trailer = _Node(None)  # 尾哨兵
        self._header._next = self._trailer
        self._trailer._prev = self._header
        self._size = 0
    
    def __len__(self) -> int:
        """返回链表中的元素数量"""
        return self._size
    
    def __repr__(self) -> str:
        """链表的字符串表示"""
        elements = [str(node._element) for node in self._traverse_forward()]
        return f"DoublyLinkedList([{', '.join(elements)}])"
    
    def __iter__(self) -> Iterator:
        """使链表可迭代"""
        return self._traverse_forward()
    
    def is_empty(self) -> bool:
        """
        检查链表是否为空
        
        返回：
            bool: 如果链表为空返回True
        """
        return self._size == 0
    
    def _traverse_forward(self) -> Iterator:
        """
        从前向后遍历链表（生成器）
        
        生成：
            Node: 链表中的每个节点（不包括哨兵）
        """
        current = self._header._next
        while current != self._trailer:
            yield current
            current = current._next
    
    def _traverse_backward(self) -> Iterator:
        """
        从后向前遍历链表（生成器）
        
        生成：
            Node: 链表中的每个节点（不包括哨兵）
        """
        current = self._trailer._prev
        while current != self._header:
            yield current
            current = current._prev
    
    def _insert_between(self, element: Any, 
                        predecessor: _Node, 
                        successor: _Node) -> _Node:
        """
        在两个节点之间插入新节点（内部方法）
        
        这是核心插入方法，其他插入方法都基于此实现。
        
        参数：
            element: 要插入的元素
            predecessor: 前驱节点
            successor: 后继节点
            
        返回：
            _Node: 新创建的节点
            
        时间复杂度：O(1)
        """
        newest = _Node(element, predecessor, successor)
        predecessor._next = newest
        successor._prev = newest
        self._size += 1
        return newest
    
    def _delete_node(self, node: _Node) -> Any:
        """
        删除指定节点（内部方法）
        
        这是核心删除方法，其他删除方法都基于此实现。
        
        参数：
            node: 要删除的节点
            
        返回：
            Any: 被删除节点存储的元素
            
        时间复杂度：O(1)
        """
        predecessor = node._prev
        successor = node._next
        predecessor._next = successor
        successor._prev = predecessor
        self._size -= 1
        
        # 清理删除节点的引用，帮助垃圾回收
        element = node._element
        node._prev = node._next = node._element = None
        return element
    
    # ========== 公共插入方法 ==========
    
    def add_first(self, element: Any) -> None:
        """
        在链表头部插入元素
        
        参数：
            element: 要插入的元素
            
        时间复杂度：O(1)
            
        示例：
            >>> dll.add_first(1)  # [1]
            >>> dll.add_first(0)  # [0, 1]
        """
        self._insert_between(element, self._header, self._header._next)
    
    def add_last(self, element: Any) -> None:
        """
        在链表尾部插入元素
        
        参数：
            element: 要插入的元素
            
        时间复杂度：O(1)
            
        示例：
            >>> dll.add_last(1)  # [1]
            >>> dll.add_last(2)  # [1, 2]
        """
        self._insert_between(element, self._trailer._prev, self._trailer)
    
    def insert_at(self, index: int, element: Any) -> None:
        """
        在指定位置插入元素
        
        参数：
            index: 插入位置（0-based）
            element: 要插入的元素
            
        异常：
            IndexError: 如果索引超出范围
            
        时间复杂度：O(n)，因为需要遍历到指定位置
            
        示例：
            >>> dll.insert_at(1, 5)  # 在位置1插入5
        """
        if index < 0 or index > self._size:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._size}]")
        
        if index == 0:
            self.add_first(element)
        elif index == self._size:
            self.add_last(element)
        else:
            current = self._header._next
            for _ in range(index):
                current = current._next
            self._insert_between(element, current._prev, current)
    
    # ========== 公共删除方法 ==========
    
    def delete_first(self) -> Any:
        """
        删除并返回链表头部元素
        
        返回：
            Any: 被删除的元素
            
        异常：
            DataStructureException: 如果链表为空
            
        时间复杂度：O(1)
        """
        if self.is_empty():
            raise DataStructureException("双向链表", "链表为空，无法删除")
        return self._delete_node(self._header._next)
    
    def delete_last(self) -> Any:
        """
        删除并返回链表尾部元素
        
        返回：
            Any: 被删除的元素
            
        异常：
            DataStructureException: 如果链表为空
            
        时间复杂度：O(1)
        """
        if self.is_empty():
            raise DataStructureException("双向链表", "链表为空，无法删除")
        return self._delete_node(self._trailer._prev)
    
    def delete_at(self, index: int) -> Any:
        """
        删除并返回指定位置的元素
        
        参数：
            index: 删除位置（0-based）
            
        返回：
            Any: 被删除的元素
            
        异常：
            IndexError: 如果索引超出范围
            
        时间复杂度：O(n)
        """
        if index < 0 or index >= self._size:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._size - 1}]")
        
        current = self._header._next
        for _ in range(index):
            current = current._next
        return self._delete_node(current)
    
    # ========== 访问方法 ==========
    
    def first(self) -> Any:
        """
        返回链表头部元素（不删除）
        
        返回：
            Any: 头部元素
            
        异常：
            DataStructureException: 如果链表为空
            
        时间复杂度：O(1)
        """
        if self.is_empty():
            raise DataStructureException("双向链表", "链表为空")
        return self._header._next._element
    
    def last(self) -> Any:
        """
        返回链表尾部元素（不删除）
        
        返回：
            Any: 尾部元素
            
        异常：
            DataStructureException: 如果链表为空
            
        时间复杂度：O(1)
        """
        if self.is_empty():
            raise DataStructureException("双向链表", "链表为空")
        return self._trailer._prev._element
    
    def get_at(self, index: int) -> Any:
        """
        返回指定位置的元素（不删除）
        
        参数：
            index: 位置索引（0-based）
            
        返回：
            Any: 该位置的元素
            
        异常：
            IndexError: 如果索引超出范围
            
        时间复杂度：O(n)
        """
        if index < 0 or index >= self._size:
            raise IndexError(f"索引 {index} 超出范围 [0, {self._size - 1}]")
        
        current = self._header._next
        for _ in range(index):
            current = current._next
        return current._element
    
    # ========== 搜索方法 ==========
    
    def find(self, element: Any) -> int:
        """
        查找元素首次出现的位置
        
        参数：
            element: 要查找的元素
            
        返回：
            int: 元素的位置索引，如果未找到返回-1
            
        时间复杂度：O(n)
        """
        for i, node in enumerate(self._traverse_forward()):
            if node._element == element:
                return i
        return -1
    
    def contains(self, element: Any) -> bool:
        """
        检查链表是否包含指定元素
        
        参数：
            element: 要检查的元素
            
        返回：
            bool: 如果包含返回True
            
        时间复杂度：O(n)
        """
        return self.find(element) != -1
    
    # ========== 转换方法 ==========
    
    def to_list(self) -> list:
        """
        将链表转换为Python列表
        
        返回：
            list: 包含所有元素的列表
        """
        return [node._element for node in self._traverse_forward()]
    
    def reverse(self) -> None:
        """
        就地反转链表
        
        时间复杂度：O(n)
        空间复杂度：O(1)
        """
        # 交换每个节点的前后指针
        current = self._header
        while current is not None:
            # 交换 prev 和 next
            current._prev, current._next = current._next, current._prev
            current = current._prev  # 移动到下一个节点（原来的next）
        
        # 交换 header 和 trailer
        self._header, self._trailer = self._trailer, self._header
