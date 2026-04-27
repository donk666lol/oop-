from data_structures.doubly_linked_list import DoublyLinkedList
from data_structures.hash_map import HashMap
from data_structures.stack import Stack

class Library:
    #图书馆核心管理器
    def __init__(self):
        self.book_map = HashMap()                    
        # 用哈希表存图书，按ID快速查
        self.member_map = HashMap()                   
        # 用哈希表存会员
        self.loan_history = DoublyLinkedList()        
        # 用双向链表存借阅记录
        self.undo_stack = Stack()                     
        # 用栈存操作历史（撤销）
    def add_book(self, book):
        self.book_map.put(book.get_id(), book)
    def get_book(self, book_id):
        return self.book_map.get(book_id)
    def add_member(self, member):
        self.member_map.put(member.get_id(), member)
    def get_member(self, member_id):
        return self.member_map.get(member_id)
    def search_book(self, keyword):
        #搜索书名包含关键词的书（遍历）
        results = []
        for book in self.book_map.get_all():
            if keyword.lower() in book.get_name().lower():
                results.append(book)
        return results
    def get_all_books(self):
        return self.book_map.get_all()
    def get_all_members(self):
        return self.member_map.get_all()
    def add_loan(self, loan):
        #添加借阅记录
        self.loan_history.append(loan)
    def get_loan_history(self):
        return self.loan_history.get_all()