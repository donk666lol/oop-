# -*- coding: utf-8 -*-
"""
用户实体模块 - User Entity Module

本模块定义用户类，代表图书馆的注册用户。

设计说明：
1. 使用枚举表示用户类型和状态
2. 实现借阅限制逻辑
3. 记录用户活动历史

OOP概念展示：
- 封装：私有属性 + 属性访问器
- 类属性：用户总数统计
- 特殊方法：字符串表示、比较运算
- 静态方法：验证逻辑
"""

from datetime import date, datetime
from typing import Optional, List
from enum import Enum, auto


class UserType(Enum):
    """用户类型枚举"""
    STUDENT = auto()     # 学生
    TEACHER = auto()     # 教师
    STAFF = auto()       # 职工
    ADMIN = auto()       # 管理员
    
    def __str__(self) -> str:
        names = {
            UserType.STUDENT: "学生",
            UserType.TEACHER: "教师",
            UserType.STAFF: "职工",
            UserType.ADMIN: "管理员"
        }
        return names[self]


class UserStatus(Enum):
    """用户状态枚举"""
    ACTIVE = auto()      # 正常
    SUSPENDED = auto()   # 暂停
    DELETED = auto()     # 已删除
    
    def __str__(self) -> str:
        names = {
            UserStatus.ACTIVE: "正常",
            UserStatus.SUSPENDED: "暂停",
            UserStatus.DELETED: "已删除"
        }
        return names[self]


class User:
    """
    用户类
    
    代表图书馆的注册用户。
    
    属性：
        user_id: 用户唯一标识符
        name: 姓名
        email: 邮箱
        user_type: 用户类型
        status: 账户状态
        register_date: 注册日期
        borrowed_books: 当前借阅的图书ID列表
        borrow_history: 借阅历史记录ID列表
    
    类属性：
        total_users: 用户总数
        BORROW_LIMITS: 各类型用户的借阅上限
    
    示例：
        >>> user = User("U001", "张三", "zhangsan@example.com", UserType.STUDENT)
        >>> user.can_borrow()  # 检查是否可以借书
    """
    
    # 类属性：用户总数
    total_users = 0
    
    # 类属性：各类型用户的借阅上限
    BORROW_LIMITS = {
        UserType.STUDENT: 5,
        UserType.TEACHER: 10,
        UserType.STAFF: 5,
        UserType.ADMIN: 20
    }
    
    # 各类型用户的借阅天数上限
    BORROW_DAYS = {
        UserType.STUDENT: 30,
        UserType.TEACHER: 60,
        UserType.STAFF: 30,
        UserType.ADMIN: 90
    }
    
    def __init__(self, user_id: str, name: str, email: str,
                 user_type: UserType = UserType.STUDENT,
                 phone: str = "", department: str = ""):
        """
        初始化用户实例
        
        参数：
            user_id: 用户ID（如：U001）
            name: 姓名
            email: 邮箱地址
            user_type: 用户类型（默认：学生）
            phone: 电话号码
            department: 部门/学院
        """
        # 基本信息
        self._user_id = user_id
        self._name = name
        self._email = self._validate_email(email)
        self._user_type = user_type
        self._phone = phone
        self._department = department
        
        # 状态信息
        self._status = UserStatus.ACTIVE
        self._register_date = date.today()
        
        # 借阅信息
        self._borrowed_books: List[str] = []
        self._reserved_books: List[str] = []
        self._overdue_count = 0
        
        # 更新类属性
        User.total_users += 1
    
    def __del__(self):
        """析构方法"""
        User.total_users -= 1
    
    # ========== 属性访问器 ==========
    
    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("姓名不能为空")
        self._name = value.strip()
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str) -> None:
        self._email = self._validate_email(value)
    
    @property
    def user_type(self) -> UserType:
        return self._user_type
    
    @property
    def phone(self) -> str:
        return self._phone
    
    @phone.setter
    def phone(self, value: str) -> None:
        self._phone = value.strip() if value else ""
    
    @property
    def department(self) -> str:
        return self._department
    
    @department.setter
    def department(self, value: str) -> None:
        self._department = value.strip() if value else ""
    
    @property
    def status(self) -> UserStatus:
        return self._status
    
    @property
    def register_date(self) -> date:
        return self._register_date
    
    @property
    def borrowed_books(self) -> List[str]:
        return self._borrowed_books.copy()
    
    @property
    def reserved_books(self) -> List[str]:
        return self._reserved_books.copy()
    
    @property
    def borrowed_count(self) -> int:
        return len(self._borrowed_books)
    
    @property
    def overdue_count(self) -> int:
        return self._overdue_count
    
    @property
    def borrow_limit(self) -> int:
        """获取借阅上限"""
        return self.BORROW_LIMITS[self._user_type]
    
    @property
    def max_borrow_days(self) -> int:
        """获取最大借阅天数"""
        return self.BORROW_DAYS[self._user_type]
    
    @property
    def is_active(self) -> bool:
        return self._status == UserStatus.ACTIVE
    
    # ========== 特殊方法 ==========
    
    def __str__(self) -> str:
        return f"[{self._user_id}] {self._name} ({self._user_type}, {self._status})"
    
    def __repr__(self) -> str:
        return (f"User(user_id='{self._user_id}', name='{self._name}', "
                f"email='{self._email}', type={self._user_type.name})")
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self._user_id == other._user_id
    
    def __lt__(self, other: 'User') -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self._name < other._name
    
    def __hash__(self) -> int:
        return hash(self._user_id)
    
    # ========== 业务方法 ==========
    
    def can_borrow(self) -> bool:
        """
        检查用户是否可以借书
        
        返回：
            bool: 可以借书返回True
            
        条件：
            1. 账户状态正常
            2. 未超过借阅上限
            3. 无逾期记录
        """
        return (self.is_active and 
                self.borrowed_count < self.borrow_limit and 
                self._overdue_count == 0)
    
    def add_borrowed_book(self, book_id: str) -> bool:
        """
        添加借阅记录
        
        参数：
            book_id: 图书ID
            
        返回：
            bool: 添加成功返回True
        """
        if book_id not in self._borrowed_books:
            self._borrowed_books.append(book_id)
            return True
        return False
    
    def remove_borrowed_book(self, book_id: str) -> bool:
        """
        移除借阅记录
        
        参数：
            book_id: 图书ID
            
        返回：
            bool: 移除成功返回True
        """
        if book_id in self._borrowed_books:
            self._borrowed_books.remove(book_id)
            return True
        return False
    
    def add_reserved_book(self, book_id: str) -> bool:
        """添加预约记录"""
        if book_id not in self._reserved_books:
            self._reserved_books.append(book_id)
            return True
        return False
    
    def remove_reserved_book(self, book_id: str) -> bool:
        """取消预约"""
        if book_id in self._reserved_books:
            self._reserved_books.remove(book_id)
            return True
        return False
    
    def add_overdue(self) -> None:
        """增加逾期次数"""
        self._overdue_count += 1
    
    def clear_overdue(self) -> None:
        """清除逾期记录"""
        self._overdue_count = 0
    
    def suspend(self) -> None:
        """暂停账户"""
        self._status = UserStatus.SUSPENDED
    
    def activate(self) -> None:
        """激活账户"""
        self._status = UserStatus.ACTIVE
    
    def delete(self) -> None:
        """删除账户"""
        self._status = UserStatus.DELETED
    
    def upgrade(self, new_type: UserType) -> bool:
        """
        升级用户类型
        
        参数：
            new_type: 新的用户类型
            
        返回：
            bool: 升级成功返回True
        """
        if new_type.value > self._user_type.value:
            self._user_type = new_type
            return True
        return False
    
    # ========== 辅助方法 ==========
    
    @staticmethod
    def _validate_email(email: str) -> str:
        """验证邮箱格式"""
        email = email.strip()
        if '@' not in email:
            raise ValueError(f"无效的邮箱格式: {email}")
        return email
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'user_id': self._user_id,
            'name': self._name,
            'email': self._email,
            'user_type': self._user_type.name,
            'phone': self._phone,
            'department': self._department,
            'status': self._status.name,
            'register_date': self._register_date.isoformat(),
            'borrowed_books': self._borrowed_books,
            'reserved_books': self._reserved_books,
            'overdue_count': self._overdue_count
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        """从字典创建实例"""
        user = cls(
            user_id=data['user_id'],
            name=data['name'],
            email=data['email'],
            user_type=UserType[data.get('user_type', 'STUDENT')],
            phone=data.get('phone', ''),
            department=data.get('department', '')
        )
        
        if 'status' in data:
            user._status = UserStatus[data['status']]
        if 'register_date' in data:
            user._register_date = date.fromisoformat(data['register_date'])
        if 'borrowed_books' in data:
            user._borrowed_books = data['borrowed_books']
        if 'reserved_books' in data:
            user._reserved_books = data['reserved_books']
        if 'overdue_count' in data:
            user._overdue_count = data['overdue_count']
        
        return user
    
    @classmethod
    def get_total_count(cls) -> int:
        """获取用户总数"""
        return cls.total_users
