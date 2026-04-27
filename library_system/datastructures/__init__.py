# -*- coding: utf-8 -*-
"""
数据结构模块 - Data Structures Module

本模块包含所有必需的数据结构实现：
- DoublyLinkedList: 双向链表
- Stack: 栈
- Queue: 队列
- Tree: 通用树
- BinarySearchTree: 二叉搜索树
- HashTable: 哈希表

这些数据结构是OOP课程的核心要求，展示了对抽象数据类型(ADT)的理解和实现能力。
"""

from .doubly_linked_list import DoublyLinkedList
from .stack import ArrayStack, is_matched, reverse_string, evaluate_postfix
from .queue import ArrayQueue, CircularQueue
from .tree import Tree, TreeNode, CategoryTree
from .binary_search_tree import BinarySearchTree, TreeNode as BSTNode
from .hash_table import HashTable

__all__ = [
    'DoublyLinkedList',
    'ArrayStack',
    'is_matched',
    'reverse_string', 
    'evaluate_postfix',
    'ArrayQueue',
    'CircularQueue',
    'Tree',
    'TreeNode',
    'CategoryTree',
    'BinarySearchTree',
    'BSTNode',
    'HashTable'
]
