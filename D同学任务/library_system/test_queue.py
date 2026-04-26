import unittest
from queue import Queue
from library_exceptions import EmptyStructureError

class TestQueue(unittest.TestCase):
    def test_enqueue_dequeue(self):
        q = Queue()
        q.enqueue("a")
        self.assertEqual(q.dequeue(), "a")

    def test_empty_dequeue(self):
        q = Queue()
        with self.assertRaises(EmptyStructureError):
            q.dequeue()

if __name__ == "__main__":
    unittest.main()