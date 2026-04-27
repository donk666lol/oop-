from typing import Any, Optional, Iterator, List, Callable, Generic, TypeVar

T = TypeVar('T')


class BinaryTreeTraversal(Generic[T]):
    
    
    @staticmethod
    def in_order(node) -> Iterator[T]:
       
        if node is not None:
            yield from BinaryTreeTraversal.in_order(node.left)
            yield node.value
            yield from BinaryTreeTraversal.in_order(node.right)
    
    @staticmethod
    def in_order_iterative(node) -> Iterator[T]:
       
        stack = []
        current = node
        while current or stack:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            yield current.value
            current = current.right
    
    @staticmethod
    def pre_order(node) -> Iterator[T]:
       
        if node is not None:
            yield node.value
            yield from BinaryTreeTraversal.pre_order(node.left)
            yield from BinaryTreeTraversal.pre_order(node.right)
    
    @staticmethod
    def pre_order_iterative(node) -> Iterator[T]:
       
        if not node:
            return
        stack = [node]
        while stack:
            current = stack.pop()
            yield current.value
            if current.right:
                stack.append(current.right)
            if current.left:
                stack.append(current.left)
    
    @staticmethod
    def post_order(node) -> Iterator[T]:
        
        if node is not None:
            yield from BinaryTreeTraversal.post_order(node.left)
            yield from BinaryTreeTraversal.post_order(node.right)
            yield node.value
    
    @staticmethod
    def post_order_iterative(node) -> Iterator[T]:
        
        if not node:
            return
        stack = [(node, False)]
        while stack:
            current, visited = stack.pop()
            if visited:
                yield current.value
            else:
                stack.append((current, True))
                if current.right:
                    stack.append((current.right, False))
                if current.left:
                    stack.append((current.left, False))
    
    @staticmethod
    def level_order(node) -> Iterator[T]:
        
        if not node:
            return
        queue = [node]
        while queue:
            current = queue.pop(0)
            yield current.value
            if current.left:
                queue.append(current.left)
            if current.right:
                queue.append(current.right)


class GeneralTreeTraversal(Generic[T]):
   
    
    @staticmethod
    def pre_order(node) -> Iterator[T]:
       
        if node is not None:
            yield node.data
            for child in node.children:
                yield from GeneralTreeTraversal.pre_order(child)
    
    @staticmethod
    def pre_order_iterative(node) -> Iterator[T]:
        
        if not node:
            return
        stack = [node]
        while stack:
            current = stack.pop()
            yield current.data
            # 逆序入栈，保证顺序正确
            for child in reversed(current.children):
                stack.append(child)
    
    @staticmethod
    def post_order(node) -> Iterator[T]:
        
        if node is not None:
            for child in node.children:
                yield from GeneralTreeTraversal.post_order(child)
            yield node.data
    
    @staticmethod
    def post_order_iterative(node) -> Iterator[T]:
        
        if not node:
            return
        stack = [(node, False)]
        while stack:
            current, visited = stack.pop()
            if visited:
                yield current.data
            else:
                stack.append((current, True))
                # 逆序入栈，保证顺序正确
                for child in reversed(current.children):
                    stack.append((child, False))
    
    @staticmethod
    def level_order(node) -> Iterator[T]:
       
        if not node:
            return
        queue = [node]
        while queue:
            current = queue.pop(0)
            yield current.data
            queue.extend(current.children)


class TraversalUtils:
    
    
    @staticmethod
    def traverse_and_process(node, traversal_func, process_func) -> List[Any]:
        
        results = []
        for item in traversal_func(node):
            results.append(process_func(item))
        return results
    
    @staticmethod
    def find_in_traversal(node, traversal_func, predicate) -> Optional[Any]:
        
        for item in traversal_func(node):
            if predicate(item):
                return item
        return None
    
    @staticmethod
    def count_nodes(node, traversal_func) -> int:
        
        count = 0
        for _ in traversal_func(node):
            count += 1
        return count
    
    @staticmethod
    def max_depth(node) -> int:
        
        if not node:
            return -1
        if not hasattr(node, 'children'):
            # 二叉树
            left_depth = TraversalUtils.max_depth(node.left) if node.left else -1
            right_depth = TraversalUtils.max_depth(node.right) if node.right else -1
            return 1 + max(left_depth, right_depth)
        else:
            # 通用树
            if not node.children:
                return 0
            return 1 + max(TraversalUtils.max_depth(child) for child in node.children)
