# -*- coding: utf-8 -*-
"""
借阅记录实体模块 - Borrow Record Entity Module

本模块定义借阅记录类，记录图书的借阅历史。

设计说明：
1. 记录完整的借阅生命周期
2. 支持逾期计算和罚款计算
3. 使用组合关系关联Book和User

OOP概念展示：
- 组合关系：BorrowRecord包含book_id和user_id
- 特殊方法：字符串表示、比较运算
- 属性装饰器：封装和计算属性
- 枚举：借阅状态
"""

from datetime import date, datetime, timedelta
from typing import Optional
from enum import Enum, auto


class RecordStatus(Enum):
    """借阅记录状态"""
    ACTIVE = auto()      # 借阅中
    RETURNED = auto()    # 已归还
    OVERDUE = auto()      # 逾期未还
    LOST = auto()        # 已丢失
    FINE_PAID = auto()   # 已缴罚款
    
    def __str__(self) -> str:
        names = {
            RecordStatus.ACTIVE: "借阅中",
            RecordStatus.RETURNED: "已归还",
            RecordStatus.OVERDUE: "逾期未还",
            RecordStatus.LOST: "已丢失",
            RecordStatus.FINE_PAID: "已缴罚款"
        }
        return names[self]


class BorrowRecord:
    """
    借阅记录类
    
    记录一次完整的借阅行为。
    
    属性：
        record_id: 记录唯一ID
        book_id: 图书ID
        user_id: 用户ID
        borrow_date: 借出日期
        due_date: 应还日期
        return_date: 实际归还日期
        status: 当前状态
        fine_amount: 罚款金额
    
    类属性：
        FINE_PER_DAY: 每日罚款金额
    
    示例：
        >>> record = BorrowRecord("R001", "B001", "U001")
        >>> record.calculate_fine()  # 计算罚款
    """
    
    # 类属性：每日罚款金额（元）
    FINE_PER_DAY = 0.5
    
    # 类属性：记录总数（用于生成ID）
    total_records = 0
    
    def __init__(self, record_id: str, book_id: str, user_id: str,
                 borrow_date: Optional[date] = None,
                 due_date: Optional[date] = None,
                 borrow_days: int = 30):
        """
        初始化借阅记录
        
        参数：
            record_id: 记录ID
            book_id: 图书ID
            user_id: 用户ID
            borrow_date: 借出日期（默认今天）
            due_date: 应还日期（默认30天后）
            borrow_days: 借阅天数（默认30天）
        """
        self._record_id = record_id
        self._book_id = book_id
        self._user_id = user_id
        
        # 日期信息
        self._borrow_date = borrow_date or date.today()
        self._due_date = due_date or (self._borrow_date + timedelta(days=borrow_days))
        self._return_date: Optional[date] = None
        
        # 状态信息
        self._status = RecordStatus.ACTIVE
        self._fine_amount = 0.0
        
        # 更新类属性
        BorrowRecord.total_records += 1
    
    def __del__(self):
        BorrowRecord.total_records -= 1
    
    # ========== 属性访问器 ==========
    
    @property
    def record_id(self) -> str:
        return self._record_id
    
    @property
    def book_id(self) -> str:
        return self._book_id
    
    @property
    def user_id(self) -> str:
        return self._user_id
    
    @property
    def borrow_date(self) -> date:
        return self._borrow_date
    
    @property
    def due_date(self) -> date:
        return self._due_date
    
    @property
    def return_date(self) -> Optional[date]:
        return self._return_date
    
    @property
    def status(self) -> RecordStatus:
        return self._status
    
    @property
    def fine_amount(self) -> float:
        return self._fine_amount
    
    @property
    def is_active(self) -> bool:
        return self._status == RecordStatus.ACTIVE
    
    @property
    def is_returned(self) -> bool:
        return self._status == RecordStatus.RETURNED
    
    @property
    def is_overdue(self) -> bool:
        """检查是否逾期"""
        return date.today() > self._due_date and self._status == RecordStatus.ACTIVE
    
    @property
    def days_borrowed(self) -> int:
        """计算已借阅天数"""
        end_date = self._return_date or date.today()
        return (end_date - self._borrow_date).days
    
    @property
    def days_overdue(self) -> int:
        """计算逾期天数"""
        if self._status == RecordStatus.RETURNED:
            return max(0, (self._return_date - self._due_date).days) if self._return_date else 0
        
        if self._status == RecordStatus.ACTIVE:
            return max(0, (date.today() - self._due_date).days)
        
        return 0
    
    # ========== 特殊方法 ==========
    
    def __str__(self) -> str:
        return (f"[{self._record_id}] Book:{self._book_id} User:{self._user_id} "
                f"{self._borrow_date}~{self._due_date} ({self._status})")
    
    def __repr__(self) -> str:
        return (f"BorrowRecord(record_id='{self._record_id}', "
                f"book_id='{self._book_id}', user_id='{self._user_id}')")
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BorrowRecord):
            return NotImplemented
        return self._record_id == other._record_id
    
    def __lt__(self, other: 'BorrowRecord') -> bool:
        if not isinstance(other, BorrowRecord):
            return NotImplemented
        return self._borrow_date < other._borrow_date
    
    def __hash__(self) -> int:
        return hash(self._record_id)
    
    # ========== 业务方法 ==========
    
    def return_book(self, return_date: Optional[date] = None) -> float:
        """
        归还图书
        
        参数：
            return_date: 归还日期（默认今天）
            
        返回：
            float: 罚款金额
        """
        if self._status != RecordStatus.ACTIVE:
            return 0.0
        
        self._return_date = return_date or date.today()
        
        # 计算罚款
        self._fine_amount = self.calculate_fine(self._return_date)
        
        # 更新状态
        if self._fine_amount > 0:
            self._status = RecordStatus.OVERDUE
        else:
            self._status = RecordStatus.RETURNED
        
        return self._fine_amount
    
    def mark_lost(self) -> float:
        """标记为丢失"""
        self._status = RecordStatus.LOST
        self._return_date = date.today()
        self._fine_amount = self.calculate_fine()
        return self._fine_amount
    
    def pay_fine(self) -> None:
        """缴纳罚款"""
        if self._fine_amount > 0:
            self._status = RecordStatus.FINE_PAID
    
    def calculate_fine(self, calc_date: Optional[date] = None) -> float:
        """
        计算罚款金额
        
        参数：
            calc_date: 计算截止日期（默认今天或归还日期）
            
        返回：
            float: 罚款金额
        """
        check_date = calc_date or self._return_date or date.today()
        
        if check_date <= self._due_date:
            return 0.0
        
        overdue_days = (check_date - self._due_date).days
        return overdue_days * self.FINE_PER_DAY
    
    def extend_due_date(self, extra_days: int) -> None:
        """
        续借延长应还日期
        
        参数：
            extra_days: 延长的天数
        """
        if self._status == RecordStatus.ACTIVE:
            self._due_date += timedelta(days=extra_days)
    
    def check_overdue(self) -> bool:
        """
        检查并更新逾期状态
        
        返回：
            bool: 如果逾期返回True
        """
        if self.is_overdue and self._status == RecordStatus.ACTIVE:
            self._status = RecordStatus.OVERDUE
            return True
        return False
    
    # ========== 序列化方法 ==========
    
    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            'record_id': self._record_id,
            'book_id': self._book_id,
            'user_id': self._user_id,
            'borrow_date': self._borrow_date.isoformat(),
            'due_date': self._due_date.isoformat(),
            'return_date': self._return_date.isoformat() if self._return_date else None,
            'status': self._status.name,
            'fine_amount': self._fine_amount
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'BorrowRecord':
        """从字典创建实例"""
        record = cls(
            record_id=data['record_id'],
            book_id=data['book_id'],
            user_id=data['user_id'],
            borrow_date=date.fromisoformat(data['borrow_date']),
            due_date=date.fromisoformat(data['due_date'])
        )
        
        if data.get('return_date'):
            record._return_date = date.fromisoformat(data['return_date'])
        if 'status' in data:
            record._status = RecordStatus[data['status']]
        if 'fine_amount' in data:
            record._fine_amount = data['fine_amount']
        
        return record
    
    @classmethod
    def generate_id(cls, prefix: str = "R") -> str:
        """生成新记录ID"""
        record_num = cls.total_records + 1
        return f"{prefix}{record_num:04d}"
