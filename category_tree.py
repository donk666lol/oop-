# 4. 图书分类树
class CategoryNode:
    def __init__(self, category_name):
        self.category_name = category_name
        self.children = []
        self.books = []  # 统一命名

    def add_sub_category(self, child_node):
        self.children.append(child_node)

    def add_book_to_category(self, book_node):
        self.books.append(book_node)

class CategoryTree:
    def __init__(self):
        self.root = CategoryNode("全部图书")

    # 展示分类树（补全实现）
    def show_tree(self, node=None, depth=0):
        if node is None:
            node = self.root
        print("  " * depth + f"📂 {node.category_name}")
        for book in node.books:
            print("  " * (depth + 1) + f"📕 {book.title}")
        for child in node.children:
            self.show_tree(child, depth + 1)

    # 查找图书（补全）
    def find_book(self, title):
        def search(node):
            for b in node.books:
                if title in b.title:
                    return b
            for child in node.children:
                res = search(child)
                if res:
                    return res
            return None
        result = search(self.root)
        if result:
            print(f"✅ 找到：《{result.title}》")
        else:
            print("❌ 未找到")
        return result