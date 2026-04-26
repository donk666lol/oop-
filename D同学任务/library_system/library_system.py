from hash_map import HashMap
from doubly_linked_list import DoublyLinkedList
from stack import Stack
from queue import Queue
from library_exceptions import BookNotFoundError, InvalidInputError

class LibrarySystem:
    def __init__(self):
        self.books = HashMap()
        self.borrow_records = DoublyLinkedList()
        self.operation_history = Stack()
        self.reserve_queue = Queue()
        self.books.put("1001", {"name": "Python编程", "status": "在馆"})
        self.books.put("1002", {"name": "数据结构", "status": "已借出"})
        self.books.put("1003", {"name": "计算机网络", "status": "在馆"})

    def get_book(self, book_id):
        book = self.books.get(book_id)
        if not book:
            raise BookNotFoundError(book_id)
        return book

    def borrow_book(self, book_id):
        book = self.get_book(book_id)
        if book["status"] == "已借出":
            return "已借出，无法借阅"
        book["status"] = "已借出"
        self.borrow_records.add_last(book_id)
        self.operation_history.push(f"借阅 {book_id}")
        return "借阅成功"

    def show_all_books(self):
        return self.books.keys()