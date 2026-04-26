import unittest
from library_system import LibrarySystem
from library_exceptions import BookNotFoundError, InvalidInputError

class TestSystem(unittest.TestCase):
    def setUp(self):
        self.lib = LibrarySystem()

    def test_borrow(self):
        self.assertEqual(self.lib.borrow_book("1001"), "借阅成功")

    def test_not_found(self):
        with self.assertRaises(BookNotFoundError):
            self.lib.get_book("9999")

def safe_input_book_id():
    try:
        book_id = input("输入图书编号：").strip()
        if not book_id.isdigit() or len(book_id) != 4:
            raise InvalidInputError()
        return book_id
    except:
        print("输入错误，不崩溃，继续运行")
        return None

def run_system():
    lib = LibrarySystem()
    print("=== 图书馆系统 不会崩溃版 ===")
    while True:
        print("\n1 借阅 2 查看 3 退出")
        try:
            c = input("选择：").strip()
            if c == "1":
                bid = safe_input_book_id()
                if bid:
                    print(lib.borrow_book(bid))
            elif c == "2":
                print("所有图书编号：", lib.show_all_books())
            elif c == "3":
                break
            else:
                raise InvalidInputError()
        except Exception as e:
            print("错误：", e, " 系统继续运行")

if __name__ == "__main__":
    print("=== 运行单元测试 ===")
    unittest.main(argv=[""], exit=False)

    print("\n=== 启动系统（乱输也不崩溃）===")
    run_system()