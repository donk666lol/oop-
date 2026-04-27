#7.哈希表
class BookHashTable:
    def __init__(self):
        # 哈希容器：key=book_id，value=书籍节点
        self.hash_map = {}

    # 添加书籍进哈希表
    def add_book(self, book_node):
        self.hash_map[book_node.book_id] = book_node

    # 按ID哈希查找（O(1) 最快）
    def search_by_id(self, book_id):
        if book_id in self.hash_map:
            b = self.hash_map[book_id]
            print(f"✅ 哈希表找到：{b.title} | 作者：{b.author}")
            return b
        print("❌ 哈希表未找到该书籍")
        return None

    # 删除哈希表数据
    def remove_book(self, book_id):
        if book_id in self.hash_map:
            del self.hash_map[book_id]
            print("✅ 哈希表书籍已删除")
            return True
        return False

    # 清空哈希表
    def clear(self):
        self.hash_map.clear()