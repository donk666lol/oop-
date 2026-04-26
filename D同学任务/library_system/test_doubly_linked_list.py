import unittest
from doubly_linked_list import DoublyLinkedList

class TestDLL(unittest.TestCase):
    def test_add(self):
        dll = DoublyLinkedList()
        dll.add_last(1)
        self.assertEqual(dll.traverse(), [1])

    def test_remove(self):
        dll = DoublyLinkedList()
        dll.add_last(2)
        dll.remove(2)
        self.assertTrue(dll.is_empty())

if __name__ == "__main__":
    unittest.main()