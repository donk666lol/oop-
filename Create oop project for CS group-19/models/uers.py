#用户大类，所有用户都有ID、名字、邮箱，都有借书，还书等功能，写成公共类供你们继承
class User(Entity):
    def __init__(self, id, name, email):
        super().__init__(id, name)   
        self._email = email
        self._borrowed_books = []   

    def get_email(self):
        return self._email

    def borrow_book(self, book):
        self._borrowed_books.append(book)

    def return_book(self, book):
        if book in self._borrowed_books:
            self._borrowed_books.remove(book)

    def get_borrowed_count(self):
        return len(self._borrowed_books)