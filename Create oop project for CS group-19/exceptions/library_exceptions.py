class LibraryError(Exception):
    def __init__(self, message="图书馆系统错误"):
        self.message = message
        super().__init__(self.message)

class InvalidInputError(LibraryError):
    def __init__(self, field, value):
        self.field = field
        self.value = value
        super().__init__(f"输入无效：[{field}={value}]")

class ItemNotFoundError(LibraryError):
    def __init__(self, item_type, item_id):
        self.item_type = item_type
        self.item_id = item_id
        super().__init__(f"未找到{item_type}：{item_id}")

class DuplicateError(LibraryError):
    def __init__(self, item_type, item_id):
        self.item_type = item_type
        self.item_id = item_id
        super().__init__(f"{item_type} {item_id} 已存在，请勿重复添加")

class OverdueError(LibraryError):
    def __init__(self, loan_id, days):
        self.loan_id = loan_id
        self.days = days
        super().__init__(f"借阅记录 {loan_id} 已超期 {days} 天")