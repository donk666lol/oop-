class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    # 添加书籍
    def add_books(self, node):
        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

    # 删除书籍（修复死循环bug）
    def remove_books(self, book_id):
        current = self.head
        while current:
            if current.book_id == book_id:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next  # 修复这里
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                print("✅ 删除成功")
                return True
            current = current.next  # 移到循环内
        print("❌ 删除失败：未找到该书籍")
        return False

    # 查找书籍（优化输出）
    def find_books(self, title):
        current = self.head
        result = []
        while current:
            if title in current.title:
                result.append(current)  # 返回节点更实用
                print(f"✅ 找到：{current.title} (ID:{current.book_id})")
            current = current.next
        return result

    # 展示全部书籍
    def print_books(self):
        current = self.head
        if not current:
            print("📕 暂无图书")
            return
        print("=" * 60)
        while current:
            print(f"ID:{current.book_id} | 《{current.title}》 | {current.author} | 版本:{current.version}")
            current = current.next
        print("=" * 60)

    # 转为列表，方便数据持久化
    def to_list(self):
        res = []
        cur = self.head
        while cur:
            res.append({
                "title": cur.title,
                "author": cur.author,
                "version": cur.version,
                "book_id": cur.book_id
            })
            cur = cur.next
        return res