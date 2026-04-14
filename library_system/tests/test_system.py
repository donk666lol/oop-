# -*- coding: utf-8 -*-
"""
系统测试模块 - System Test Module

使用unittest框架测试核心功能。

测试覆盖：
- 实体类测试（Book, User, BorrowRecord）
- 数据结构测试（DoublyLinkedList, Stack, Queue, BST, HashTable）
- 系统集成测试
"""

import unittest
from datetime import date, timedelta
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entities.book import Book, BookStatus
from entities.user import User, UserType, UserStatus
from entities.borrow_record import BorrowRecord, RecordStatus
from datastructures.doubly_linked_list import DoublyLinkedList
from datastructures.stack import ArrayStack
from datastructures.queue import ArrayQueue
from datastructures.binary_search_tree import BinarySearchTree
from datastructures.hash_table import HashTable
from core.exceptions import (
    BookNotFoundException, UserNotFoundException,
    DuplicateItemException, DataStructureException
)


# ========== 实体类测试 ==========

class TestBook(unittest.TestCase):
    """图书类测试"""
    
    def setUp(self):
        """每个测试前的初始化"""
        self.book = Book(
            book_id="B001",
            isbn="9787115428028",
            title="Python编程",
            author="John Smith",
            publisher="人民邮电出版社",
            publish_year=2020,
            category="计算机"
        )
    
    def test_book_creation(self):
        """测试图书创建"""
        self.assertEqual(self.book.book_id, "B001")
        self.assertEqual(self.book.title, "Python编程")
        self.assertEqual(self.book.status, BookStatus.AVAILABLE)
        self.assertTrue(self.book.is_available)
    
    def test_book_borrow(self):
        """测试图书借阅"""
        result = self.book.borrow("U001", 30)
        self.assertTrue(result)
        self.assertEqual(self.book.status, BookStatus.BORROWED)
        self.assertEqual(self.book.current_borrower, "U001")
        self.assertFalse(self.book.is_available)
        self.assertEqual(self.book.borrow_count, 1)
    
    def test_book_return(self):
        """测试图书归还"""
        self.book.borrow("U001", 30)
        result = self.book.return_book()
        self.assertTrue(result)
        self.assertEqual(self.book.status, BookStatus.AVAILABLE)
        self.assertIsNone(self.book.current_borrower)
    
    def test_book_comparison(self):
        """测试图书比较"""
        book2 = Book("B002", "9787115428029", "Java编程", "Jane Doe")
        self.assertNotEqual(self.book, book2)
        
        book3 = Book("B001", "9787115428028", "Python编程", "John Smith")
        self.assertEqual(self.book, book3)
    
    def test_book_serialization(self):
        """测试图书序列化"""
        data = self.book.to_dict()
        self.assertEqual(data['book_id'], "B001")
        self.assertEqual(data['title'], "Python编程")
        
        restored_book = Book.from_dict(data)
        self.assertEqual(restored_book.book_id, self.book.book_id)
        self.assertEqual(restored_book.title, self.book.title)


class TestUser(unittest.TestCase):
    """用户类测试"""
    
    def setUp(self):
        self.user = User(
            user_id="U001",
            name="张三",
            email="zhangsan@example.com",
            user_type=UserType.STUDENT
        )
    
    def test_user_creation(self):
        """测试用户创建"""
        self.assertEqual(self.user.user_id, "U001")
        self.assertEqual(self.user.name, "张三")
        self.assertEqual(self.user.user_type, UserType.STUDENT)
        self.assertTrue(self.user.is_active)
    
    def test_user_can_borrow(self):
        """测试用户借阅权限"""
        self.assertTrue(self.user.can_borrow())
        self.assertEqual(self.user.borrow_limit, 5)
    
    def test_user_borrow_operations(self):
        """测试用户借阅操作"""
        self.user.add_borrowed_book("B001")
        self.assertEqual(self.user.borrowed_count, 1)
        
        self.user.remove_borrowed_book("B001")
        self.assertEqual(self.user.borrowed_count, 0)
    
    def test_user_status_change(self):
        """测试用户状态变更"""
        self.user.suspend()
        self.assertEqual(self.user.status, UserStatus.SUSPENDED)
        self.assertFalse(self.user.can_borrow())
        
        self.user.activate()
        self.assertEqual(self.user.status, UserStatus.ACTIVE)
        self.assertTrue(self.user.can_borrow())


class TestBorrowRecord(unittest.TestCase):
    """借阅记录类测试"""
    
    def setUp(self):
        self.record = BorrowRecord(
            record_id="R001",
            book_id="B001",
            user_id="U001",
            borrow_days=30
        )
    
    def test_record_creation(self):
        """测试记录创建"""
        self.assertEqual(self.record.record_id, "R001")
        self.assertEqual(self.record.book_id, "B001")
        self.assertEqual(self.record.status, RecordStatus.ACTIVE)
        self.assertTrue(self.record.is_active)
    
    def test_fine_calculation(self):
        """测试罚款计算"""
        # 模拟逾期
        self.record._due_date = date.today() - timedelta(days=5)
        fine = self.record.calculate_fine()
        self.assertEqual(fine, 5 * BorrowRecord.FINE_PER_DAY)
    
    def test_record_return(self):
        """测试记录归还"""
        fine = self.record.return_book()
        self.assertEqual(self.record.status, RecordStatus.RETURNED)
        self.assertIsNotNone(self.record.return_date)


# ========== 数据结构测试 ==========

class TestDoublyLinkedList(unittest.TestCase):
    """双向链表测试"""
    
    def setUp(self):
        self.dll = DoublyLinkedList()
    
    def test_add_first(self):
        """测试头部添加"""
        self.dll.add_first(1)
        self.assertEqual(len(self.dll), 1)
        self.assertEqual(self.dll.first(), 1)
    
    def test_add_last(self):
        """测试尾部添加"""
        self.dll.add_last(1)
        self.dll.add_last(2)
        self.assertEqual(self.dll.last(), 2)
    
    def test_delete_operations(self):
        """测试删除操作"""
        self.dll.add_last(1)
        self.dll.add_last(2)
        self.dll.add_last(3)
        
        self.assertEqual(self.dll.delete_first(), 1)
        self.assertEqual(self.dll.delete_last(), 3)
        self.assertEqual(len(self.dll), 1)
    
    def test_iteration(self):
        """测试迭代"""
        for i in range(5):
            self.dll.add_last(i)
        
        result = list(self.dll)
        self.assertEqual(result, [0, 1, 2, 3, 4])
    
    def test_empty_list_error(self):
        """测试空链表异常"""
        with self.assertRaises(DataStructureException):
            self.dll.delete_first()


class TestArrayStack(unittest.TestCase):
    """栈测试"""
    
    def setUp(self):
        self.stack = ArrayStack()
    
    def test_push_pop(self):
        """测试压栈和出栈"""
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.pop(), 1)
    
    def test_top(self):
        """测试获取栈顶"""
        self.stack.push(1)
        self.assertEqual(self.stack.top(), 1)
        self.assertEqual(len(self.stack), 1)
    
    def test_empty_stack_error(self):
        """测试空栈异常"""
        with self.assertRaises(DataStructureException):
            self.stack.pop()


class TestArrayQueue(unittest.TestCase):
    """队列测试"""
    
    def setUp(self):
        self.queue = ArrayQueue()
    
    def test_enqueue_dequeue(self):
        """测试入队和出队"""
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.assertEqual(self.queue.dequeue(), 1)
        self.assertEqual(self.queue.dequeue(), 2)
    
    def test_first_last(self):
        """测试获取队首队尾"""
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.assertEqual(self.queue.first(), 1)
        self.assertEqual(self.queue.last(), 2)
    
    def test_empty_queue_error(self):
        """测试空队异常"""
        with self.assertRaises(DataStructureException):
            self.queue.dequeue()


class TestBinarySearchTree(unittest.TestCase):
    """二叉搜索树测试"""
    
    def setUp(self):
        self.bst = BinarySearchTree()
    
    def test_insert_search(self):
        """测试插入和搜索"""
        self.bst.insert(50, "Fifty")
        self.bst.insert(30, "Thirty")
        self.bst.insert(70, "Seventy")
        
        self.assertEqual(self.bst.search(30), "Thirty")
        self.assertEqual(self.bst.search(50), "Fifty")
        self.assertIsNone(self.bst.search(100))
    
    def test_delete(self):
        """测试删除"""
        self.bst.insert(50, "Fifty")
        self.bst.insert(30, "Thirty")
        
        self.bst.delete(30)
        self.assertIsNone(self.bst.search(30))
    
    def test_inorder_traversal(self):
        """测试中序遍历"""
        self.bst.insert(50, 50)
        self.bst.insert(30, 30)
        self.bst.insert(70, 70)
        self.bst.insert(20, 20)
        self.bst.insert(40, 40)
        
        result = self.bst.to_sorted_list()
        self.assertEqual(result, [20, 30, 40, 50, 70])
    
    def test_range_search(self):
        """测试范围查询"""
        for i in [50, 30, 70, 20, 40, 60, 80]:
            self.bst.insert(i, i)
        
        result = self.bst.range_search(30, 60)
        self.assertEqual(result, [30, 40, 50, 60])


class TestHashTable(unittest.TestCase):
    """哈希表测试"""
    
    def setUp(self):
        self.ht = HashTable()
    
    def test_insert_get(self):
        """测试插入和获取"""
        self.ht.insert("B001", "Book1")
        self.ht.insert("B002", "Book2")
        
        self.assertEqual(self.ht.get("B001"), "Book1")
        self.assertEqual(self.ht.get("B002"), "Book2")
    
    def test_update(self):
        """测试更新"""
        self.ht.insert("B001", "Book1")
        self.ht.insert("B001", "Book1Updated")
        
        self.assertEqual(self.ht.get("B001"), "Book1Updated")
    
    def test_remove(self):
        """测试删除"""
        self.ht.insert("B001", "Book1")
        self.ht.remove("B001")
        
        self.assertIsNone(self.ht.get("B001"))
    
    def test_iteration(self):
        """测试迭代"""
        self.ht.insert("B001", "Book1")
        self.ht.insert("B002", "Book2")
        
        keys = list(self.ht.keys())
        self.assertIn("B001", keys)
        self.assertIn("B002", keys)


# ========== 集成测试 ==========

class TestIntegration(unittest.TestCase):
    """系统集成测试"""
    
    def test_book_borrow_flow(self):
        """测试完整的借书流程"""
        # 创建图书和用户
        book = Book("B001", "9787115428028", "Python编程", "John Smith")
        user = User("U001", "张三", "test@example.com", UserType.STUDENT)
        
        # 用户可以借书
        self.assertTrue(user.can_borrow())
        
        # 图书可借
        self.assertTrue(book.is_available)
        
        # 执行借阅
        book.borrow(user.user_id, user.max_borrow_days)
        user.add_borrowed_book(book.book_id)
        
        # 验证状态
        self.assertFalse(book.is_available)
        self.assertEqual(user.borrowed_count, 1)
        
        # 归还
        book.return_book()
        user.remove_borrowed_book(book.book_id)
        
        self.assertTrue(book.is_available)
        self.assertEqual(user.borrowed_count, 0)


# ========== 辅助函数测试 ==========

class TestStackApplications(unittest.TestCase):
    """栈应用测试"""
    
    def test_bracket_matching(self):
        """测试括号匹配"""
        from datastructures.stack import is_matched
        
        self.assertTrue(is_matched("(a + b) * (c - d)"))
        self.assertTrue(is_matched("[{()}]"))
        self.assertFalse(is_matched("((a + b)"))
        self.assertFalse(is_matched(")a + b("))
    
    def test_string_reversal(self):
        """测试字符串反转"""
        from datastructures.stack import reverse_string
        
        self.assertEqual(reverse_string("hello"), "olleh")
        self.assertEqual(reverse_string("Python"), "nohtyP")


# 运行测试
if __name__ == '__main__':
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestBook))
    suite.addTests(loader.loadTestsFromTestCase(TestUser))
    suite.addTests(loader.loadTestsFromTestCase(TestBorrowRecord))
    suite.addTests(loader.loadTestsFromTestCase(TestDoublyLinkedList))
    suite.addTests(loader.loadTestsFromTestCase(TestArrayStack))
    suite.addTests(loader.loadTestsFromTestCase(TestArrayQueue))
    suite.addTests(loader.loadTestsFromTestCase(TestBinarySearchTree))
    suite.addTests(loader.loadTestsFromTestCase(TestHashTable))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestStackApplications))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
