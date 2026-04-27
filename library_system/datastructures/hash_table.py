# -*- coding: utf-8 -*-
"""
哈希表模块 - Hash Table Module

哈希表（Hash Table）是一种基于键值对的高效数据结构。
通过哈希函数将键映射到数组索引，实现快速查找。

核心概念：
- 哈希函数：将键转换为数组索引的函数
- 冲突解决：当多个键映射到同一索引时的处理方法
- 负载因子：元素数量/数组大小，影响性能

时间复杂度分析（平均情况）：
- 查找：O(1)
- 插入：O(1)
- 删除：O(1)

最坏情况（所有键冲突）：
- 所有操作：O(n)

空间复杂度：O(n)

冲突解决方法：
1. 链地址法（Separate Chaining）：每个槽位维护一个链表
2. 开放地址法（Open Addressing）：寻找下一个空槽位

本项目使用链地址法实现。

本项目应用：
- 存储图书信息（以ISBN/ID为键）
- 用户信息快速查找
- 借阅记录索引
"""

from typing import Any, Optional, Generic, TypeVar, Iterator
from dataclasses import dataclass
from core.exceptions import DataStructureException

K = TypeVar('K')
V = TypeVar('V')


@dataclass
class HashEntry(Generic[K, V]):
    """
    哈希表条目类
    
    存储键值对，以及指向下一个条目的指针（用于链地址法）。
    
    属性：
        key: 键
        value: 值
        next: 指向下一个条目（链地址法）
    """
    key: K
    value: V
    next: Optional['HashEntry[K, V]'] = None


class HashTable(Generic[K, V]):
    """
    哈希表类（链地址法实现）
    
    特点：
    - 使用链地址法解决冲突
    - 支持动态扩容
    - 提供完整的CRUD操作
    
    示例：
        >>> ht = HashTable[str, Book]()
        >>> ht.insert("ISBN001", book1)
        >>> ht.get("ISBN001")  # 返回 book1
        >>> ht.remove("ISBN001")
        >>> len(ht)  # 返回 0
    """
    
    DEFAULT_CAPACITY = 16  # 默认初始容量
    LOAD_FACTOR_THRESHOLD = 0.75  # 扩容阈值
    
    def __init__(self, initial_capacity: int = DEFAULT_CAPACITY):
        """
        初始化哈希表
        
        参数：
            initial_capacity: 初始容量（默认16）
        """
        self._capacity = initial_capacity
        self._size = 0
        # 桶数组，每个元素是一个链表头指针
        self._buckets: list[Optional[HashEntry[K, V]]] = [None] * self._capacity
    
    def __len__(self) -> int:
        """返回哈希表中元素数量"""
        return self._size
    
    def __repr__(self) -> str:
        """哈希表的字符串表示"""
        pairs = []
        for key, value in self.items():
            pairs.append(f"{key}: {value}")
        return f"HashTable({{{', '.join(pairs)}}})"
    
    def __contains__(self, key: K) -> bool:
        """支持 'key in hashtable' 语法"""
        return self.contains(key)
    
    def __getitem__(self, key: K) -> V:
        """支持 'hashtable[key]' 语法"""
        value = self.get(key)
        if value is None:
            raise KeyError(f"键 '{key}' 不存在")
        return value
    
    def __setitem__(self, key: K, value: V) -> None:
        """支持 'hashtable[key] = value' 语法"""
        self.insert(key, value)
    
    def __delitem__(self, key: K) -> None:
        """支持 'del hashtable[key]' 语法"""
        if not self.remove(key):
            raise KeyError(f"键 '{key}' 不存在")
    
    def _hash(self, key: K) -> int:
        """
        计算键的哈希值（内部方法）
        
        使用Python内置hash函数，并对容量取模
        
        参数：
            key: 要哈希的键
            
        返回：
            int: 桶索引
        """
        # 使用位运算确保结果为正数
        return hash(key) & 0x7FFFFFFF % self._capacity
    
    def _get_load_factor(self) -> float:
        """
        计算当前负载因子
        
        返回：
            float: 负载因子
        """
        return self._size / self._capacity
    
    def _resize(self, new_capacity: int) -> None:
        """
        扩容/缩容（内部方法）
        
        参数：
            new_capacity: 新的容量
            
        时间复杂度：O(n)，需要重新哈希所有元素
        """
        old_buckets = self._buckets
        self._capacity = new_capacity
        self._buckets = [None] * new_capacity
        self._size = 0
        
        # 重新插入所有元素
        for head in old_buckets:
            current = head
            while current is not None:
                self.insert(current.key, current.value)
                current = current.next
    
    # ========== 核心操作 ==========
    
    def insert(self, key: K, value: V) -> None:
        """
        插入或更新键值对
        
        如果键已存在，更新对应的值；否则创建新条目。
        
        参数：
            key: 键
            value: 值
            
        时间复杂度：平均O(1)，最坏O(n)
            
        示例：
            >>> ht.insert("B001", book1)  # 插入新条目
            >>> ht.insert("B001", book2)  # 更新现有条目
        """
        index = self._hash(key)
        
        if self._buckets[index] is None:
            # 桶为空，直接插入
            self._buckets[index] = HashEntry(key, value)
            self._size += 1
        else:
            # 桶不为空，查找或追加
            current = self._buckets[index]
            while True:
                if current.key == key:
                    # 键已存在，更新值
                    current.value = value
                    return
                if current.next is None:
                    break
                current = current.next
            # 在链表末尾添加新条目
            current.next = HashEntry(key, value)
            self._size += 1
        
        # 检查是否需要扩容
        if self._get_load_factor() > self.LOAD_FACTOR_THRESHOLD:
            self._resize(2 * self._capacity)
    
    def get(self, key: K) -> Optional[V]:
        """
        获取指定键对应的值
        
        参数：
            key: 要查找的键
            
        返回：
            Optional[V]: 对应的值，如果键不存在返回None
            
        时间复杂度：平均O(1)，最坏O(n)
            
        示例：
            >>> book = ht.get("B001")  # 返回对应的book或None
        """
        index = self._hash(key)
        current = self._buckets[index]
        
        while current is not None:
            if current.key == key:
                return current.value
            current = current.next
        
        return None
    
    def remove(self, key: K) -> Optional[V]:
        """
        删除指定键对应的条目
        
        参数：
            key: 要删除的键
            
        返回：
            Optional[V]: 被删除的值，如果键不存在返回None
            
        时间复杂度：平均O(1)，最坏O(n)
            
        示例：
            >>> book = ht.remove("B001")  # 删除并返回对应的值
        """
        index = self._hash(key)
        
        if self._buckets[index] is None:
            return None
        
        current = self._buckets[index]
        
        # 处理链表头节点
        if current.key == key:
            self._buckets[index] = current.next
            self._size -= 1
            return current.value
        
        # 处理链表中的其他节点
        while current.next is not None:
            if current.next.key == key:
                value = current.next.value
                current.next = current.next.next
                self._size -= 1
                return value
            current = current.next
        
        return None
    
    def contains(self, key: K) -> bool:
        """
        检查是否包含指定键
        
        参数：
            key: 要检查的键
            
        返回：
            bool: 如果包含返回True
            
        时间复杂度：平均O(1)
        """
        return self.get(key) is not None
    
    def update(self, key: K, value: V) -> bool:
        """
        更新指定键的值
        
        参数：
            key: 要更新的键
            value: 新值
            
        返回：
            bool: 如果键存在并更新成功返回True
            
        时间复杂度：平均O(1)
        """
        index = self._hash(key)
        current = self._buckets[index]
        
        while current is not None:
            if current.key == key:
                current.value = value
                return True
            current = current.next
        
        return False
    
    # ========== 遍历操作 ==========
    
    def keys(self) -> Iterator[K]:
        """
        返回所有键的迭代器
        
        生成：
            K: 哈希表中的每个键
        """
        for head in self._buckets:
            current = head
            while current is not None:
                yield current.key
                current = current.next
    
    def values(self) -> Iterator[V]:
        """
        返回所有值的迭代器
        
        生成：
            V: 哈希表中的每个值
        """
        for head in self._buckets:
            current = head
            while current is not None:
                yield current.value
                current = current.next
    
    def items(self) -> Iterator[tuple[K, V]]:
        """
        返回所有键值对的迭代器
        
        生成：
            tuple[K, V]: 每个键值对
        """
        for head in self._buckets:
            current = head
            while current is not None:
                yield (current.key, current.value)
                current = current.next
    
    # ========== 其他操作 ==========
    
    def clear(self) -> None:
        """清空哈希表"""
        self._buckets = [None] * self._capacity
        self._size = 0
    
    def is_empty(self) -> bool:
        """检查哈希表是否为空"""
        return self._size == 0
    
    def to_dict(self) -> dict:
        """
        将哈希表转换为Python字典
        
        返回：
            dict: 包含所有键值对的字典
        """
        return dict(self.items())
    
    def get_bucket_distribution(self) -> list[int]:
        """
        获取桶分布信息（用于性能分析）
        
        返回：
            list[int]: 每个桶的元素数量
        """
        distribution = []
        for head in self._buckets:
            count = 0
            current = head
            while current is not None:
                count += 1
                current = current.next
            distribution.append(count)
        return distribution
    
    def get_statistics(self) -> dict:
        """
        获取哈希表统计信息
        
        返回：
            dict: 包含容量、大小、负载因子等统计信息
        """
        distribution = self.get_bucket_distribution()
        non_empty_buckets = sum(1 for count in distribution if count > 0)
        
        return {
            'capacity': self._capacity,
            'size': self._size,
            'load_factor': self._get_load_factor(),
            'non_empty_buckets': non_empty_buckets,
            'max_chain_length': max(distribution) if distribution else 0,
            'avg_chain_length': sum(distribution) / non_empty_buckets if non_empty_buckets > 0 else 0
        }
    
    @classmethod
    def from_dict(cls, dictionary: dict[K, V], capacity: Optional[int] = None) -> 'HashTable[K, V]':
        """
        从字典创建哈希表
        
        参数：
            dictionary: 源字典
            capacity: 初始容量（可选）
            
        返回：
            HashTable: 新创建的哈希表
        """
        if capacity is None:
            capacity = max(cls.DEFAULT_CAPACITY, len(dictionary) * 2)
        
        ht = cls(capacity)
        for key, value in dictionary.items():
            ht.insert(key, value)
        
        return ht
