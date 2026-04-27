# -*- coding: utf-8 -*-
"""
栈模块 - Stack Module

栈是一种后进先出（LIFO: Last In First Out）的线性数据结构。
类似于叠盘子，最后放上去的盘子会最先被取走。

核心操作：
- push(e): 将元素e压入栈顶
- pop(): 弹出并返回栈顶元素
- top(): 返回栈顶元素（不删除）
- is_empty(): 检查栈是否为空
- len(): 返回栈中元素数量

时间复杂度分析：
- push: O(1) 均摊（使用动态数组时）
- pop: O(1) 均摊
- top: O(1)
- is_empty: O(1)

空间复杂度：O(n)

应用场景：
- 函数调用栈（递归）
- 括号匹配检查
- 表达式求值
- 浏览器前进/后退
- 文本编辑器撤销操作

本项目应用：
- 管理用户操作历史（撤销功能）
- 追踪系统操作日志
"""

from typing import Any, Optional, Generic, TypeVar
from core.exceptions import DataStructureException

T = TypeVar('T')


class ArrayStack(Generic[T]):
    """
    基于Python列表实现的栈
    
    列表末尾作为栈顶，这样push和pop操作都是O(1)
    
    示例：
        >>> stack = ArrayStack[int]()
        >>> stack.push(1)
        >>> stack.push(2)
        >>> stack.top()  # 返回 2
        >>> stack.pop()  # 返回 2
        >>> len(stack)   # 返回 1
    """
    
    def __init__(self, initial_capacity: int = 10):
        """
        初始化空栈
        
        参数：
            initial_capacity: 初始容量（默认10）
        """
        self._data: list[Optional[T]] = [None] * initial_capacity
        self._size = 0
        self._capacity = initial_capacity
    
    def __len__(self) -> int:
        """返回栈中元素数量"""
        return self._size
    
    def __repr__(self) -> str:
        """栈的字符串表示"""
        elements = [str(self._data[i]) for i in range(self._size)]
        return f"Stack([{', '.join(elements)}] <- 栈顶)"
    
    def __iter__(self):
        """使栈可迭代（从栈顶到栈底）"""
        for i in range(self._size - 1, -1, -1):
            yield self._data[i]
    
    def is_empty(self) -> bool:
        """
        检查栈是否为空
        
        返回：
            bool: 如果栈为空返回True
        """
        return self._size == 0
    
    def _resize(self, new_capacity: int) -> None:
        """
        调整栈的容量（内部方法）
        
        参数：
            new_capacity: 新的容量大小
            
        时间复杂度：O(n)，需要复制所有元素
        """
        old_data = self._data
        self._data = [None] * new_capacity
        for i in range(self._size):
            self._data[i] = old_data[i]
        self._capacity = new_capacity
    
    def push(self, element: T) -> None:
        """
        将元素压入栈顶
        
        参数：
            element: 要压入的元素
            
        时间复杂度：O(1) 均摊
            
        示例：
            >>> stack = ArrayStack()
            >>> stack.push(1)  # 栈：[1]
            >>> stack.push(2)  # 栈：[1, 2]
        """
        # 如果栈满了，扩容为原来的2倍
        if self._size == self._capacity:
            self._resize(2 * self._capacity)
        
        self._data[self._size] = element
        self._size += 1
    
    def pop(self) -> T:
        """
        弹出并返回栈顶元素
        
        返回：
            T: 栈顶元素
            
        异常：
            DataStructureException: 如果栈为空
            
        时间复杂度：O(1) 均摊
            
        示例：
            >>> stack.pop()  # 返回并删除栈顶元素
        """
        if self.is_empty():
            raise DataStructureException("栈", "不能从空栈弹出元素")
        
        self._size -= 1
        element = self._data[self._size]
        self._data[self._size] = None  # 帮助垃圾回收
        
        # 如果元素数量少于容量的1/4，缩容为一半
        if self._size > 0 and self._size < self._capacity // 4:
            self._resize(self._capacity // 2)
        
        return element
    
    def top(self) -> T:
        """
        返回栈顶元素（不删除）
        
        返回：
            T: 栈顶元素
            
        异常：
            DataStructureException: 如果栈为空
            
        时间复杂度：O(1)
        """
        if self.is_empty():
            raise DataStructureException("栈", "栈为空，没有栈顶元素")
        return self._data[self._size - 1]
    
    def clear(self) -> None:
        """清空栈"""
        self._data = [None] * self._capacity
        self._size = 0
    
    def to_list(self) -> list:
        """
        将栈转换为列表（栈顶元素在列表末尾）
        
        返回：
            list: 包含栈中所有元素的列表
        """
        return [self._data[i] for i in range(self._size)]


# ========== 栈的应用示例 ==========

def is_matched(expression: str) -> bool:
    """
    使用栈检查括号是否正确匹配
    
    参数：
        expression: 要检查的表达式字符串
        
    返回：
        bool: 如果括号匹配返回True
        
    示例：
        >>> is_matched("(a + b) * (c - d)")  # True
        >>> is_matched("((a + b)")          # False
        >>> is_matched("[{()}]")            # True
        
    时间复杂度：O(n)
    空间复杂度：O(n)
    """
    left_brackets = '([{'
    right_brackets = ')]}'
    stack = ArrayStack[str]()
    
    for char in expression:
        if char in left_brackets:
            stack.push(char)
        elif char in right_brackets:
            if stack.is_empty():
                return False
            # 检查是否匹配
            left = stack.pop()
            if left_brackets.index(left) != right_brackets.index(char):
                return False
    
    return stack.is_empty()


def reverse_string(s: str) -> str:
    """
    使用栈反转字符串
    
    参数：
        s: 要反转的字符串
        
    返回：
        str: 反转后的字符串
        
    时间复杂度：O(n)
    空间复杂度：O(n)
    """
    stack = ArrayStack[str]()
    for char in s:
        stack.push(char)
    
    result = []
    while not stack.is_empty():
        result.append(stack.pop())
    
    return ''.join(result)


def evaluate_postfix(expression: str) -> float:
    """
    计算后缀表达式（逆波兰表达式）
    
    参数：
        expression: 后缀表达式，用空格分隔
                    例如："3 4 + 2 *"
        
    返回：
        float: 计算结果
        
    示例：
        >>> evaluate_postfix("3 4 + 2 *")  # 返回 14
        >>> evaluate_postfix("5 1 2 + 4 * + 3 -")  # 返回 14
        
    时间复杂度：O(n)
    空间复杂度：O(n)
    """
    stack = ArrayStack[float]()
    operators = {'+', '-', '*', '/', '^'}
    
    tokens = expression.split()
    
    for token in tokens:
        if token not in operators:
            stack.push(float(token))
        else:
            if len(stack) < 2:
                raise ValueError("无效的后缀表达式")
            right = stack.pop()
            left = stack.pop()
            
            if token == '+':
                stack.push(left + right)
            elif token == '-':
                stack.push(left - right)
            elif token == '*':
                stack.push(left * right)
            elif token == '/':
                if right == 0:
                    raise ZeroDivisionError("除数不能为0")
                stack.push(left / right)
            elif token == '^':
                stack.push(left ** right)
    
    if len(stack) != 1:
        raise ValueError("无效的后缀表达式")
    
    return stack.pop()
