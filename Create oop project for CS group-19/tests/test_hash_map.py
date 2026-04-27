import unittest
from data_structures.hash_map import HashMap

class TestHashMap(unittest.TestCase):
    def setUp(self):
        self.h = HashMap()

    def test_put_and_get(self):
        self.h.put("book1", {"title": "BOOK1", "author": "AUTHOR1"})
        self.assertIsNotNone(self.h.get("book1"))
        self.assertEqual(self.h.get("book1")["title"], "BOOK1")

    def test_get_nonexistent(self):
        self.assertIsNone(self.h.get("not exist"))

    def test_update(self):
        self.h.put("book1", "BOOK2")
        self.h.put("book1", "BOOK1")
        self.assertEqual(self.h.get("book1"), "BOOK1")

    def test_delete(self):
        self.h.put("book1", "BOOK1")
        self.assertTrue(self.h.delete("book1"))
        self.assertFalse(self.h.delete("not exist"))
        self.assertIsNone(self.h.get("book1"))

    def test_get_all(self):
        self.h.put("book1", 1)
        self.h.put("book2", 2)
        self.h.put("book3", 3)
        self.assertEqual(len(self.h.get_all()), 3)