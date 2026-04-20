	from abc import ABC, abstractmethod
	class BookExistErr(Exception):
	    pass
	class BookNotFoundErr(Exception):
	    pass
	class Book:
	    def __init__(self, bid, title, author):
	        self.bid = bid
	        self.title = title
	        self.author = author
	    def __str__(self):
	        return "ID:" + str(self.bid) + " " + self.title
	class BaseTree(ABC):
	    @abstractmethod
	    def insert(self, book): pass
	    @abstractmethod
	    def search(self, bid): pass
	    @abstractmethod
	    def in_order(self): pass
	class TreeNode:
	    def __init__(self, book):
	        self.book = book
	        self.l = None
	        self.r = None
	class BookBST(BaseTree):
	    def __init__(self):
	        self.root = None
	        self.cmp_cnt = 0 # 用来算查找次数的
	    def insert(self, book):
	        if self.root is None:
	            self.root = TreeNode(book)
	        else:
	            self._insert(self.root, book)
	    def _insert(self, node, book):
	        if book.bid < node.book.bid:
	            if node.l is None:
	                node.l = TreeNode(book)
	            else:
	                self._insert(node.l, book)
	        elif book.bid > node.book.bid:
	            if node.r is None:
	                node.r = TreeNode(book)
	            else:
	                self._insert(node.r, book)
	        else:
	            raise BookExistErr("id重复了")
	    def search(self, bid):
	        self.cmp_cnt = 0
	        res = self._search(self.root, bid)
	        if res is None:
	            raise BookNotFoundErr("找不到这本书")
	        return res
	    def _search(self, node, bid):
	        if node is None:
	            return None
	        self.cmp_cnt += 1
	        if bid == node.book.bid:
	            return node.book
	        elif bid < node.book.bid:
	            return self._search(node.l, bid)
	        else:
	            return self._search(node.r, bid)
	    def delete(self, bid):
	        self.root = self._delete(self.root, bid)
	    def _delete(self, node, bid):
	        if node is None:
	            raise BookNotFoundErr("找不到这本书删不了")
	        if bid < node.book.bid:
	            node.l = self._delete(node.l, bid)
	        elif bid > node.book.bid:
	            node.r = self._delete(node.r, bid)
	        else:
	            if node.l is None:
	                return node.r
	            if node.r is None:
	                return node.l
	            # 找右边最小的顶上去
	            tmp = node.r
	            while tmp.l is not None:
	                tmp = tmp.l
	            node.book = tmp.book
	            node.r = self._delete(node.r, tmp.book.bid)
	        return node
	    def in_order(self):
	        res = []
	        self._in_order(self.root, res)
	        return res
	    def _in_order(self, node, res):
	        if node is not None:
	            self._in_order(node.l, res)
	            res.append(node.book)
	            self._in_order(node.r, res)
	    def pre_order(self):
	        res = []
	        self._pre(self.root, res)
	        return res
	    def _pre(self, node, res):
	        if node is not None:
	            res.append(node.book)
	            self._pre(node.l, res)
	            self._pre(node.r, res)
	    def post_order(self):
	        res = []
	        self._post(self.root, res)
	        return res
	    def _post(self, node, res):
	        if node is not None:
	            self._post(node.l, res)
	            self._post(node.r, res)
	            res.append(node.book)
	if __name__ == '__main__':
	    bst = BookBST()
	    bst.insert(Book(105, "Python", "A"))
	    bst.insert(Book(102, "数据结构", "B"))
	    bst.insert(Book(110, "算法", "C"))
	    bst.insert(Book(101, "C语言", "D"))
	    print("中序遍历:")
	    for b in bst.in_order():
	        print(b)
	    # 查找测试
	    try:
	        b = bst.search(102)
	        print("\n找到了:", b)
	        print("找了", bst.cmp_cnt, "次")
	    except BookNotFoundErr as e:
	        print(e)
	    # 重复插入测试
	    print("\n测试重复插入:")
	    try:
	        bst.insert(Book(105, "xx", "xx"))
	    except BookExistErr as e:
	        print("报错啦:", e)
	    # 删除测试
	    print("\n删除102:")
	    bst.delete(102)
	    for b in bst.in_order():
	        print(b)
