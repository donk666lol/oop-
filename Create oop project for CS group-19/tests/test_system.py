import unittest
from models.library import Library
from models.book import Book
from models.member import Student
from services.library_service import LibraryService

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        self.library = Library()
        self.service = LibraryService(self.library)
        self.book = Book("B001", "BOOK1")
        self.student = Student("S001", "STUDENT1")
        self.library.add_book(self.book)
        self.library.add_member(self.student)

    def test_borrow_success(self):
        self.assertIn("成功", self.service.borrow_book("B001", "S001"))
        self.assertFalse(self.book.is_available())

    def test_borrow_book_not_found(self):
        self.assertIn("找不到", self.service.borrow_book("B999", "S001"))

    def test_borrow_member_not_found(self):
        self.assertIn("找不到", self.service.borrow_book("B001", "S999"))

    def test_borrow_already_borrowed(self):
        self.service.borrow_book("B001", "S001")
        self.assertIn("已借走", self.service.borrow_book("B001", "S001"))

    def test_return_book(self):
        self.service.borrow_book("B001", "S001")
        self.assertIn("成功", self.service.return_book("B001", "S001"))
        self.assertTrue(self.book.is_available())

    def test_return_not_borrowed(self):
        self.assertIn("成功", self.service.return_book("B001", "S001"))

    def test_undo_borrow(self):
        self.service.borrow_book("B001", "S001")
        self.assertIn("撤销", self.service.undo())
        self.assertTrue(self.book.is_available())