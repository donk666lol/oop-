import unittest
from data_structures.queue import Queue

class TestQueue(unittest.TestCase):
    def setUp(self):
        self.q = Queue()

    def test_enqueue_dequeue(self):
        self.q.enqueue("book1")
        self.q.enqueue("book2")
        self.assertEqual(self.q.dequeue(), "book1")
        self.assertEqual(self.q.dequeue(), "book2")

    def test_empty_dequeue(self):
        self.assertIsNone(self.q.dequeue())