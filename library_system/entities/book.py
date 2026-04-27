# -*- coding: utf-8 -*-
"""
图书实体模块 - Book Entity Module

本模块定义图书类，是系统的核心实体之一。

设计说明：
1. 使用属性装饰器(@property)实现封装
2. 实现比较运算符用于排序
3. 实现字符串表示方法用于输出
4. 使用枚举表示图书状态

OOP概念展示：
- 类与对象
- 封装（私有属性 + 属性访问器）
- 特殊方法重写(__str__, __repr__, __eq__, __lt__等)
- 类属性（所有图书总数统计）
- 静态方法
"""

from datetime import date, datetime
from typing import Optional
from enum import Enum, auto


class BookStatus(Enum):
    """
    图书状态枚举
    
    使用枚举而不是字符串常量的优点：
    1. 类型安全，编译时检查
    2. 自动补全支持
    3. 避免拼写错误
    4. 可迭代
    """
    AVAILABLE = auto()      # 可借阅
    BORROWED = auto()       # 已借出
    RESERVED = auto()       # 已预约
    OVERDUE = auto()        # 逾期未还
    MAINTENANCE = auto()    # 维护中
    LOST = auto()           # 已丢失
    
    def __str__(self) -> str:
        """中文状态名称"""
        names = {
            BookStatus.AVAILABLE: "可借阅",
            BookStatus.BORROWED: "已借出",
            BookStatus.RESERVED: "已预约",
            BookStatus.OVERDUE: "逾期未还",
            BookStatus.MAINTENANCE: "维护中",
            BookStatus.LOST: "已丢失"
        }
        return names[self]


class Book:
    """
    图书类
    
    代表图书馆中的一本图书。
    
    属性：
        book_id: 图书唯一标识符
        isbn: ISBN编号
        title: 书名
        author: 作者
        publisher: 出版社
        publish_year: 出版年份
        category: 分类
        status: 当前状态
        location: 馆藏位置
        borrow_count: 借阅次数
        added_date: 入馆日期
    
    类属性：
        total_books: 图书总数（所有实例共享）
    
    示例：
        >>> book = Book("B001", "9787115428028", "Python编程", "John Smith")
        >>> print(book)
        [B001] Python编程 - John Smith (可借阅)
    """
    
    # 类属性：统计所有图书数量
    total_books = 0
    
    def __init__(self, book_id: str, isbn: str, title: str, author: str,
                 publisher: str = "未知出版社", publish_year: int = 2020,
                 category: str = "未分类", location: str = "A-01-001"):
        """
        初始化图书实例
        
        参数：
            book_id: 图书唯一ID（如：B001）
            isbn: ISBN编号（13位数字）
            title: 书名
            author: 作者
            publisher: 出版社（默认：未知出版社）
            publish_year: 出版年份（默认：2020）
            category: 分类（默认：未分类）
            location: 馆藏位置（默认：A-01-001）
        """
        # 私有属性（封装）
        self._book_id = book_id
        self._isbn = self._validate_isbn(isbn)
        self._title = title
        self._author = author
        self._publisher = publisher
        self._publish_year = publish_year
        self._category = category
        self._location = location
        
        # 状态相关
        self._status = BookStatus.AVAILABLE
        self._current_borrower: Optional[str] = None
        self._borrow_date: Optional[date] = None
        self._due_date: Optional[date] = None
        
        # 统计信息
        self._borrow_count = 0
        self._added_date = date.today()
        
        # 更新类属性
        Book.total_books += 1
    
    def __del__(self):
        """析构方法：减少图书总数"""
        Book.total_books -= 1
    
    # ========== 属性访问器（封装） ==========
    
    @property
    def book_id(self) -> str:
        """获取图书ID"""
        return self._book_id
    
    @property
    def isbn(self) -> str:
        """获取ISBN"""
        return self._isbn
    
    @property
    def title(self) -> str:
        """获取书名"""
        return self._title
    
    @title.setter
    def title(self, value: str) -> None:
        """设置书名"""
        if not value or not value.strip():
            raise ValueError("书名不能为空")
        self._title = value.strip()
    
    @property
    def author(self) -> str:
        """获取作者"""
        return self._author
    
    @author.setter
    def author(self, value: str) -> None:
        """设置作者"""
        self._author = value.strip() if value else "佚名"
    
    @property
    def publisher(self) -> str:
        """获取出版社"""
        return self._publisher
    
    @property
    def publish_year(self) -> int:
        """获取出版年份"""
        return self._publish_year
    
    @property
    def category(self) -> str:
        """获取分类"""
        return self._category
    
    @category.setter
    def category(self, value: str) -> None:
        """设置分类"""
        self._category = value.strip() if value else "未分类"
    
    @property
    def status(self) -> BookStatus:
        """获取状态"""
        return self._status
    
    @property
    def location(self) -> str:
        """获取馆藏位置"""
        return self._location
    
    @location.setter
    def location(self, value: str) -> None:
        """设置馆藏位置"""
        self._location = value.strip() if value else "未知位置"
    
    @property
    def current_borrower(self) -> Optional[str]:
        """获取当前借阅者ID"""
        return self._current_borrower
    
    @property
    def borrow_count(self) -> int:
        """获取借阅次数"""
        return self._borrow_count
    
    @property
    def added_date(self) -> date:
        """获取入馆日期"""
        return self._added_date
    
    @property
    def due_date(self) -> Optional[date]:
        """获取应还日期"""
        return self._due_date
    
    @property
    def is_available(self) -> bool:
        """检查是否可借"""
        return self._status == BookStatus.AVAILABLE
    
    @property
    def is_borrowed(self) -> bool:
        """检查是否已借出"""
        return self._status == BookStatus.BORROWED
    
    @property
    def is_overdue(self) -> bool:
        """检查是否逾期"""
        if self._due_date is None:
            return False
        return date.today() > self._due_date and self._status == BookStatus.BORROWED
    
    # ========== 特殊方法重写 ==========
    
    def __str__(self) -> str:
        """用户友好的字符串表示"""
        return f"[{self._book_id}] {self._title} - {self._author} ({self._status})"
    
    def __repr__(self) -> str:
        """开发者友好的字符串表示"""
        return (f"Book(book_id='{self._book_id}', isbn='{self._isbn}', "
                f"title='{self._title}', author='{self._author}', "
                f"status={self._status.name})")
    
    def __eq__(self, other: object) -> bool:
        """相等比较（基于book_id）"""
        if not isinstance(other, Book):
            return NotImplemented
        return self._book_id == other._book_id
    
    def __lt__(self, other: 'Book') -> bool:
        """小于比较（基于title，用于排序）"""
        if not isinstance(other, Book):
            return NotImplemented
        return self._title < other._title
    
    def __le__(self, other: 'Book') -> bool:
        """小于等于比较"""
        return self == other or self < other
    
    def __gt__(self, other: 'Book') -> bool:
        """大于比较"""
        return not self <= other
    
    def __ge__(self, other: 'Book') -> bool:
        """大于等于比较"""
        return not self < other
    
    def __hash__(self) -> int:
        """哈希值（基于book_id）"""
        return hash(self._book_id)
    
    # ========== 业务方法 ==========
    
    def borrow(self, user_id: str, borrow_days: int = 30) -> bool:
        """
        借阅图书
        
        参数：
            user_id: 借阅者ID
            borrow_days: 借阅天数（默认30天）
            
        返回：
            bool: 借阅成功返回True
            
        示例：
            >>> book.borrow("U001", 14)  # 借阅14天
        """
        if not self.is_available:
            return False
        
        self._status = BookStatus.BORROWED
        self._current_borrower = user_id
        self._borrow_date = date.today()
        self._due_date = date.today().replace(
            day=date.today().day + borrow_days
        )
        self._borrow_count += 1
        return True
    
    def return_book(self) -> bool:
        """
        归还图书
        
        返回：
            bool: 归还成功返回True
        """
        if self._status not in (BookStatus.BORROWED, BookStatus.OVERDUE):
            return False
        
        self._status = BookStatus.AVAILABLE
        self._current_borrower = None
        self._borrow_date = None
        self._due_date = None
        return True
    
    def reserve(self) -> bool:
        """预约图书"""
        if self._status == BookStatus.AVAILABLE:
            self._status = BookStatus.RESERVED
            return True
        return False
    
    def cancel_reservation(self) -> bool:
        """取消预约"""
        if self._status == BookStatus.RESERVED:
            self._status = BookStatus.AVAILABLE
            return True
        return False
    
    def mark_lost(self) -> None:
        """标记为丢失"""
        self._status = BookStatus.LOST
        self._current_borrower = None
        self._borrow_date = None
        self._due_date = None
    
    def mark_maintenance(self) -> None:
        """标记为维护中"""
        self._status = BookStatus.MAINTENANCE
    
    def set_available(self) -> None:
        """设置为可借"""
        self._status = BookStatus.AVAILABLE
    
    def check_overdue(self) -> None:
        """检查并更新逾期状态"""
        if self.is_overdue:
            self._status = BookStatus.OVERDUE
    
    # ========== 辅助方法 ==========
    
    @staticmethod
    def _validate_isbn(isbn: str) -> str:
        """
        验证并格式化ISBN
        
        参数：
            isbn: 待验证的ISBN字符串
            
        返回：
            str: 格式化后的ISBN
            
        异常：
            ValueError: 如果ISBN格式无效
        """
        # 移除分隔符
        isbn_clean = isbn.replace('-', '').replace(' ', '')
        
        # 简单验证：13位数字
        if not isbn_clean.isdigit() or len(isbn_clean) not in (10, 13):
            raise ValueError(f"无效的ISBN格式: {isbn}")
        
        return isbn_clean
    
    def to_dict(self) -> dict:
        """
        转换为字典（用于序列化）
        
        返回：
            dict: 包含图书信息的字典
        """
        return {
            'book_id': self._book_id,
            'isbn': self._isbn,
            'title': self._title,
            'author': self._author,
            'publisher': self._publisher,
            'publish_year': self._publish_year,
            'category': self._category,
            'location': self._location,
            'status': self._status.name,
            'current_borrower': self._current_borrower,
            'borrow_date': self._borrow_date.isoformat() if self._borrow_date else None,
            'due_date': self._due_date.isoformat() if self._due_date else None,
            'borrow_count': self._borrow_count,
            'added_date': self._added_date.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Book':
        """
        从字典创建图书实例（用于反序列化）
        
        参数：
            data: 包含图书信息的字典
            
        返回：
            Book: 图书实例
        """
        book = cls(
            book_id=data['book_id'],
            isbn=data['isbn'],
            title=data['title'],
            author=data['author'],
            publisher=data.get('publisher', '未知出版社'),
            publish_year=data.get('publish_year', 2020),
            category=data.get('category', '未分类'),
            location=data.get('location', 'A-01-001')
        )
        
        # 恢复状态
        if 'status' in data:
            book._status = BookStatus[data['status']]
        if 'current_borrower' in data:
            book._current_borrower = data['current_borrower']
        if 'borrow_date' in data and data['borrow_date']:
            book._borrow_date = date.fromisoformat(data['borrow_date'])
        if 'due_date' in data and data['due_date']:
            book._due_date = date.fromisoformat(data['due_date'])
        if 'borrow_count' in data:
            book._borrow_count = data['borrow_count']
        if 'added_date' in data:
            book._added_date = date.fromisoformat(data['added_date'])
        
        return book
    
    @staticmethod
    def get_status_list() -> list[str]:
        """获取所有状态列表"""
        return [status.name for status in BookStatus]
    
    @classmethod
    def get_total_count(cls) -> int:
        """获取图书总数"""
        return cls.total_books
