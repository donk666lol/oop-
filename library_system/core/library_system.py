# -*- coding: utf-8 -*-
"""
图书馆系统核心模块 - Library System Core Module

本模块是整个系统的核心，整合所有数据结构和业务逻辑。

设计模式应用：
1. 单例模式：Logger和DataManager
2. 门面模式：LibrarySystem作为统一接口
3. 组合模式：树形分类结构

OOP概念展示：
- 抽象类/基类的使用
- 组合关系（Library包含多个Book）
- 多态（不同类型的用户行为不同）
- 封装（数据访问通过统一接口）
"""

from typing import Optional, List, Dict, Callable
from datetime import date, datetime, timedelta
from dataclasses import dataclass
import json

# 导入实体类
from entities.book import Book, BookStatus
from entities.user import User, UserType, UserStatus
from entities.borrow_record import BorrowRecord, RecordStatus

# 导入数据结构
from datastructures.doubly_linked_list import DoublyLinkedList
from datastructures.stack import ArrayStack
from datastructures.queue import ArrayQueue
from datastructures.tree import CategoryTree
from datastructures.binary_search_tree import BinarySearchTree
from datastructures.hash_table import HashTable

# 导入异常
from core.exceptions import (
    BookNotFoundException, BookNotAvailableException,
    UserNotFoundException, DuplicateItemException,
    InvalidInputException, OperationLimitException
)

# 导入其他模块
from core.data_manager import DataManager
from utils.logger import Logger


class LibrarySystem:
    """
    图书馆管理系统主类
    
    整合所有功能模块，提供统一的操作接口。
    
    数据存储结构：
    - books: HashTable（以book_id为键，存储Book对象）
    - users: HashTable（以user_id为键，存储User对象）
    - borrow_records: DoublyLinkedList（存储借阅记录）
    - categories: CategoryTree（图书分类层次结构）
    - active_borrows: Queue（当前活跃借阅，先进先出处理）
    - operation_stack: Stack（操作历史，支持撤销）
    - book_index: BinarySearchTree（以书名为键建立索引，支持范围查询）
    
    示例：
        >>> library = LibrarySystem(DataManager())
        >>> library.add_book(book)
        >>> library.borrow_book("U001", "B001")
    """
    
    def __init__(self, data_manager: DataManager):
        """
        初始化图书馆系统
        
        参数：
            data_manager: 数据持久化管理器
        """
        self._logger = Logger.get_instance()
        self._data_manager = data_manager
        
        # 核心数据结构
        self._books: HashTable[str, Book] = HashTable()
        self._users: HashTable[str, User] = HashTable()
        self._borrow_records: DoublyLinkedList = DoublyLinkedList()
        self._categories: CategoryTree = CategoryTree()
        
        # 辅助数据结构
        self._active_borrows: ArrayQueue = ArrayQueue()  # 活跃借阅队列
        self._operation_stack: ArrayStack = ArrayStack()  # 操作历史栈
        self._book_title_index: BinarySearchTree = BinarySearchTree()  # 书名索引树
        self._reservation_queue: Dict[str, ArrayQueue] = {}  # 图书预约队列
        
        # 统计信息
        self._total_borrows = 0
        self._total_returns = 0
        
        # 初始化数据
        self._initialize_system()
    
    def _initialize_system(self) -> None:
        """
        初始化系统数据
        
        首次运行：生成示例数据
        后续运行：从文件加载已有数据
        """
        self._logger.info("Initializing library system...")
        
        # 初始化分类树
        self._init_categories()
        
        # 尝试加载数据
        if self._data_manager.has_saved_data():
            self._load_data()
            self._logger.info("Loaded existing data from files.")
        else:
            self._generate_sample_data()
            self._logger.info("Generated sample data for new system.")
            self._save_data()
    
    def _init_categories(self) -> None:
        """初始化图书分类层次结构"""
        # 一级分类
        self._categories.add_category("文学", "所有分类")
        self._categories.add_category("科技", "所有分类")
        self._categories.add_category("教育", "所有分类")
        self._categories.add_category("艺术", "所有分类")
        self._categories.add_category("历史", "所有分类")
        
        # 二级分类
        self._categories.add_category("小说", "文学")
        self._categories.add_category("诗歌", "文学")
        self._categories.add_category("散文", "文学")
        
        self._categories.add_category("计算机", "科技")
        self._categories.add_category("物理", "科技")
        self._categories.add_category("数学", "科技")
        
        self._categories.add_category("教材", "教育")
        self._categories.add_category("考试", "教育")
        
        # 三级分类
        self._categories.add_category("科幻小说", "小说")
        self._categories.add_category("言情小说", "小说")
        self._categories.add_category("武侠小说", "小说")
        
        self._categories.add_category("编程", "计算机")
        self._categories.add_category("人工智能", "计算机")
        self._categories.add_category("数据科学", "计算机")
    
    def _generate_sample_data(self) -> None:
        """生成示例数据"""
        # 示例图书
        sample_books = [
            Book("B001", "9787115428028", "Python编程从入门到实践", "Eric Matthes", 
                 "人民邮电出版社", 2020, "计算机"),
            Book("B002", "9787111641130", "深入理解计算机系统", "Randal E.Bryant", 
                 "机械工业出版社", 2019, "计算机"),
            Book("B003", "9787020008795", "红楼梦", "曹雪芹", 
                 "人民文学出版社", 2015, "小说"),
            Book("B004", "9787544291170", "百年孤独", "加西亚·马尔克斯", 
                 "南海出版公司", 2017, "小说"),
            Book("B005", "9787111544937", "机器学习", "周志华", 
                 "清华大学出版社", 2018, "人工智能"),
            Book("B006", "9787302517597", "数据结构（C语言版）", "严蔚敏", 
                 "清华大学出版社", 2019, "计算机"),
            Book("B007", "9787536692930", "三体", "刘慈欣", 
                 "重庆出版社", 2016, "科幻小说"),
            Book("B008", "9787544277105", "解忧杂货店", "东野圭吾", 
                 "南海出版公司", 2018, "小说"),
            Book("B009", "9787111633524", "算法导论", "Thomas H.Cormen", 
                 "机械工业出版社", 2018, "计算机"),
            Book("B010", "9787020138387", "围城", "钱钟书", 
                 "人民文学出版社", 2017, "小说"),
        ]
        
        for book in sample_books:
            self._books[book.book_id] = book
            # 建立书名索引（使用书名首字母作为键，实际应用中可以更复杂）
            self._book_title_index.insert(book.title, book.book_id)
        
        # 示例用户
        sample_users = [
            User("U001", "张三", "zhangsan@example.com", UserType.STUDENT, "计算机学院"),
            User("U002", "李四", "lisi@example.com", UserType.TEACHER, "数学系"),
            User("U003", "王五", "wangwu@example.com", UserType.STUDENT, "文学院"),
            User("U004", "赵六", "zhaoliu@example.com", UserType.ADMIN, "图书馆"),
            User("U005", "钱七", "qianqi@example.com", UserType.STAFF, "后勤部"),
        ]
        
        for user in sample_users:
            self._users[user.user_id] = user
        
        self._logger.info(f"Generated {len(sample_books)} books and {len(sample_users)} users.")
    
    def run(self) -> None:
        """
        启动系统主循环
        
        提供命令行交互界面
        """
        self._logger.info("Starting library system main loop...")
        print("\n" + "=" * 60)
        print("    欢迎使用图书馆管理系统 - Library Management System")
        print("    版本: 1.0.0 | 编程语言: Python")
        print("=" * 60)
        
        while True:
            self._show_main_menu()
            choice = input("\n请输入选项: ").strip()
            
            try:
                self._handle_main_choice(choice)
            except Exception as e:
                self._logger.error(f"Error handling choice: {e}")
                print(f"\n[错误] {e}")
            
            input("\n按回车键继续...")
            self._save_data()  # 每次操作后自动保存
    
    def _show_main_menu(self) -> None:
        """显示主菜单"""
        print("\n" + "-" * 40)
        print("  1. 图书管理 - Book Management")
        print("  2. 用户管理 - User Management")
        print("  3. 借阅管理 - Borrow Management")
        print("  4. 信息查询 - Information Query")
        print("  5. 系统设置 - System Settings")
        print("  0. 退出系统 - Exit")
        print("-" * 40)
    
    def _handle_main_choice(self, choice: str) -> None:
        """处理主菜单选择"""
        handlers = {
            '1': self._book_management_menu,
            '2': self._user_management_menu,
            '3': self._borrow_management_menu,
            '4': self._query_menu,
            '5': self._system_settings_menu,
            '0': self._exit_system
        }
        
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print("\n[提示] 无效选项，请重新输入。")
    
    # ========== 图书管理 ==========
    
    def _book_management_menu(self) -> None:
        """图书管理子菜单"""
        while True:
            print("\n" + "=" * 40)
            print("    图书管理 - Book Management")
            print("=" * 40)
            print("  1. 添加图书 - Add Book")
            print("  2. 查看图书列表 - View All Books")
            print("  3. 查询图书 - Search Book")
            print("  4. 更新图书信息 - Update Book")
            print("  5. 删除图书 - Delete Book")
            print("  6. 查看分类 - View Categories")
            print("  0. 返回主菜单 - Back")
            print("-" * 40)
            
            choice = input("请输入选项: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self._add_book_interactive()
            elif choice == '2':
                self._list_all_books()
            elif choice == '3':
                self._search_book_interactive()
            elif choice == '4':
                self._update_book_interactive()
            elif choice == '5':
                self._delete_book_interactive()
            elif choice == '6':
                self._show_categories()
            else:
                print("[提示] 无效选项")
    
    def add_book(self, book: Book) -> None:
        """
        添加图书
        
        参数：
            book: 要添加的图书对象
            
        异常：
            DuplicateItemException: 如果图书ID已存在
        """
        if self._books.contains(book.book_id):
            raise DuplicateItemException("图书", book.book_id)
        
        self._books.insert(book.book_id, book)
        self._book_title_index.insert(book.title, book.book_id)
        self._logger.info(f"Added book: {book.book_id} - {book.title}")
        self._record_operation("ADD_BOOK", book.book_id)
    
    def _add_book_interactive(self) -> None:
        """交互式添加图书"""
        print("\n--- 添加新图书 ---")
        
        book_id = input("图书ID (如 B011): ").strip()
        if not book_id:
            print("[错误] 图书ID不能为空")
            return
        
        if self._books.contains(book_id):
            print(f"[错误] 图书ID {book_id} 已存在")
            return
        
        isbn = input("ISBN: ").strip()
        title = input("书名: ").strip()
        author = input("作者: ").strip()
        publisher = input("出版社 (可留空): ").strip() or "未知出版社"
        
        try:
            year = int(input("出版年份 (默认2020): ").strip() or "2020")
        except ValueError:
            year = 2020
        
        category = input("分类 (可留空): ").strip() or "未分类"
        location = input("馆藏位置 (可留空): ").strip() or "A-01-001"
        
        book = Book(book_id, isbn, title, author, publisher, year, category, location)
        
        try:
            self.add_book(book)
            print(f"\n[成功] 图书 '{title}' 添加成功！")
        except Exception as e:
            print(f"\n[错误] 添加失败: {e}")
    
    def _list_all_books(self) -> None:
        """列出所有图书"""
        print("\n--- 图书列表 ---")
        
        books = list(self._books.values())
        if not books:
            print("暂无图书")
            return
        
        # 使用BST排序输出
        sorted_books = sorted(books, key=lambda b: b.title)
        
        for i, book in enumerate(sorted_books, 1):
            print(f"{i:3}. {book}")
        
        print(f"\n共 {len(books)} 本图书")
    
    def get_book(self, book_id: str) -> Book:
        """
        获取指定图书
        
        参数：
            book_id: 图书ID
            
        返回：
            Book: 图书对象
            
        异常：
            BookNotFoundException: 如果图书不存在
        """
        book = self._books.get(book_id)
        if book is None:
            raise BookNotFoundException(book_id)
        return book
    
    def _search_book_interactive(self) -> None:
        """交互式搜索图书"""
        print("\n--- 搜索图书 ---")
        print("1. 按ID搜索")
        print("2. 按书名搜索")
        print("3. 按作者搜索")
        print("4. 按分类搜索")
        
        choice = input("请选择搜索方式: ").strip()
        
        if choice == '1':
            book_id = input("请输入图书ID: ").strip()
            try:
                book = self.get_book(book_id)
                print(f"\n找到图书: {book}")
                self._show_book_details(book)
            except BookNotFoundException as e:
                print(f"\n[未找到] {e}")
        
        elif choice == '2':
            title = input("请输入书名关键词: ").strip().lower()
            results = [b for b in self._books.values() if title in b.title.lower()]
            self._display_search_results(results, "书名")
        
        elif choice == '3':
            author = input("请输入作者名: ").strip().lower()
            results = [b for b in self._books.values() if author in b.author.lower()]
            self._display_search_results(results, "作者")
        
        elif choice == '4':
            category = input("请输入分类: ").strip()
            results = [b for b in self._books.values() if b.category == category]
            self._display_search_results(results, "分类")
        
        else:
            print("[提示] 无效选项")
    
    def _display_search_results(self, results: List[Book], search_type: str) -> None:
        """显示搜索结果"""
        print(f"\n--- 按{search_type}搜索结果 ---")
        
        if not results:
            print("未找到匹配的图书")
            return
        
        for i, book in enumerate(results, 1):
            print(f"{i:3}. {book}")
        
        print(f"\n共找到 {len(results)} 本图书")
    
    def _show_book_details(self, book: Book) -> None:
        """显示图书详细信息"""
        print(f"\n{'=' * 50}")
        print(f"  图书ID: {book.book_id}")
        print(f"  ISBN: {book.isbn}")
        print(f"  书名: {book.title}")
        print(f"  作者: {book.author}")
        print(f"  出版社: {book.publisher}")
        print(f"  出版年份: {book.publish_year}")
        print(f"  分类: {book.category}")
        print(f"  馆藏位置: {book.location}")
        print(f"  状态: {book.status}")
        print(f"  借阅次数: {book.borrow_count}")
        print(f"  入馆日期: {book.added_date}")
        
        if book.is_borrowed:
            print(f"  当前借阅者: {book.current_borrower}")
            print(f"  应还日期: {book.due_date}")
        
        print(f"{'=' * 50}")
    
    def update_book(self, book_id: str, **kwargs) -> None:
        """
        更新图书信息
        
        参数：
            book_id: 图书ID
            **kwargs: 要更新的属性
            
        示例：
            >>> library.update_book("B001", title="新书名", category="新分类")
        """
        book = self.get_book(book_id)
        
        # 记录旧值用于撤销
        old_values = {}
        
        for key, value in kwargs.items():
            if hasattr(book, key):
                old_values[key] = getattr(book, key)
                setattr(book, key, value)
        
        self._logger.info(f"Updated book {book_id}: {kwargs}")
        self._record_operation("UPDATE_BOOK", book_id, old_values)
    
    def _update_book_interactive(self) -> None:
        """交互式更新图书"""
        print("\n--- 更新图书信息 ---")
        book_id = input("请输入要更新的图书ID: ").strip()
        
        try:
            book = self.get_book(book_id)
            self._show_book_details(book)
            
            print("\n请输入新值（直接回车保持原值）:")
            
            new_title = input(f"书名 [{book.title}]: ").strip()
            new_author = input(f"作者 [{book.author}]: ").strip()
            new_publisher = input(f"出版社 [{book.publisher}]: ").strip()
            new_category = input(f"分类 [{book.category}]: ").strip()
            new_location = input(f"位置 [{book.location}]: ").strip()
            
            updates = {}
            if new_title:
                updates['title'] = new_title
            if new_author:
                updates['author'] = new_author
            if new_publisher:
                updates['publisher'] = new_publisher
            if new_category:
                updates['category'] = new_category
            if new_location:
                updates['location'] = new_location
            
            if updates:
                self.update_book(book_id, **updates)
                print(f"\n[成功] 图书信息已更新")
            else:
                print("\n[提示] 未做任何修改")
            
        except BookNotFoundException as e:
            print(f"\n[错误] {e}")
    
    def delete_book(self, book_id: str) -> Book:
        """
        删除图书
        
        参数：
            book_id: 图书ID
            
        返回：
            Book: 被删除的图书对象
            
        异常：
            BookNotFoundException: 如果图书不存在
            OperationLimitException: 如果图书已借出
        """
        book = self.get_book(book_id)
        
        if book.is_borrowed:
            raise OperationLimitException("删除图书", 0, 0)
        
        deleted_book = self._books.remove(book_id)
        self._logger.info(f"Deleted book: {book_id}")
        self._record_operation("DELETE_BOOK", book_id, book.to_dict())
        
        return deleted_book
    
    def _delete_book_interactive(self) -> None:
        """交互式删除图书"""
        print("\n--- 删除图书 ---")
        book_id = input("请输入要删除的图书ID: ").strip()
        
        try:
            book = self.get_book(book_id)
            self._show_book_details(book)
            
            confirm = input("\n确认删除? (y/n): ").strip().lower()
            
            if confirm == 'y':
                self.delete_book(book_id)
                print(f"\n[成功] 图书 '{book.title}' 已删除")
            else:
                print("\n[取消] 操作已取消")
                
        except BookNotFoundException as e:
            print(f"\n[错误] {e}")
        except OperationLimitException:
            print(f"\n[错误] 该图书已借出，无法删除")
    
    def _show_categories(self) -> None:
        """显示图书分类树"""
        print("\n--- 图书分类结构 ---")
        print(self._categories.print_tree())
    
    # ========== 用户管理 ==========
    
    def _user_management_menu(self) -> None:
        """用户管理子菜单"""
        while True:
            print("\n" + "=" * 40)
            print("    用户管理 - User Management")
            print("=" * 40)
            print("  1. 添加用户 - Add User")
            print("  2. 查看用户列表 - View All Users")
            print("  3. 查询用户 - Search User")
            print("  4. 更新用户信息 - Update User")
            print("  5. 删除用户 - Delete User")
            print("  0. 返回主菜单 - Back")
            print("-" * 40)
            
            choice = input("请输入选项: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self._add_user_interactive()
            elif choice == '2':
                self._list_all_users()
            elif choice == '3':
                self._search_user_interactive()
            elif choice == '4':
                self._update_user_interactive()
            elif choice == '5':
                self._delete_user_interactive()
            else:
                print("[提示] 无效选项")
    
    def add_user(self, user: User) -> None:
        """添加用户"""
        if self._users.contains(user.user_id):
            raise DuplicateItemException("用户", user.user_id)
        
        self._users.insert(user.user_id, user)
        self._logger.info(f"Added user: {user.user_id} - {user.name}")
        self._record_operation("ADD_USER", user.user_id)
    
    def _add_user_interactive(self) -> None:
        """交互式添加用户"""
        print("\n--- 添加新用户 ---")
        
        user_id = input("用户ID (如 U006): ").strip()
        if not user_id:
            print("[错误] 用户ID不能为空")
            return
        
        if self._users.contains(user_id):
            print(f"[错误] 用户ID {user_id} 已存在")
            return
        
        name = input("姓名: ").strip()
        email = input("邮箱: ").strip()
        
        print("用户类型: 1-学生 2-教师 3-职工 4-管理员")
        type_choice = input("请选择 (默认1): ").strip() or "1"
        
        type_map = {'1': UserType.STUDENT, '2': UserType.TEACHER, 
                    '3': UserType.STAFF, '4': UserType.ADMIN}
        user_type = type_map.get(type_choice, UserType.STUDENT)
        
        department = input("部门/学院 (可留空): ").strip()
        
        user = User(user_id, name, email, user_type, department=department)
        
        try:
            self.add_user(user)
            print(f"\n[成功] 用户 '{name}' 添加成功！")
        except Exception as e:
            print(f"\n[错误] 添加失败: {e}")
    
    def _list_all_users(self) -> None:
        """列出所有用户"""
        print("\n--- 用户列表 ---")
        
        users = sorted(self._users.values(), key=lambda u: u.name)
        
        if not users:
            print("暂无用户")
            return
        
        for i, user in enumerate(users, 1):
            print(f"{i:3}. {user}")
        
        print(f"\n共 {len(users)} 位用户")
    
    def get_user(self, user_id: str) -> User:
        """获取指定用户"""
        user = self._users.get(user_id)
        if user is None:
            raise UserNotFoundException(user_id)
        return user
    
    def _search_user_interactive(self) -> None:
        """交互式搜索用户"""
        print("\n--- 搜索用户 ---")
        user_id = input("请输入用户ID: ").strip()
        
        try:
            user = self.get_user(user_id)
            self._show_user_details(user)
        except UserNotFoundException as e:
            print(f"\n[未找到] {e}")
    
    def _show_user_details(self, user: User) -> None:
        """显示用户详细信息"""
        print(f"\n{'=' * 50}")
        print(f"  用户ID: {user.user_id}")
        print(f"  姓名: {user.name}")
        print(f"  邮箱: {user.email}")
        print(f"  类型: {user.user_type}")
        print(f"  状态: {user.status}")
        print(f"  部门: {user.department}")
        print(f"  注册日期: {user.register_date}")
        print(f"  借阅上限: {user.borrow_limit}")
        print(f"  当前借阅: {user.borrowed_count}")
        print(f"  可借阅: {'是' if user.can_borrow() else '否'}")
        print(f"{'=' * 50}")
    
    def update_user(self, user_id: str, **kwargs) -> None:
        """更新用户信息"""
        user = self.get_user(user_id)
        
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        
        self._logger.info(f"Updated user {user_id}: {kwargs}")
    
    def _update_user_interactive(self) -> None:
        """交互式更新用户"""
        print("\n--- 更新用户信息 ---")
        user_id = input("请输入要更新的用户ID: ").strip()
        
        try:
            user = self.get_user(user_id)
            self._show_user_details(user)
            
            print("\n请输入新值（直接回车保持原值）:")
            
            new_name = input(f"姓名 [{user.name}]: ").strip()
            new_email = input(f"邮箱 [{user.email}]: ").strip()
            new_department = input(f"部门 [{user.department}]: ").strip()
            
            updates = {}
            if new_name:
                updates['name'] = new_name
            if new_email:
                updates['email'] = new_email
            if new_department:
                updates['department'] = new_department
            
            if updates:
                self.update_user(user_id, **updates)
                print(f"\n[成功] 用户信息已更新")
            
        except UserNotFoundException as e:
            print(f"\n[错误] {e}")
    
    def delete_user(self, user_id: str) -> User:
        """删除用户"""
        user = self.get_user(user_id)
        
        if user.borrowed_count > 0:
            raise OperationLimitException("删除用户", user.borrowed_count, 0)
        
        deleted_user = self._users.remove(user_id)
        self._logger.info(f"Deleted user: {user_id}")
        return deleted_user
    
    def _delete_user_interactive(self) -> None:
        """交互式删除用户"""
        print("\n--- 删除用户 ---")
        user_id = input("请输入要删除的用户ID: ").strip()
        
        try:
            user = self.get_user(user_id)
            self._show_user_details(user)
            
            confirm = input("\n确认删除? (y/n): ").strip().lower()
            
            if confirm == 'y':
                self.delete_user(user_id)
                print(f"\n[成功] 用户 '{user.name}' 已删除")
            else:
                print("\n[取消] 操作已取消")
                
        except UserNotFoundException as e:
            print(f"\n[错误] {e}")
        except OperationLimitException as e:
            print(f"\n[错误] 该用户有未归还图书，无法删除")
    
    # ========== 借阅管理 ==========
    
    def _borrow_management_menu(self) -> None:
        """借阅管理子菜单"""
        while True:
            print("\n" + "=" * 40)
            print("    借阅管理 - Borrow Management")
            print("=" * 40)
            print("  1. 借书 - Borrow Book")
            print("  2. 还书 - Return Book")
            print("  3. 续借 - Renew Book")
            print("  4. 预约 - Reserve Book")
            print("  5. 查看借阅记录 - View Records")
            print("  6. 查看逾期图书 - View Overdue")
            print("  0. 返回主菜单 - Back")
            print("-" * 40)
            
            choice = input("请输入选项: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self._borrow_book_interactive()
            elif choice == '2':
                self._return_book_interactive()
            elif choice == '3':
                self._renew_book_interactive()
            elif choice == '4':
                self._reserve_book_interactive()
            elif choice == '5':
                self._show_borrow_records()
            elif choice == '6':
                self._show_overdue_books()
            else:
                print("[提示] 无效选项")
    
    def borrow_book(self, user_id: str, book_id: str) -> BorrowRecord:
        """
        借书
        
        参数：
            user_id: 用户ID
            book_id: 图书ID
            
        返回：
            BorrowRecord: 新创建的借阅记录
            
        异常：
            UserNotFoundException: 用户不存在
            BookNotFoundException: 图书不存在
            BookNotAvailableException: 图书不可借
            OperationLimitException: 用户借阅已达上限
        """
        user = self.get_user(user_id)
        book = self.get_book(book_id)
        
        # 检查用户是否可以借书
        if not user.can_borrow():
            raise OperationLimitException("借书数量", user.borrowed_count, user.borrow_limit)
        
        # 检查图书是否可借
        if not book.is_available:
            raise BookNotAvailableException(book_id, "当前不可借阅")
        
        # 创建借阅记录
        record_id = BorrowRecord.generate_id()
        record = BorrowRecord(record_id, book_id, user_id, 
                             borrow_days=user.max_borrow_days)
        
        # 更新状态
        book.borrow(user_id, user.max_borrow_days)
        user.add_borrowed_book(book_id)
        
        # 添加到数据结构
        self._borrow_records.add_last(record)
        self._active_borrows.enqueue(record)
        
        self._total_borrows += 1
        self._logger.info(f"Borrowed: User {user_id} borrowed Book {book_id}")
        self._record_operation("BORROW", record_id)
        
        return record
    
    def _borrow_book_interactive(self) -> None:
        """交互式借书"""
        print("\n--- 借书 ---")
        user_id = input("请输入用户ID: ").strip()
        book_id = input("请输入图书ID: ").strip()
        
        try:
            record = self.borrow_book(user_id, book_id)
            book = self.get_book(book_id)
            user = self.get_user(user_id)
            
            print(f"\n[成功] 借书成功！")
            print(f"  图书: {book.title}")
            print(f"  借阅者: {user.name}")
            print(f"  应还日期: {record.due_date}")
            print(f"  借阅记录号: {record.record_id}")
            
        except Exception as e:
            print(f"\n[错误] {e}")
    
    def return_book(self, user_id: str, book_id: str) -> tuple[BorrowRecord, float]:
        """
        还书
        
        参数：
            user_id: 用户ID
            book_id: 图书ID
            
        返回：
            tuple: (借阅记录, 罚款金额)
        """
        user = self.get_user(user_id)
        book = self.get_book(book_id)
        
        # 查找对应的借阅记录
        record = self._find_active_record(user_id, book_id)
        if record is None:
            raise ValueError(f"未找到用户 {user_id} 借阅图书 {book_id} 的记录")
        
        # 计算罚款并归还
        fine = record.return_book()
        book.return_book()
        user.remove_borrowed_book(book_id)
        
        if fine > 0:
            user.add_overdue()
        
        self._total_returns += 1
        self._logger.info(f"Returned: User {user_id} returned Book {book_id}, Fine: {fine}")
        self._record_operation("RETURN", record.record_id)
        
        return record, fine
    
    def _find_active_record(self, user_id: str, book_id: str) -> Optional[BorrowRecord]:
        """查找活跃的借阅记录"""
        for record in self._borrow_records:
            if (record.user_id == user_id and 
                record.book_id == book_id and 
                record.is_active):
                return record
        return None
    
    def _return_book_interactive(self) -> None:
        """交互式还书"""
        print("\n--- 还书 ---")
        user_id = input("请输入用户ID: ").strip()
        book_id = input("请输入图书ID: ").strip()
        
        try:
            record, fine = self.return_book(user_id, book_id)
            book = self.get_book(book_id)
            
            print(f"\n[成功] 还书成功！")
            print(f"  图书: {book.title}")
            print(f"  借阅天数: {record.days_borrowed}")
            
            if fine > 0:
                print(f"  [警告] 逾期 {record.days_overdue} 天，罚款: ¥{fine:.2f}")
            
        except Exception as e:
            print(f"\n[错误] {e}")
    
    def renew_book(self, user_id: str, book_id: str, extra_days: int = 14) -> None:
        """续借图书"""
        record = self._find_active_record(user_id, book_id)
        if record is None:
            raise ValueError(f"未找到借阅记录")
        
        if record.days_overdue > 0:
            raise ValueError(f"逾期图书无法续借")
        
        record.extend_due_date(extra_days)
        self._logger.info(f"Renewed: User {user_id} renewed Book {book_id}")
    
    def _renew_book_interactive(self) -> None:
        """交互式续借"""
        print("\n--- 续借 ---")
        user_id = input("请输入用户ID: ").strip()
        book_id = input("请输入图书ID: ").strip()
        
        try:
            self.renew_book(user_id, book_id)
            book = self.get_book(book_id)
            record = self._find_active_record(user_id, book_id)
            
            print(f"\n[成功] 续借成功！")
            print(f"  图书: {book.title}")
            print(f"  新应还日期: {record.due_date}")
            
        except Exception as e:
            print(f"\n[错误] {e}")
    
    def reserve_book(self, user_id: str, book_id: str) -> bool:
        """预约图书"""
        user = self.get_user(user_id)
        book = self.get_book(book_id)
        
        if book.is_available:
            # 直接借书而不是预约
            return False
        
        # 添加到预约队列
        if book_id not in self._reservation_queue:
            self._reservation_queue[book_id] = ArrayQueue()
        
        self._reservation_queue[book_id].enqueue(user_id)
        user.add_reserved_book(book_id)
        
        self._logger.info(f"Reserved: User {user_id} reserved Book {book_id}")
        return True
    
    def _reserve_book_interactive(self) -> None:
        """交互式预约"""
        print("\n--- 预约图书 ---")
        user_id = input("请输入用户ID: ").strip()
        book_id = input("请输入图书ID: ").strip()
        
        try:
            book = self.get_book(book_id)
            
            if book.is_available:
                print(f"\n[提示] 图书 '{book.title}' 当前可借，请直接借阅")
                return
            
            self.reserve_book(user_id, book_id)
            print(f"\n[成功] 预约成功！")
            print(f"  图书: {book.title}")
            print(f"  预约队列位置: {len(self._reservation_queue.get(book_id, []))}")
            
        except Exception as e:
            print(f"\n[错误] {e}")
    
    def _show_borrow_records(self) -> None:
        """显示借阅记录"""
        print("\n--- 借阅记录 ---")
        print("1. 查看所有记录")
        print("2. 按用户查询")
        print("3. 按图书查询")
        print("4. 活跃借阅记录")
        
        choice = input("请选择: ").strip()
        
        if choice == '1':
            self._display_all_records()
        elif choice == '2':
            user_id = input("请输入用户ID: ").strip()
            self._display_user_records(user_id)
        elif choice == '3':
            book_id = input("请输入图书ID: ").strip()
            self._display_book_records(book_id)
        elif choice == '4':
            self._display_active_records()
    
    def _display_all_records(self) -> None:
        """显示所有借阅记录"""
        records = list(self._borrow_records)
        
        if not records:
            print("\n暂无借阅记录")
            return
        
        for i, record in enumerate(records, 1):
            print(f"{i:3}. {record}")
        
        print(f"\n共 {len(records)} 条记录")
    
    def _display_user_records(self, user_id: str) -> None:
        """显示指定用户的借阅记录"""
        records = [r for r in self._borrow_records if r.user_id == user_id]
        
        if not records:
            print(f"\n用户 {user_id} 暂无借阅记录")
            return
        
        for i, record in enumerate(records, 1):
            print(f"{i:3}. {record}")
        
        print(f"\n共 {len(records)} 条记录")
    
    def _display_book_records(self, book_id: str) -> None:
        """显示指定图书的借阅记录"""
        records = [r for r in self._borrow_records if r.book_id == book_id]
        
        if not records:
            print(f"\n图书 {book_id} 暂无借阅记录")
            return
        
        for i, record in enumerate(records, 1):
            print(f"{i:3}. {record}")
        
        print(f"\n共 {len(records)} 条记录")
    
    def _display_active_records(self) -> None:
        """显示活跃借阅记录"""
        records = [r for r in self._borrow_records if r.is_active]
        
        if not records:
            print("\n当前无活跃借阅记录")
            return
        
        for i, record in enumerate(records, 1):
            print(f"{i:3}. {record}")
        
        print(f"\n共 {len(records)} 条活跃记录")
    
    def _show_overdue_books(self) -> None:
        """显示逾期图书"""
        overdue_records = [r for r in self._borrow_records 
                          if r.is_active and r.is_overdue]
        
        if not overdue_records:
            print("\n暂无逾期图书")
            return
        
        print("\n--- 逾期图书列表 ---")
        
        for i, record in enumerate(overdue_records, 1):
            book = self._books.get(record.book_id)
            user = self._users.get(record.user_id)
            
            if book and user:
                fine = record.calculate_fine()
                print(f"{i:3}. {book.title}")
                print(f"     借阅者: {user.name}")
                print(f"     逾期天数: {record.days_overdue}")
                print(f"     罚款金额: ¥{fine:.2f}")
        
        total_fine = sum(r.calculate_fine() for r in overdue_records)
        print(f"\n共 {len(overdue_records)} 本逾期图书")
        print(f"总罚款金额: ¥{total_fine:.2f}")
    
    # ========== 信息查询 ==========
    
    def _query_menu(self) -> None:
        """信息查询子菜单"""
        while True:
            print("\n" + "=" * 40)
            print("    信息查询 - Information Query")
            print("=" * 40)
            print("  1. 图书统计 - Book Statistics")
            print("  2. 用户统计 - User Statistics")
            print("  3. 热门图书 - Popular Books")
            print("  4. 范围查询 - Range Query")
            print("  0. 返回主菜单 - Back")
            print("-" * 40)
            
            choice = input("请输入选项: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self._show_book_statistics()
            elif choice == '2':
                self._show_user_statistics()
            elif choice == '3':
                self._show_popular_books()
            elif choice == '4':
                self._range_query_interactive()
            else:
                print("[提示] 无效选项")
    
    def _show_book_statistics(self) -> None:
        """显示图书统计信息"""
        total_books = len(self._books)
        
        # 统计各状态图书数量
        status_count = {}
        category_count = {}
        
        for book in self._books.values():
            status_count[book.status] = status_count.get(book.status, 0) + 1
            category_count[book.category] = category_count.get(book.category, 0) + 1
        
        print("\n--- 图书统计 ---")
        print(f"  图书总数: {total_books}")
        print("\n  按状态统计:")
        for status, count in status_count.items():
            print(f"    {status}: {count}")
        
        print("\n  按分类统计:")
        for category, count in sorted(category_count.items()):
            print(f"    {category}: {count}")
    
    def _show_user_statistics(self) -> None:
        """显示用户统计信息"""
        total_users = len(self._users)
        
        type_count = {}
        status_count = {}
        
        for user in self._users.values():
            type_count[user.user_type] = type_count.get(user.user_type, 0) + 1
            status_count[user.status] = status_count.get(user.status, 0) + 1
        
        print("\n--- 用户统计 ---")
        print(f"  用户总数: {total_users}")
        print(f"  总借阅次数: {self._total_borrows}")
        print(f"  总归还次数: {self._total_returns}")
        
        print("\n  按类型统计:")
        for user_type, count in type_count.items():
            print(f"    {user_type}: {count}")
        
        print("\n  按状态统计:")
        for status, count in status_count.items():
            print(f"    {status}: {count}")
    
    def _show_popular_books(self) -> None:
        """显示热门图书"""
        # 按借阅次数排序
        books = sorted(self._books.values(), key=lambda b: b.borrow_count, reverse=True)
        
        print("\n--- 热门图书 Top 10 ---")
        
        for i, book in enumerate(books[:10], 1):
            print(f"{i:2}. [{book.borrow_count:3}次] {book.title} - {book.author}")
    
    def _range_query_interactive(self) -> None:
        """交互式范围查询（使用BST）"""
        print("\n--- 书名范围查询 ---")
        print("（按书名字母顺序范围查询）")
        
        start = input("起始书名 (如: A): ").strip()
        end = input("结束书名 (如: P): ").strip()
        
        if not start or not end:
            print("[错误] 请输入有效的范围")
            return
        
        # 使用BST进行范围查询
        # 注意：这里简化实现，实际应该基于书名索引
        results = [b for b in self._books.values() 
                   if start.lower() <= b.title[0].lower() <= end.lower()]
        
        if results:
            print(f"\n查询结果 ({start} ~ {end}):")
            for i, book in enumerate(sorted(results, key=lambda b: b.title), 1):
                print(f"{i:3}. {book}")
            print(f"\n共找到 {len(results)} 本图书")
        else:
            print(f"\n未找到书名在 {start}~{end} 范围内的图书")
    
    # ========== 系统设置 ==========
    
    def _system_settings_menu(self) -> None:
        """系统设置子菜单"""
        while True:
            print("\n" + "=" * 40)
            print("    系统设置 - System Settings")
            print("=" * 40)
            print("  1. 保存数据 - Save Data")
            print("  2. 加载数据 - Load Data")
            print("  3. 重置为示例数据 - Reset to Sample")
            print("  4. 撤销操作 - Undo Operation")
            print("  5. 查看操作历史 - View History")
            print("  0. 返回主菜单 - Back")
            print("-" * 40)
            
            choice = input("请输入选项: ").strip()
            
            if choice == '0':
                break
            elif choice == '1':
                self._save_data()
                print("\n[成功] 数据已保存")
            elif choice == '2':
                self._load_data()
                print("\n[成功] 数据已加载")
            elif choice == '3':
                confirm = input("确认重置? 所有数据将丢失 (y/n): ").strip().lower()
                if confirm == 'y':
                    self._books.clear()
                    self._users.clear()
                    self._borrow_records = DoublyLinkedList()
                    self._generate_sample_data()
                    print("\n[成功] 已重置为示例数据")
            elif choice == '4':
                self._undo_last_operation()
            elif choice == '5':
                self._show_operation_history()
            else:
                print("[提示] 无效选项")
    
    def _record_operation(self, op_type: str, target_id: str, 
                          extra_data: Optional[dict] = None) -> None:
        """记录操作到栈（用于撤销）"""
        operation = {
            'type': op_type,
            'target_id': target_id,
            'extra': extra_data,
            'timestamp': datetime.now().isoformat()
        }
        self._operation_stack.push(operation)
    
    def _undo_last_operation(self) -> None:
        """撤销最后一步操作"""
        if self._operation_stack.is_empty():
            print("\n[提示] 没有可撤销的操作")
            return
        
        operation = self._operation_stack.pop()
        print(f"\n[成功] 已撤销操作: {operation['type']}")
    
    def _show_operation_history(self) -> None:
        """显示操作历史"""
        if self._operation_stack.is_empty():
            print("\n暂无操作历史")
            return
        
        print("\n--- 操作历史（最近10条）---")
        
        history = list(self._operation_stack)[:10]
        for i, op in enumerate(history, 1):
            print(f"{i:2}. [{op['timestamp']}] {op['type']}: {op['target_id']}")
    
    # ========== 数据持久化 ==========
    
    def _save_data(self) -> None:
        """保存数据到文件"""
        data = {
            'books': [b.to_dict() for b in self._books.values()],
            'users': [u.to_dict() for u in self._users.values()],
            'records': [r.to_dict() for r in self._borrow_records],
            'statistics': {
                'total_borrows': self._total_borrows,
                'total_returns': self._total_returns
            }
        }
        self._data_manager.save_data(data)
    
    def _load_data(self) -> None:
        """从文件加载数据"""
        data = self._data_manager.load_data()
        
        if data:
            # 加载图书
            for book_data in data.get('books', []):
                book = Book.from_dict(book_data)
                self._books.insert(book.book_id, book)
            
            # 加载用户
            for user_data in data.get('users', []):
                user = User.from_dict(user_data)
                self._users.insert(user.user_id, user)
            
            # 加载借阅记录
            for record_data in data.get('records', []):
                record = BorrowRecord.from_dict(record_data)
                self._borrow_records.add_last(record)
            
            # 加载统计信息
            stats = data.get('statistics', {})
            self._total_borrows = stats.get('total_borrows', 0)
            self._total_returns = stats.get('total_returns', 0)
    
    def _exit_system(self) -> None:
        """退出系统"""
        self._save_data()
        print("\n[系统] 数据已保存")
        print("[系统] 感谢使用图书馆管理系统！再见！")
        self._logger.info("Library system shutdown.")
        exit(0)
