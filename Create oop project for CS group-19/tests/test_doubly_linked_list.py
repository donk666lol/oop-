import unittest
from data_structures.doubly_linked_list import DoublyLinkedList

class TestDoublyLinkedList(unittest.TestCase):
    def setUp(self):
        self.dll = DoublyLinkedList()

    def test_append_single(self):
        self.dll.append("book1")
        self.assertEqual(self.dll.size, 1)

    def test_append_multiple(self):
        self.dll.append("book1")
        self.dll.append("book2")
        self.dll.append("book3")
        self.assertEqual(self.dll.size, 3)

    def test_get_all(self):
        self.dll.append(1)
        self.dll.append(2)
        self.dll.append(3)
        self.assertEqual(self.dll.get_all(), [1, 2, 3])

    def test_remove_from_middle(self):
        self.dll.append("book1")
        self.dll.append("book2")
        self.dll.append("book3")
        self.dll.remove("book2")
        self.assertEqual(self.dll.get_all(), ["book1", "book3"])
        self.assertEqual(self.dll.size, 2)

    def test_remove_nonexistent(self):
        self.assertFalse(self.dll.remove("not exist"))

    def test_empty_list(self):
        self.assertEqual(self.dll.get_all(), [])
        self.assertEqual(self.dll.size, 0)

if __name__ == "__main__":
    unittest.main()