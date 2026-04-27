class BSTNode:
    def __init__(self, book_node):
        self.book = book_node  # 存书籍对象
        self.left = None       # 左子树 <
        self.right = None      # 右子树 >

class BinarySearchTree:
    def __init__(self):
        self.root = None

    # 插入节点（按 book_id 排序）
    def insert(self, book_node):
        new_node = BSTNode(book_node)
        if not self.root:
            self.root = new_node
            return

        current = self.root
        while True:
            if book_node.book_id < current.book.book_id:
                if not current.left:
                    current.left = new_node
                    break
                current = current.left
            else:
                if not current.right:
                    current.right = new_node
                    break
                current = current.right

    # BST 二分查找（按 ID 查找，速度极快）
    def search_by_id(self, book_id):
        current = self.root
        while current:
            if book_id == current.book.book_id:
                return current.book  # 找到
            elif book_id < current.book.book_id:
                current = current.left
            else:
                current = current.right
        return None  # 没找到