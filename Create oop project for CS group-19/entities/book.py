'''
图书实体类，体现封装特性
'''

class Book:

    def __init__(self, book_id: str, title: str, author: str, catrgory: str, total_copies: int, price: float = 0.0):
        self._book_id = book_id
        self._title = title
        self._author = author
        self._category = catrgory
        self._total_copies = total_copies
        self._available_copies = total_copies
        self._price = price

    
    @property
    def book_id(self):
        return self._book_id
    
    @property
    def title(self):
        return self._title
    
    @property
    def available_copies(self):
        return self._available_copies
    
    #借书
    def borrow(self):
        if self._available_copies > 0:
            self._total_copies -= 1
            return True
        return False
    
    def return_book(self):
        if self._available_copies < self._total_copies:
            self._available_copies += 1
            return True
        return False
    

    