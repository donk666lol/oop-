from entities.book import Book

class Book(Entity):
    """所有书的公共类"""
    def __init__(self, id, title, author, isbn, category):
        super().__init__(id, title)
        self._author = author
        self._isbn = isbn
        self._category = category
        self._is_borrowed = False

    def borrow(self):
        if self._is_borrowed:
            return False, "这本书已经被借走了"
        self._is_borrowed = True
        return True, "借书成功"

    def return_book(self):
        self._is_borrowed = False

    def get_isbn(self):
        return self._isbn

    def get_author(self):
        return self._author

    def is_available(self):
        return not self._is_borrowed

    def display_info(self):
        status = "可借" if self.is_available() else "已借出"
        return f"ID:{self._id} | 书名:{self._name} | 作者:{self._author} | ISBN:{self._isbn} | 状态:{status}"

    def to_dict(self):
        return {
            "_id": self._id, "_name": self._name,
            "_author": self._author, "_isbn": self._isbn,
            "_category": self._category, "_is_borrowed": self._is_borrowed,
            "_type": self.__class__.__name__
        }


class FictionBook(Book):
    def __init__(self, id, title, author, isbn, genre):
        super().__init__(id, title, author, isbn, "小说")
        self._genre = genre

    def display_info(self):
        return super().display_info() + f" | 体裁:{self._genre}"

    def to_dict(self):
        d = super().to_dict()
        d["_genre"] = self._genre
        return d


class NonFictionBook(Book):
    def __init__(self, id, title, author, isbn, subject):
        super().__init__(id, title, author, isbn, "非虚构")
        self._subject = subject

    def display_info(self):
        return super().display_info() + f" | 学科:{self._subject}"

    def to_dict(self):
        d = super().to_dict()
        d["_subject"] = self._subject
        return d