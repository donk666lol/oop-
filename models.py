import json

# 1. 双向链表来存储图书信息
class BooksNode:
    def __init__(self, title, author, version, book_id):
        self.title = title
        self.author = author
        self.version = version
        self.book_id = book_id
        self.prev = None
        self.next = None
        
# 4. 图书分类树
class CategoryNode:
    def __init__(self, category_name):
        self.category_name = category_name
        self.children = []
        self.books = []  # 统一命名

    def add_sub_category(self, child_node):
        self.children.append(child_node)

    def add_book_to_category(self, book_node):
        self.books.append(book_node)