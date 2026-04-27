import models

# 3. 队列来排队预约书籍借阅
class ReservationQueue:
    def __init__(self):
        self.queue = []  # 存 (borrower, book)

    # 加入队列（修复：存人+书对象）
    def enqueue(self, borrower, book):
        self.queue.append((borrower, book))
        print(f"{borrower} ✅ 成功加入《{book.title}》排队")

    # 查看前面还有几人
    def peek(self, me):
        if not self.queue:
            print("无人排队")
            return None
        for i, (user, book) in enumerate(self.queue):
            if user == me:
                print(f"你前面还有 {i} 人")
                return i
        print("你未排队")
        return False

    # 取消排队
    def cancel(self, me):
        if not self.queue:
            print("📭 队列为空")
            return None
        for i, (user, book) in enumerate(self.queue):
            if user == me:
                self.queue.pop(i)
                print(f"{me} ❌ 已退出《{book.title}》排队")
                return True
        print("你未排队")
        return False

    # 队首借书离开
    def dequeue(self):
        if not self.queue:
            print("📭 无人排队")
            return None
        borrower, book = self.queue.pop(0)
        print(f"{borrower} ✅ 已借走《{book.title}》")
        return borrower

    # 打印队列（修复格式）
    def print_queue(self):
        if not self.queue:
            print("📭 无人排队")
            return
        print("=" * 50)
        for idx, (user, book) in enumerate(self.queue, 1):
            print(f"第{idx}位：{user} → 《{book.title}》")
        print("=" * 50)