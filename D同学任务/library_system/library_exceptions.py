class BookNotFoundError(Exception):
    def __init__(self, book_id):
        self.book_id = book_id
        super().__init__(f"图书编号 {book_id} 不存在")

class InvalidInputError(Exception):
    def __init__(self, msg="输入不合法，请重新输入"):
        self.msg = msg
        super().__init__(self.msg)

class EmptyStructureError(Exception):
    def __init__(self, msg="当前结构为空，无法操作"):
        self.msg = msg
        super().__init__(self.msg)