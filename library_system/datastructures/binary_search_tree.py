# -*- coding: utf-8 -*-
"""
二叉搜索树模块 - Binary Search Tree Module

二叉搜索树（BST）是一种特殊的二叉树，满足以下性质：
- 对于任意节点，左子树所有节点的值都小于该节点的值
- 对于任意节点，右子树所有节点的值都大于该节点的值
- 左右子树也都是二叉搜索树

时间复杂度分析（平均情况，树高h = log n）：
- 查找：O(log n)
- 插入：O(log n)
- 删除：O(log n)
- 遍历：O(n)

最坏情况（树退化为链表）：
- 所有操作：O(n)

空间复杂度：O(n)

本项目应用：
- 存储图书分类层次结构
- 按ID范围快速查询图书
- 实现排序输出功能
"""

from typing import Any, Optional, Callable, Generic, TypeVar, Iterator
from core.exceptions import DataStructureException

T = TypeVar('T')
K = TypeVar('K')


class TreeNode(Generic[T]):
    """
    二叉搜索树节点类
    
    属性：
        key: 节点的键值（用于比较和排序）
        value: 节点存储的数据
        left: 左子节点
        right: 右子节点
        parent: 父节点
    """
    
    def __init__(self, key: Any, value: T, 
                 parent: Optional['TreeNode[T]'] = None):
        """
        初始化节点
        
        参数：
            key: 节点的键值
            value: 节点存储的数据
            parent: 父节点（默认为None）
        """
        self.key = key
        self.value = value
        self.left: Optional[TreeNode[T]] = None
        self.right: Optional[TreeNode[T]] = None
        self.parent = parent
    
    def __repr__(self) -> str:
        """节点的字符串表示"""
        return f"TreeNode(key={self.key}, value={self.value})"
    
    def is_leaf(self) -> bool:
        """检查是否为叶子节点"""
        return self.left is None and self.right is None
    
    def has_left_child(self) -> bool:
        """检查是否有左子节点"""
        return self.left is not None
    
    def has_right_child(self) -> bool:
        """检查是否有右子节点"""
        return self.right is not None
    
    def has_any_child(self) -> bool:
        """检查是否有任意子节点"""
        return self.left is not None or self.right is not None
    
    def has_both_children(self) -> bool:
        """检查是否同时有左右子节点"""
        return self.left is not None and self.right is not None


class BinarySearchTree(Generic[T]):
    """
    二叉搜索树类
    
    提供：插入、查找、删除、遍历等操作
    支持递归和非递归遍历
    
    示例：
        >>> bst = BinarySearchTree()
        >>> bst.insert(50, "A")
        >>> bst.insert(30, "B")
        >>> bst.insert(70, "C")
        >>> bst.search(30)  # 返回 "B"
        >>> bst.delete(30)
        >>> bst.inorder()  # 返回 ["A", "C"]
    """
    
    def __init__(self):
        """初始化空二叉搜索树"""
        self._root: Optional[TreeNode[T]] = None
        self._size = 0
    
    def __len__(self) -> int:
        """返回树中节点数量"""
        return self._size
    
    def __repr__(self) -> str:
        """树的字符串表示"""
        elements = [str(node.value) for node in self.inorder_nodes()]
        return f"BST([{', '.join(elements)}])"
    
    def __iter__(self) -> Iterator[T]:
        """使树可迭代（中序遍历）"""
        for node in self.inorder_nodes():
            yield node.value
    
    def is_empty(self) -> bool:
        """检查树是否为空"""
        return self._root is None
    
    # ========== 插入操作 ==========
    
    def insert(self, key: Any, value: T) -> None:
        """
        插入键值对
        
        如果键已存在，更新对应的值；否则创建新节点。
        
        参数：
            key: 键值
            value: 存储的值
            
        时间复杂度：O(h)，h为树高
            
        示例：
            >>> bst.insert(50, "Root")
            >>> bst.insert(30, "Left")
        """
        if self.is_empty():
            self._root = TreeNode(key, value)
            self._size = 1
        else:
            self._insert_node(self._root, key, value)
    
    def _insert_node(self, node: TreeNode[T], key: Any, value: T) -> None:
        """
        递归插入辅助方法
        
        参数：
            node: 当前节点
            key: 键值
            value: 存储的值
        """
        if key == node.key:
            # 键已存在，更新值
            node.value = value
        elif key < node.key:
            if node.left is None:
                node.left = TreeNode(key, value, parent=node)
                self._size += 1
            else:
                self._insert_node(node.left, key, value)
        else:
            if node.right is None:
                node.right = TreeNode(key, value, parent=node)
                self._size += 1
            else:
                self._insert_node(node.right, key, value)
    
    # ========== 查找操作 ==========
    
    def search(self, key: Any) -> Optional[T]:
        """
        查找指定键对应的值
        
        参数：
            key: 要查找的键
            
        返回：
            Optional[T]: 找到的值，如果不存在返回None
            
        时间复杂度：O(h)
            
        示例：
            >>> bst.search(50)  # 返回对应的值或None
        """
        node = self._find_node(key)
        return node.value if node else None
    
    def _find_node(self, key: Any) -> Optional[TreeNode[T]]:
        """
        查找指定键对应的节点（内部方法）
        
        参数：
            key: 要查找的键
            
        返回：
            Optional[TreeNode]: 找到的节点，如果不存在返回None
        """
        current = self._root
        while current is not None:
            if key == current.key:
                return current
            elif key < current.key:
                current = current.left
            else:
                current = current.right
        return None
    
    def contains(self, key: Any) -> bool:
        """
        检查是否包含指定键
        
        参数：
            key: 要检查的键
            
        返回：
            bool: 如果包含返回True
            
        时间复杂度：O(h)
        """
        return self._find_node(key) is not None
    
    # ========== 删除操作 ==========
    
    def delete(self, key: Any) -> Optional[T]:
        """
        删除指定键对应的节点
        
        参数：
            key: 要删除的键
            
        返回：
            Optional[T]: 被删除节点的值，如果键不存在返回None
            
        时间复杂度：O(h)
            
        示例：
            >>> bst.delete(50)  # 删除键为50的节点
        """
        node = self._find_node(key)
        if node is None:
            return None
        
        value = node.value
        
        if node.is_leaf():
            self._delete_leaf(node)
        elif node.has_both_children():
            self._delete_internal(node)
        else:
            self._delete_one_child(node)
        
        self._size -= 1
        return value
    
    def _delete_leaf(self, node: TreeNode[T]) -> None:
        """删除叶子节点"""
        if node.parent is None:
            self._root = None
        elif node == node.parent.left:
            node.parent.left = None
        else:
            node.parent.right = None
    
    def _delete_one_child(self, node: TreeNode[T]) -> None:
        """删除只有一个子节点的节点"""
        child = node.left if node.left else node.right
        
        if node.parent is None:
            self._root = child
        elif node == node.parent.left:
            node.parent.left = child
        else:
            node.parent.right = child
        
        if child:
            child.parent = node.parent
    
    def _delete_internal(self, node: TreeNode[T]) -> None:
        """
        删除有两个子节点的内部节点
        
        策略：找到右子树的最小节点（后继），用其替换当前节点
        """
        successor = self._find_min_node(node.right)
        node.key = successor.key
        node.value = successor.value
        
        # 删除后继节点（它最多有一个右子节点）
        if successor.is_leaf():
            self._delete_leaf(successor)
        else:
            self._delete_one_child(successor)
    
    def _find_min_node(self, node: TreeNode[T]) -> TreeNode[T]:
        """找到子树中的最小节点（最左节点）"""
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def _find_max_node(self, node: TreeNode[T]) -> TreeNode[T]:
        """找到子树中的最大节点（最右节点）"""
        current = node
        while current.right is not None:
            current = current.right
        return current
    
    # ========== 遍历操作（递归实现） ==========
    
    def inorder_nodes(self) -> Iterator[TreeNode[T]]:
        """
        中序遍历（左-根-右），返回节点
        
        特点：按键值升序输出
        
        时间复杂度：O(n)
        
        示例：
            >>> for node in bst.inorder_nodes():
            ...     print(node.key, node.value)
        """
        yield from self._inorder_recursive(self._root)
    
    def _inorder_recursive(self, node: Optional[TreeNode[T]]) -> Iterator[TreeNode[T]]:
        """递归中序遍历"""
        if node is not None:
            yield from self._inorder_recursive(node.left)
            yield node
            yield from self._inorder_recursive(node.right)
    
    def preorder_nodes(self) -> Iterator[TreeNode[T]]:
        """
        前序遍历（根-左-右），返回节点
        
        应用：复制树结构、打印目录结构
        
        时间复杂度：O(n)
        """
        yield from self._preorder_recursive(self._root)
    
    def _preorder_recursive(self, node: Optional[TreeNode[T]]) -> Iterator[TreeNode[T]]:
        """递归前序遍历"""
        if node is not None:
            yield node
            yield from self._preorder_recursive(node.left)
            yield from self._preorder_recursive(node.right)
    
    def postorder_nodes(self) -> Iterator[TreeNode[T]]:
        """
        后序遍历（左-右-根），返回节点
        
        应用：删除树（先删子树）、计算目录大小
        
        时间复杂度：O(n)
        """
        yield from self._postorder_recursive(self._root)
    
    def _postorder_recursive(self, node: Optional[TreeNode[T]]) -> Iterator[TreeNode[T]]:
        """递归后序遍历"""
        if node is not None:
            yield from self._postorder_recursive(node.left)
            yield from self._postorder_recursive(node.right)
            yield node
    
    # ========== 范围查询 ==========
    
    def range_search(self, low: Any, high: Any) -> list[T]:
        """
        范围查询：返回键在[low, high]范围内的所有值
        
        参数：
            low: 范围下界（包含）
            high: 范围上界（包含）
            
        返回：
            list[T]: 范围内的值列表（按键升序）
            
        时间复杂度：O(k + h)，k为结果数量，h为树高
            
        示例：
            >>> bst.range_search(30, 70)  # 返回键在30到70之间的所有值
        """
        result = []
        self._range_search_recursive(self._root, low, high, result)
        return result
    
    def _range_search_recursive(self, node: Optional[TreeNode[T]], 
                                 low: Any, high: Any, result: list) -> None:
        """递归范围查询"""
        if node is None:
            return
        
        # 如果当前节点的键大于下界，搜索左子树
        if node.key > low:
            self._range_search_recursive(node.left, low, high, result)
        
        # 如果当前节点的键在范围内，添加到结果
        if low <= node.key <= high:
            result.append(node.value)
        
        # 如果当前节点的键小于上界，搜索右子树
        if node.key < high:
            self._range_search_recursive(node.right, low, high, result)
    
    # ========== 其他操作 ==========
    
    def min_key(self) -> Optional[Any]:
        """返回最小键"""
        if self.is_empty():
            return None
        return self._find_min_node(self._root).key
    
    def max_key(self) -> Optional[Any]:
        """返回最大键"""
        if self.is_empty():
            return None
        return self._find_max_node(self._root).key
    
    def get_height(self) -> int:
        """
        返回树的高度（递归实现）
        
        时间复杂度：O(n)
        """
        return self._height_recursive(self._root)
    
    def _height_recursive(self, node: Optional[TreeNode[T]]) -> int:
        """递归计算高度"""
        if node is None:
            return -1
        return 1 + max(self._height_recursive(node.left), 
                       self._height_recursive(node.right))
    
    def clear(self) -> None:
        """清空树"""
        self._root = None
        self._size = 0
    
    def to_sorted_list(self) -> list[T]:
        """
        将树转换为按键升序排列的列表
        
        返回：
            list[T]: 升序排列的值列表
        """
        return [node.value for node in self.inorder_nodes()]
    
    def count_nodes(self) -> int:
        """递归计算节点数量（用于验证）"""
        return self._count_recursive(self._root)
    
    def _count_recursive(self, node: Optional[TreeNode[T]]) -> int:
        """递归计数"""
        if node is None:
            return 0
        return 1 + self._count_recursive(node.left) + self._count_recursive(node.right)
