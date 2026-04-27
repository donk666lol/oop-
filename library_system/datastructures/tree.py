# -*- coding: utf-8 -*-
"""
通用树模块 - General Tree Module

树是一种非线性数据结构，由节点和边组成，具有层次关系。
本模块实现通用树（General Tree），每个节点可以有任意数量的子节点。

核心概念：
- 根节点（Root）：树的顶部节点
- 叶子节点（Leaf）：没有子节点的节点
- 内部节点（Internal）：有至少一个子节点的节点
- 子树（Subtree）：节点及其所有后代组成的树
- 深度（Depth）：从根到某节点的路径长度
- 高度（Height）：从某节点到其最远叶子节点的路径长度

时间复杂度分析：
- 查找：O(n) 最坏情况
- 插入：O(1) 如果已知父节点
- 遍历：O(n)
- 深度/高度计算：O(n)

空间复杂度：O(n)

本项目应用：
- 图书分类层次结构（如：文学 > 小说 > 科幻小说）
- 组织架构表示
- 菜单系统
"""

from typing import Any, Optional, Generic, TypeVar, Iterator, Callable
from dataclasses import dataclass, field
from core.exceptions import DataStructureException

T = TypeVar('T')


@dataclass
class TreeNode(Generic[T]):
    """
    树节点类
    
    属性：
        data: 节点存储的数据
        children: 子节点列表
        parent: 父节点（根节点为None）
    
    示例：
        >>> root = TreeNode("Root")
        >>> child1 = TreeNode("Child 1")
        >>> root.add_child(child1)
    """
    data: T
    children: list['TreeNode[T]'] = field(default_factory=list)
    parent: Optional['TreeNode[T]'] = None
    
    def __repr__(self) -> str:
        """节点的字符串表示"""
        return f"TreeNode({self.data})"
    
    def add_child(self, child: 'TreeNode[T]') -> None:
        """
        添加子节点
        
        参数：
            child: 要添加的子节点
        """
        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child: 'TreeNode[T]') -> bool:
        """
        移除子节点
        
        参数：
            child: 要移除的子节点
            
        返回：
            bool: 如果移除成功返回True
        """
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            return True
        return False
    
    def is_leaf(self) -> bool:
        """检查是否为叶子节点"""
        return len(self.children) == 0
    
    def is_root(self) -> bool:
        """检查是否为根节点"""
        return self.parent is None
    
    def get_depth(self) -> int:
        """返回节点的深度（根节点深度为0）"""
        depth = 0
        current = self.parent
        while current is not None:
            depth += 1
            current = current.parent
        return depth
    
    def get_height(self) -> int:
        """
        返回节点的高度（叶子节点高度为0）
        
        时间复杂度：O(n)，需要遍历子树
        """
        if self.is_leaf():
            return 0
        return 1 + max(child.get_height() for child in self.children)
    
    def get_path_to_root(self) -> list['TreeNode[T]']:
        """
        返回从当前节点到根节点的路径
        
        返回：
            list[TreeNode]: 路径上的节点列表（从当前到根）
        """
        path = []
        current: Optional[TreeNode[T]] = self
        while current is not None:
            path.append(current)
            current = current.parent
        return path
    
    def find_child_by_data(self, data: T) -> Optional['TreeNode[T]']:
        """
        查找包含指定数据的子节点
        
        参数：
            data: 要查找的数据
            
        返回：
            Optional[TreeNode]: 找到的子节点，如果不存在返回None
        """
        for child in self.children:
            if child.data == data:
                return child
        return None


class Tree(Generic[T]):
    """
    通用树类
    
    提供：添加、删除、查找、遍历等操作
    支持递归遍历
    
    示例：
        >>> tree = Tree[str]("Root")
        >>> tree.add_child("Child 1")
        >>> tree.add_child_to("Child 1", "Grandchild")
        >>> tree.find_node("Child 1")
    """
    
    def __init__(self, root_data: Optional[T] = None):
        """
        初始化树
        
        参数：
            root_data: 根节点的数据（可选）
        """
        self._root: Optional[TreeNode[T]] = None
        if root_data is not None:
            self._root = TreeNode(root_data)
        self._size = 1 if self._root else 0
    
    def __len__(self) -> int:
        """返回树中节点数量"""
        return self._size
    
    def __repr__(self) -> str:
        """树的字符串表示"""
        if self.is_empty():
            return "Tree(Empty)"
        return f"Tree(root={self._root.data}, size={self._size})"
    
    def __iter__(self) -> Iterator[T]:
        """使树可迭代（前序遍历）"""
        return (node.data for node in self.preorder_nodes())
    
    def is_empty(self) -> bool:
        """检查树是否为空"""
        return self._root is None
    
    @property
    def root(self) -> Optional[TreeNode[T]]:
        """返回根节点"""
        return self._root
    
    # ========== 插入操作 ==========
    
    def add_child(self, parent_data: T, child_data: T) -> bool:
        """
        找到包含parent_data的节点，添加子节点
        
        参数：
            parent_data: 父节点的数据
            child_data: 新子节点的数据
            
        返回：
            bool: 如果添加成功返回True
            
        时间复杂度：O(n) 需要查找父节点
        """
        parent = self.find_node(parent_data)
        if parent is None:
            return False
        
        parent.add_child(TreeNode(child_data))
        self._size += 1
        return True
    
    def add_child_to_node(self, parent: TreeNode[T], child_data: T) -> TreeNode[T]:
        """
        向指定节点添加子节点
        
        参数：
            parent: 父节点
            child_data: 新子节点的数据
            
        返回：
            TreeNode: 新创建的子节点
            
        时间复杂度：O(1)
        """
        child = TreeNode(child_data)
        parent.add_child(child)
        self._size += 1
        return child
    
    # ========== 查找操作 ==========
    
    def find_node(self, data: T) -> Optional[TreeNode[T]]:
        """
        查找包含指定数据的节点
        
        参数：
            data: 要查找的数据
            
        返回：
            Optional[TreeNode]: 找到的节点，如果不存在返回None
            
        时间复杂度：O(n)
        """
        return self._find_recursive(self._root, data)
    
    def _find_recursive(self, node: Optional[TreeNode[T]], data: T) -> Optional[TreeNode[T]]:
        """递归查找节点"""
        if node is None:
            return None
        if node.data == data:
            return node
        for child in node.children:
            result = self._find_recursive(child, data)
            if result is not None:
                return result
        return None
    
    def contains(self, data: T) -> bool:
        """
        检查树中是否包含指定数据
        
        参数：
            data: 要检查的数据
            
        返回：
            bool: 如果包含返回True
        """
        return self.find_node(data) is not None
    
    # ========== 遍历操作（递归实现） ==========
    
    def preorder_nodes(self) -> Iterator[TreeNode[T]]:
        """
        前序遍历（根-子节点）：返回节点
        
        应用：打印目录结构
        
        时间复杂度：O(n)
        """
        yield from self._preorder_recursive(self._root)
    
    def _preorder_recursive(self, node: Optional[TreeNode[T]]) -> Iterator[TreeNode[T]]:
        """递归前序遍历"""
        if node is not None:
            yield node
            for child in node.children:
                yield from self._preorder_recursive(child)
    
    def postorder_nodes(self) -> Iterator[TreeNode[T]]:
        """
        后序遍历（子节点-根）：返回节点
        
        应用：删除树（先删子节点）、计算目录大小
        
        时间复杂度：O(n)
        """
        yield from self._postorder_recursive(self._root)
    
    def _postorder_recursive(self, node: Optional[TreeNode[T]]) -> Iterator[TreeNode[T]]:
        """递归后序遍历"""
        if node is not None:
            for child in node.children:
                yield from self._postorder_recursive(child)
            yield node
    
    def level_order_nodes(self) -> Iterator[TreeNode[T]]:
        """
        层序遍历（BFS）：返回节点
        
        应用：按层打印树
        
        时间复杂度：O(n)
        空间复杂度：O(w)，w为最大宽度
        """
        if self._root is None:
            return
        
        from collections import deque
        queue = deque([self._root])
        
        while queue:
            node = queue.popleft()
            yield node
            queue.extend(node.children)
    
    # ========== 其他操作 ==========
    
    def get_depth(self) -> int:
        """
        返回树的深度（根节点深度为0）
        
        时间复杂度：O(n)
        """
        if self._root is None:
            return -1
        return self._root.get_height()
    
    def get_leaves(self) -> list[TreeNode[T]]:
        """
        返回所有叶子节点
        
        返回：
            list[TreeNode]: 叶子节点列表
            
        时间复杂度：O(n)
        """
        return [node for node in self.preorder_nodes() if node.is_leaf()]
    
    def get_path_to_node(self, data: T) -> list[TreeNode[T]]:
        """
        返回从根到指定节点的路径
        
        参数：
            data: 目标节点的数据
            
        返回：
            list[TreeNode]: 路径上的节点列表（从根到目标）
        """
        node = self.find_node(data)
        if node is None:
            return []
        path = node.get_path_to_root()
        path.reverse()  # 从根到节点
        return path
    
    def get_ancestors(self, data: T) -> list[TreeNode[T]]:
        """获取指定节点的所有祖先节点"""
        node = self.find_node(data)
        if node is None or node.parent is None:
            return []
        return node.get_path_to_root()[1:]  # 排除自己
    
    def get_siblings(self, data: T) -> list[TreeNode[T]]:
        """获取指定节点的所有兄弟节点"""
        node = self.find_node(data)
        if node is None or node.parent is None:
            return []
        return [child for child in node.parent.children if child != node]
    
    def count_nodes(self) -> int:
        """统计节点数量（用于验证）"""
        return sum(1 for _ in self.preorder_nodes())
    
    def count_leaves(self) -> int:
        """统计叶子节点数量"""
        return sum(1 for node in self.preorder_nodes() if node.is_leaf())
    
    def get_subtree(self, data: T) -> Optional['Tree[T]']:
        """
        获取以指定节点为根的子树
        
        参数：
            data: 子树根节点的数据
            
        返回：
            Optional[Tree]: 子树，如果节点不存在返回None
        """
        node = self.find_node(data)
        if node is None:
            return None
        
        # 创建新树，深拷贝节点结构
        def copy_subtree(source: TreeNode[T]) -> TreeNode[T]:
            new_node = TreeNode(source.data)
            for child in source.children:
                new_node.add_child(copy_subtree(child))
            return new_node
        
        new_tree = Tree[T]()
        new_tree._root = copy_subtree(node)
        new_tree._size = new_tree.count_nodes()
        return new_tree
    
    def print_tree(self, indent: int = 2) -> str:
        """
        返回树的缩进字符串表示
        
        参数：
            indent: 每层的缩进空格数
            
        返回：
            str: 树的字符串表示
        """
        if self._root is None:
            return "Empty Tree"
        
        lines = []
        
        def build_string(node: TreeNode[T], prefix: str = "", is_last: bool = True):
            connector = "└── " if is_last else "├── "
            lines.append(prefix + connector + str(node.data))
            
            for i, child in enumerate(node.children):
                is_last_child = (i == len(node.children) - 1)
                new_prefix = prefix + ("    " if is_last else "│   ")
                build_string(child, new_prefix, is_last_child)
        
        lines.append(str(self._root.data))
        for i, child in enumerate(self._root.children):
            build_string(child, "", i == len(self._root.children) - 1)
        
        return '\n'.join(lines)
    
    def clear(self) -> None:
        """清空树"""
        self._root = None
        self._size = 0


class CategoryTree(Tree[str]):
    """
    图书分类树（继承自通用树）
    
    专门用于管理图书分类层次结构
    
    示例：
        >>> category_tree = CategoryTree()
        >>> category_tree.add_category("文学", None)  # 添加根分类
        >>> category_tree.add_category("小说", "文学")  # 添加子分类
        >>> category_tree.add_category("科幻小说", "小说")
    """
    
    def __init__(self, root_name: str = "所有分类"):
        """初始化分类树"""
        super().__init__(root_name)
    
    def add_category(self, category_name: str, parent_name: str) -> bool:
        """
        添加分类
        
        参数：
            category_name: 新分类名称
            parent_name: 父分类名称
            
        返回：
            bool: 如果添加成功返回True
        """
        return self.add_child(parent_name, category_name)
    
    def get_all_categories(self) -> list[str]:
        """获取所有分类名称"""
        return [node.data for node in self.preorder_nodes()]
    
    def get_subcategories(self, category_name: str) -> list[str]:
        """获取指定分类的所有直接子分类"""
        node = self.find_node(category_name)
        if node is None:
            return []
        return [child.data for child in node.children]
    
    def get_category_path(self, category_name: str) -> list[str]:
        """获取分类的完整路径（从根到该分类）"""
        path = self.get_path_to_node(category_name)
        return [node.data for node in path]
