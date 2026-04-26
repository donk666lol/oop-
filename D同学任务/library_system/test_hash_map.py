import unittest
from hash_map import HashMap

class TestHashMap(unittest.TestCase):
    def test_put_get(self):
        hm = HashMap()
        hm.put("1001", "test")
        self.assertEqual(hm.get("1001"), "test")

    def test_contains(self):
        hm = HashMap()
        hm.put("1002", "ok")
        self.assertTrue(hm.contains("1002"))

if __name__ == "__main__":
    unittest.main()