# -*- coding: utf-8 -*-
"""
自定义异常模块 - Custom Exception Module

本模块定义了系统中使用的所有自定义异常类。
自定义异常是OOP设计的重要组成部分，它允许我们：
1. 提供更有意义的错误信息
2. 区分不同类型的错误情况
3. 在调用栈中正确传播错误
4. 实现特定的错误处理逻辑

继承关系：
    LibraryException (基类)
    ├── BookNotFoundException
    ├── BookNotAvailableException
    ├── UserNotFoundException
    ├── DuplicateItemException
    ├── InvalidInputException
    └── OperationLimitException
"""

class LibraryException(Exception):
    """
    图书馆系统基础异常类
    
    所有自定义异常的基类，提供统一的异常接口。
    继承自Python内置Exception类。
    
    属性：
        message (str): 异常的详细信息
        error_code (int): 错误代码，用于程序化错误处理
    
    示例：
        >>> raise LibraryException("系统错误", 1000)
        LibraryException: 系统错误 (Error Code: 1000)
    """
    
    def __init__(self, message: str, error_code: int = 0):
        """
        初始化基础异常
        
        参数：
            message: 异常描述信息
            error_code: 错误代码（默认为0）
        """
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
    
    def __str__(self) -> str:
        """返回异常的字符串表示"""
        if self.error_code:
            return f"{self.message} (Error Code: {self.error_code})"
        return self.message


class BookNotFoundException(LibraryException):
    """
    图书未找到异常
    
    当尝试访问或操作不存在的图书时抛出。
    
    使用场景：
    - 按ID查询图书时图书不存在
    - 尝试借阅不存在的图书
    - 尝试更新或删除不存在的图书记录
    
    示例：
        >>> raise BookNotFoundException("B001")
        BookNotFoundException: 图书 'B001' 未找到
    """
    
    def __init__(self, book_id: str):
        """
        初始化图书未找到异常
        
        参数：
            book_id: 未找到的图书ID
        """
        message = f"图书 '{book_id}' 未找到"
        super().__init__(message, error_code=1001)
        self.book_id = book_id


class BookNotAvailableException(LibraryException):
    """
    图书不可借异常
    
    当尝试借阅已借出或不可借阅的图书时抛出。
    
    使用场景：
    - 借阅已借出的图书
    - 预约正在处理中的图书
    - 借阅已下架的图书
    
    示例：
        >>> raise BookNotAvailableException("B001", "已借出")
        BookNotAvailableException: 图书 'B001' 不可借阅，原因：已借出
    """
    
    def __init__(self, book_id: str, reason: str = "当前不可借阅"):
        """
        初始化图书不可借异常
        
        参数：
            book_id: 图书ID
            reason: 不可借阅的原因
        """
        message = f"图书 '{book_id}' 不可借阅，原因：{reason}"
        super().__init__(message, error_code=1002)
        self.book_id = book_id
        self.reason = reason


class UserNotFoundException(LibraryException):
    """
    用户未找到异常
    
    当尝试访问或操作不存在的用户时抛出。
    
    使用场景：
    - 按ID查询用户时用户不存在
    - 尝试处理不存在用户的借阅请求
    - 尝试更新或删除不存在的用户记录
    
    示例：
        >>> raise UserNotFoundException("U001")
        UserNotFoundException: 用户 'U001' 未找到
    """
    
    def __init__(self, user_id: str):
        """
        初始化用户未找到异常
        
        参数：
            user_id: 未找到的用户ID
        """
        message = f"用户 '{user_id}' 未找到"
        super().__init__(message, error_code=1003)
        self.user_id = user_id


class DuplicateItemException(LibraryException):
    """
    重复项异常
    
    当尝试创建已存在的实体时抛出。
    
    使用场景：
    - 添加已存在的图书（ISBN重复）
    - 注册已存在的用户（ID重复）
    - 创建重复的借阅记录
    
    示例：
        >>> raise DuplicateItemException("图书", "ISBN-123456")
        DuplicateItemException: 图书 'ISBN-123456' 已存在
    """
    
    def __init__(self, item_type: str, item_id: str):
        """
        初始化重复项异常
        
        参数：
            item_type: 项目类型（如"图书"、"用户"）
            item_id: 重复项的ID
        """
        message = f"{item_type} '{item_id}' 已存在"
        super().__init__(message, error_code=1004)
        self.item_type = item_type
        self.item_id = item_id


class InvalidInputException(LibraryException):
    """
    无效输入异常
    
    当用户输入无效数据时抛出。
    
    使用场景：
    - 输入格式不正确
    - 输入值超出允许范围
    - 必填字段为空
    
    示例：
        >>> raise InvalidInputException("图书名称", "不能为空")
        InvalidInputException: 无效的输入：图书名称 不能为空
    """
    
    def __init__(self, field: str, reason: str = ""):
        """
        初始化无效输入异常
        
        参数：
            field: 无效的字段名
            reason: 无效的原因
        """
        if reason:
            message = f"无效的输入：{field} {reason}"
        else:
            message = f"无效的输入：{field}"
        super().__init__(message, error_code=1005)
        self.field = field
        self.reason = reason


class OperationLimitException(LibraryException):
    """
    操作限制异常
    
    当用户操作超过允许的限制时抛出。
    
    使用场景：
    - 用户借书数量超过限制
    - 借阅时长超过最大天数
    - 预约数量超过限制
    
    示例：
        >>> raise OperationLimitException("借书数量", 5, 3)
        OperationLimitException: 借书数量 已达上限（当前：5，上限：3）
    """
    
    def __init__(self, operation: str, current: int, limit: int):
        """
        初始化操作限制异常
        
        参数：
            operation: 操作类型
            current: 当前数量
            limit: 限制数量
        """
        message = f"{operation} 已达上限（当前：{current}，上限：{limit}）"
        super().__init__(message, error_code=1006)
        self.operation = operation
        self.current = current
        self.limit = limit


class DataStructureException(LibraryException):
    """
    数据结构操作异常
    
    当数据结构操作出现问题时抛出。
    
    使用场景：
    - 从空栈弹出元素
    - 从空队列取出元素
    - 访问空链表
    
    示例：
        >>> raise DataStructureException("栈", "不能从空栈弹出")
        DataStructureException: 栈操作错误：不能从空栈弹出
    """
    
    def __init__(self, structure: str, reason: str):
        """
        初始化数据结构异常
        
        参数：
            structure: 数据结构类型
            reason: 错误原因
        """
        message = f"{structure}操作错误：{reason}"
        super().__init__(message, error_code=1007)
        self.structure = structure
        self.reason = reason
