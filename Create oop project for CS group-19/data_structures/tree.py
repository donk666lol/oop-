from typing import Any, Optional, Generic, TypeVar, Iterator, Callable
from dataclasses import dataclass, field
from ..core.exceptions import DataStructureException

T = TypeVar('T')


@dataclass
class TreeNode(Generic[T]):
   
    data: T
    children: list['TreeNode[T]'] = field(default_factory=list)
    parent: Optional['TreeNode[T]'] = None
    
    def add_child(self, child: 'TreeNode[T]') -> None:
        
        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child: 'TreeNode[T]') -> bool:
       
        if child in self.children:
            child.parent = None
            self.children.remove(child)
            return True
        return False
    
    def get_child(self, index: int) -> Optional['TreeNode[T]']:
        
        if 0 <= index < len(self.children):
            return self.children[index]
        return None
    
    def is_leaf(self) -> bool:
        
        return len(self.children) == 0
    
    def depth(self) -> int:
        
        depth = 0
        node = self.parent
        while node is not None:
            depth += 1
            node = node.parent
        return depth


class Tree(Generic[T]):
   
    
    def __init__(self, root_data: T):
       
        self._root = TreeNode(root_data)
    
    @property
    def root(self) -> TreeNode[T]:
        """获取根节点"""
        return self._root
    
    def is_empty(self) -> bool:
       
        return self._root is None
    
    def height(self) -> int:
       
        return self._height(self._root)
    
    def _height(self, node: Optional[TreeNode[T]]) -> int:
        
        if node is None:
            return -1
        if node.is_leaf():
            return 0
        return 1 + max(self._height(child) for child in node.children)
    
    def pre_order(self) -> Iterator[T]:
       
        yield from self._pre_order(self._root)
    
    def _pre_order(self, node: TreeNode[T]) -> Iterator[T]:
        
        yield node.data
        for child in node.children:
            yield from self._pre_order(child)
    
    def post_order(self) -> Iterator[T]:
       
        yield from self._post_order(self._root)
    
    def _post_order(self, node: TreeNode[T]) -> Iterator[T]:
       
        for child in node.children:
            yield from self._post_order(child)
        yield node.data
    
    def level_order(self) -> Iterator[T]:
       
        if self._root is None:
            return
        queue = [self._root]
        while queue:
            node = queue.pop(0)
            yield node.data
            queue.extend(node.children)
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[TreeNode[T]]:
       
        return self._find(self._root, predicate)
    
    def _find(self, node: TreeNode[T], predicate: Callable[[T], bool]) -> Optional[TreeNode[T]]:
       
        if predicate(node.data):
            return node
        for child in node.children:
            result = self._find(child, predicate)
            if result:
                return result
        return None
    
    def size(self) -> int:
        
        return self._size(self._root)
    
    def _size(self, node: Optional[TreeNode[T]]) -> int:
       
        if node is None:
            return 0
        return 1 + sum(self._size(child) for child in node.children)
    
    def clear(self) -> None:
       
        self._root = None
