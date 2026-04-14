# -*- coding: utf-8 -*-
"""
队列模块 - Queue Module

队列是一种先进先出（FIFO: First In First Out）的线性数据结构。
类似于排队等候，先来的人先接受服务。

核心操作：
- enqueue(e): 在队尾插入元素
- dequeue(): 移除并返回队首元素
- first(): 返回队首元素（不删除）
- is_empty(): 检查队列是否为空
- len(): 返回队列中元素数量

时间复杂度分析：
- enqueue: O(1) 均摊
- dequeue: O(1) 均摊
- first: O(1)
- is_empty: O(1)

空间复杂度：O(n)

应用场景：
- 任务调度（打印队列、CPU调度）
- 广度优先搜索（BFS）
- 消息缓冲区
- 客服系统排队

本项目应用：
- 管理图书预约队列
- 处理借阅请求队列
- 系统消息队列
"""

from typing import Any, Optional, Generic, TypeVar, Iterator
from core.exceptions import DataStructureException

T = TypeVar('T')


class ArrayQueue(Generic[T]):
    """
    基于循环数组实现的队列
    
    使用循环数组避免元素移动：
    - _front: 指向队首元素的索引
    - _size: 队列中元素数量
    - 队尾位置计算：(front + size) % capacity
    
    优点：
    - 所有操作O(1)
    - 空间利用率高
    - 无需元素移动
    
    示例：
        >>> queue = ArrayQueue[int]()
        >>> queue.enqueue(1)
        >>> queue.enqueue(2)
        >>> queue.first()    # 返回 1
        >>> queue.dequeue()  # 返回 1
        >>> len(queue)       # 返回 1
    """
    
    DEFAULT_CAPACITY = 10  # 默认初始容量
    
    def __init__(self, initial_capacity: int = DEFAULT_CAPACITY):
        """
        初始化空队列
        
        参数：
            initial_capacity: 初始容量（默认10）
        """
        self._data: list[Optional[T]] = [None] * initial_capacity
        self._size = 0
        self._front = 0
    
    def __len__(self) -> int:
        """返回队列中元素数量"""
        return self._size
    
    def __repr__(self) -> str:
        """队列的字符串表示"""
        elements = [str(self._data[(self._front + i) % len(self._data)]) 
                   for i in range(self._size)]
        return f"Queue([{', '.join(elements)}] <- 队尾)"
    
    def __iter__(self) -> Iterator[T]:
        """使队列可迭代（从队首到队尾）"""
        for i in range(self._size):
            yield self._data[(self._front + i) % len(self._data)]
    
    def is_empty(self) -> bool:
        """
        检查队列是否为空
        
        返回：
            bool: 如果队列为空返回True
        """
        return self._size == 0
    
    def _resize(self, new_capacity: int) -> None:
        """
        调整队列容量（内部方法）
        
        将元素重新排列到新数组的前面部分。
        
        参数：
            new_capacity: 新的容量大小
            
        时间复杂度：O(n)
        """
        old_data = self._data
        self._data = [None] * new_capacity
        
        # 将元素从旧数组复制到新数组
        for i in range(self._size):
            self._data[i] = old_data[(self._front + i) % len(old_data)]
        
        self._front = 0
    
    def enqueue(self, element: T) -> None:
        """
        在队尾插入元素
        
        参数：
            element: 要插入的元素
            
        时间复杂度：O(1) 均摊
            
        示例：
            >>> queue.enqueue(1)  # 队列：[1]
            >>> queue.enqueue(2)  # 队列：[1, 2]
        """
        # 如果队列满了，扩容为原来的2倍
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        
        # 计算队尾位置
        rear = (self._front + self._size) % len(self._data)
        self._data[rear] = element
        self._size += 1
    
    def dequeue(self) -> T:
        """
        移除并返回队首元素
        
        返回：
            T: 队首元素
            
        异常：
            DataStructureException: 如果队列为空
            
        时间复杂度：O(1) 均摊
            
        示例：
            >>> queue.dequeue()  # 返回并删除队首元素
        """
        if self.is_empty():
            raise DataStructureException("队列", "队列为空，无法出队")
        
        element = self._data[self._front]
        self._data[self._front] = None  # 帮助垃圾回收
        
        # 更新队首索引
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1
        
        # 如果元素数量少于容量的1/4且容量大于默认值，缩容为一半
        if self._size > 0 and self._size < len(self._data) // 4:
            if len(self._data) > self.DEFAULT_CAPACITY:
                self._resize(max(self.DEFAULT_CAPACITY, len(self._data) // 2))
        
        return element
    
    def first(self) -> T:
        """
        返回队首元素（不删除）
        
        返回：
            T: 队首元素
            
        异常：
            DataStructureException: 如果队列为空
            
        时间复杂度：O(1)
        """
        if self.is_empty():
            raise DataStructureException("队列", "队列为空")
        return self._data[self._front]
    
    def last(self) -> T:
        """
        返回队尾元素（不删除）
        
        返回：
            T: 队尾元素
            
        异常：
            DataStructureException: 如果队列为空
            
        时间复杂度：O(1)
        """
        if self.is_empty():
            raise DataStructureException("队列", "队列为空")
        rear = (self._front + self._size - 1) % len(self._data)
        return self._data[rear]
    
    def clear(self) -> None:
        """清空队列"""
        self._data = [None] * self.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0
    
    def to_list(self) -> list:
        """
        将队列转换为列表（队首在前）
        
        返回：
            list: 包含队列中所有元素的列表
        """
        return list(self)
    
    def rotate(self, k: int) -> None:
        """
        循环移动队列元素
        
        将队首的k个元素移动到队尾。
        
        参数：
            k: 要移动的元素数量
            
        时间复杂度：O(k)
            
        示例：
            >>> queue = Queue([1, 2, 3, 4, 5])
            >>> queue.rotate(2)
            >>> queue.to_list()  # [3, 4, 5, 1, 2]
        """
        if k <= 0 or k >= self._size:
            return
        
        for _ in range(k):
            self.enqueue(self.dequeue())


class CircularQueue(Generic[T]):
    """
    循环队列（无头尾哨兵的循环链表实现）
    
    适用于轮询调度（Round-Robin Scheduling）场景。
    
    特点：
    - 每个元素都有机会被服务
    - 服务后元素可以回到队尾继续等待
    
    应用场景：
    - CPU时间片轮转
    - 多用户系统资源分配
    - 图书预约轮询处理
    
    示例：
        >>> cq = CircularQueue()
        >>> cq.add(User("Alice"))
        >>> cq.add(User("Bob"))
        >>> current = cq.advance()  # Alice获得服务，然后移到队尾
    """
    
    class _Node:
        """循环链表节点"""
        __slots__ = ('_element', '_next')
        
        def __init__(self, element: T, next_node: Optional['CircularQueue._Node'] = None):
            self._element = element
            self._next = next_node
    
    def __init__(self):
        """初始化空循环队列"""
        self._tail: Optional[CircularQueue._Node] = None
        self._size = 0
    
    def __len__(self) -> int:
        """返回队列中元素数量"""
        return self._size
    
    def is_empty(self) -> bool:
        """检查队列是否为空"""
        return self._size == 0
    
    def first(self) -> T:
        """返回队首元素（不删除）"""
        if self.is_empty():
            raise DataStructureException("循环队列", "队列为空")
        return self._tail._next._element
    
    def add(self, element: T) -> None:
        """
        在队尾添加元素
        
        参数：
            element: 要添加的元素
            
        时间复杂度：O(1)
        """
        newest = self._Node(element)
        
        if self.is_empty():
            newest._next = newest  # 指向自己形成循环
        else:
            newest._next = self._tail._next
            self._tail._next = newest
        
        self._tail = newest
        self._size += 1
    
    def dequeue(self) -> T:
        """
        移除并返回队首元素
        
        返回：
            T: 队首元素
            
        时间复杂度：O(1)
        """
        if self.is_empty():
            raise DataStructureException("循环队列", "队列为空")
        
        head = self._tail._next
        
        if self._size == 1:
            self._tail = None
        else:
            self._tail._next = head._next
        
        self._size -= 1
        return head._element
    
    def rotate(self) -> None:
        """
        将队首元素移到队尾
        
        时间复杂度：O(1)
        """
        if not self.is_empty():
            self._tail = self._tail._next
