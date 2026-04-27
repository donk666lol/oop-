from models.loan import Loan
from models.reservation import Reservation
from data_structures.queue import Queue

class LibraryService:
    def __init__(self, library):
        self._library = library
        self._reservation_queue = Queue()

    def borrow_book(self, book_id, member_id):
        book = self._library.get_book(book_id)
        member = self._library.get_member(member_id)

        if not book:
            return "错误：找不到这本书"
        if not member:
            return "错误：找不到这个会员"
        if not member.can_borrow_more():
            return f"错误：你已达到最大借书数量（{member.get_max_borrow()}本）"
        if not book.is_available():
            return "错误：这本书已被借走"

        success, msg = book.borrow()
        if success:
            member.borrow_book(book)
            loan = Loan(f"L{book_id}_{member_id}", book, member, "2026-05-16")
            self._library.add_loan(loan)
            self._library.undo_stack.push(("borrow", book, member))
        return msg

    def return_book(self, book_id, member_id):
        book = self._library.get_book(book_id)
        member = self._library.get_member(member_id)
        if book and member:
            book.return_book()
            member.return_book(book)
            self._library.undo_stack.push(("return", book, member))
            return "还书成功"
        return "错误：书或会员不存在"

    def undo(self):
        op = self._library.undo_stack.pop()
        if not op:
            return "没有可撤销的操作"
        action, book, member = op
        if action == "borrow":
            book.return_book()
            member.return_book(book)
            return "已撤销借书操作"
        elif action == "return":
            book.borrow()
            member.borrow_book(book)
            return "已撤销还书操作"

    def search_book(self, keyword):
        return self._library.search_book(keyword)

    def add_book(self, book):
        existing = self._library.get_book(book.get_id())
        if existing:
            return f"错误：图书ID {book.get_id()} 已存在"
        self._library.add_book(book)
        return "添加成功"

    def add_member(self, member):
        existing = self._library.get_member(member.get_id())
        if existing:
            return f"错误：会员ID {member.get_id()} 已存在"
        self._library.add_member(member)
        return "添加成功"

    def save_data(self):
        from storage.data_manager import DataManager
        dm = DataManager()
        data = {
            "books": [b.to_dict() for b in self._library.get_all_books()],
            "members": [m.to_dict() for m in self._library.get_all_members()],
            "loans": [l.to_dict() for l in self._library.get_loan_history()]
        }
        dm.save(data)