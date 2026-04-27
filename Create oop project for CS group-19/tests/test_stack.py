import unittest
from data_structures.stack import Stack

class TestStack(unittest.TestCase):
    def setUp(self):
        self.s = Stack()
    def test_push_pop(self):
        self.s.push("book1")
        self.s.push("book2")
        self.assertEqual(self.s.pop(), "book2")
        self.assertEqual(self.s.pop(), "book1")

    def test_peek(self):
        self.s.push("book1")
        self.assertEqual(self.s.peek(), "book1")
        self.assertEqual(self.s.size(), 1)

    def test_empty_pop(self):
        self.assertIsNone(self.s.pop())