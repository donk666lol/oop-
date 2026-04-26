import unittest
from stack import Stack
from library_exceptions import EmptyStructureError

class TestStack(unittest.TestCase):
    def test_push_pop(self):
        s = Stack()
        s.push(1)
        self.assertEqual(s.pop(), 1)

    def test_empty_pop(self):
        s = Stack()
        with self.assertRaises(EmptyStructureError):
            s.pop()

if __name__ == "__main__":
    unittest.main()