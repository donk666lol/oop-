from typing import Any, Optional, Callable, Generic, TypeVar, Iterator
from ..core.exceptions import DataStructureException

T = TypeVar('T')
K = TypeVar('K')


class TreeNode(Generic[T]):
   
    
    def __init__(self, key: Any, value: T, 
                 parent: Optional['TreeNode[T]'] = None):
       
        self.key = key
        self.value = value
        self.left: Optional['TreeNode[T]'] = None
        self.right: Optional['TreeNode[T]'] = None
        self.parent = parent
    
    def is_leaf(self) -> bool:
        
        return self.left is None and self.right is None
    
    def has_one_child(self) -> bool:
       
        return (self.left is not None and self.right is None) or \
               (self.left is None and self.right is not None)
    
    def has_two_children(self) -> bool:
       
        return self.left is not None and self.right is not None


class BinarySearchTree(Generic[T]):
    
    def __init__(self, key_func: Optional[Callable[[T], Any]] = None):
       
        self._root: Optional[TreeNode[T]] = None
        self._size = 0
        self._key_func = key_func if key_func else lambda x: x
    
    def __len__(self) -> int:
        """返回树中节点数量"""
        return self._size
    
    def is_empty(self) -> bool:
        """检查树是否为空"""
        return self._root is None
    
    def insert(self, key: Any, value: T) -> None:
       
        if self._root is None:
            self._root = TreeNode(key, value)
            self._size = 1
        else:
            self._insert(self._root, key, value)
    
    def _insert(self, node: TreeNode[T], key: Any, value: T) -> None:
        """递归插入辅助方法"""
        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key, value, node)
                self._size += 1
            else:
                self._insert(node.left, key, value)
        elif key > node.key:
            if node.right is None:
                node.right = TreeNode(key, value, node)
                self._size += 1
            else:
                self._insert(node.right, key, value)
        else:
            raise DataStructureException("Key already exists")
    
    def search(self, key: Any) -> Optional[T]:
       
        node = self._search(self._root, key)
        return node.value if node else None
    
    def _search(self, node: Optional[TreeNode[T]], key: Any) -> Optional[TreeNode[T]]:
        """递归查找辅助方法"""
        if node is None:
            return None
        if key == node.key:
            return node
        elif key < node.key:
            return self._search(node.left, key)
        else:
            return self._search(node.right, key)
    
    def contains(self, key: Any) -> bool:
       
        return self._search(self._root, key) is not None
    
    def delete(self, key: Any) -> Optional[T]:
       
        node = self._search(self._root, key)
        if node is None:
            return None
        
        value = node.value
        self._delete(node)
        return value
    
    def _delete(self, node: TreeNode[T]) -> None:
      
        if node.is_leaf():
            # 叶节点
            if node == self._root:
                self._root = None
            elif node == node.parent.left:
                node.parent.left = None
            else:
                node.parent.right = None
            self._size -= 1
        elif node.has_one_child():
            # 只有一个子节点
            child = node.left if node.left else node.right
            if node == self._root:
                self._root = child
                child.parent = None
            elif node == node.parent.left:
                node.parent.left = child
                child.parent = node.parent
            else:
                node.parent.right = child
                child.parent = node.parent
            self._size -= 1
        else:
            # 有两个子节点，找右子树的最小节点
            successor = self._find_min(node.right)
            node.key = successor.key
            node.value = successor.value
            self._delete(successor)
    
    def _find_min(self, node: TreeNode[T]) -> TreeNode[T]:
       
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def in_order(self) -> Iterator[T]:
        
        yield from self._in_order(self._root)
    
    def _in_order(self, node: Optional[TreeNode[T]]) -> Iterator[T]:
        """递归中序遍历辅助方法"""
        if node is not None:
            yield from self._in_order(node.left)
            yield node.value
            yield from self._in_order(node.right)
    
    def pre_order(self) -> Iterator[T]:
       
        yield from self._pre_order(self._root)
    
    def _pre_order(self, node: Optional[TreeNode[T]]) -> Iterator[T]:
        """递归前序遍历辅助方法"""
        if node is not None:
            yield node.value
            yield from self._pre_order(node.left)
            yield from self._pre_order(node.right)
    
    def post_order(self) -> Iterator[T]:
       
        yield from self._post_order(self._root)
    
    def _post_order(self, node: Optional[TreeNode[T]]) -> Iterator[T]:
        """递归后序遍历辅助方法"""
        if node is not None:
            yield from self._post_order(node.left)
            yield from self._post_order(node.right)
            yield node.value
    
    def range_search(self, low: Any, high: Any) -> Iterator[T]:
       
        yield from self._range_search(self._root, low, high)
    
    def _range_search(self, node: Optional[TreeNode[T]], low: Any, high: Any) -> Iterator[T]:
        """递归范围查询辅助方法"""
        if node is not None:
            if node.key > low:
                yield from self._range_search(node.left, low, high)
            if low <= node.key <= high:
                yield node.value
            if node.key < high:
                yield from self._range_search(node.right, low, high)
    
    def get_height(self) -> int:
       
        return self._height(self._root)
    
    def _height(self, node: Optional[TreeNode[T]]) -> int:
        """递归计算高度辅助方法"""
        if node is None:
            return -1
        return 1 + max(self._height(node.left), self._height(node.right))
    
    def clear(self) -> None:
        """清空树"""
        self._root = None
        self._size = 0
    
    def to_sorted_list(self) -> list[T]:
        return list(self.in_order())
