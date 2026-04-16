## 一、项目核心要求（每个要求都必须完成）

| 类别 | 必须包含的内容 |
|------|--------------|
| OOP设计 | 类与对象、封装、继承、多态、组合、抽象类、自定义异常 |
| 数据结构（必须自己写） | 双向链表、栈、队列、树、二叉搜索树、哈希表 |
| 算法 | 递归树遍历、搜索效率分析、时间复杂度说明 |
| 持久化 | 首次运行初始化数据文件（50+条），后续运行加载更新 |
| CRUD | 创建、更新、删除、搜索/查询记录 |
| 错误处理 | 安全处理错误输入，程序不能因用户失误崩溃 |
| 测试 | 单元测试 + 类测试 + 系统测试 |
| 报告 | LaTeX模板，≤10页，4节 |
| 视频 | 演示视频≤10分钟 + 流程视频≤10分钟 |

---

## 二、5人分工总表

| 成员 | 角色 | 核心任务 |
|------|------|---------|
| A同学 | 架构师+数据结构 | 系统架构、基类、双向链表、哈希表、栈、Library类 |
| B同学 | 业务逻辑 | Book/Member/Loan/Reservation类、LibraryService、队列、搜索分析 |
| C同学 | 界面+持久化 | 菜单系统、DataManager、DataInitializer、main.py |
| D同学 | 测试+异常 | 自定义异常体系、全套测试文件 |
| E同学 | 树+报告视频 | 树+BST+递归遍历、LaTeX报告、演示视频、流程视频 |

---

## 三、A同学任务详解（架构师+数据结构）

### A同学要做的事一句话：你是盖楼的地基，所有其他人的代码都依赖你。

### 3.1 先搭架子——两个基类（所有其他类的"老祖宗"）

#### models/entity.py（实体基类）

所有东西（书、会员）都有ID和名字，写成公共类供别人继承。

```python
class Entity:
    """所有东西的基类：都有ID和名字"""
    def __init__(self, id, name):
        self._id = id          # 下划线=私有，不能直接改
        self._name = name

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name
```

#### models/user.py（用户基类）

所有用户都有邮箱和借的书。

```python
class User(Entity):
    """所有用户基类"""
    def __init__(self, id, name, email):
        super().__init__(id, name)   # 继承Entity的id和name
        self._email = email
        self._borrowed_books = []   # 借了哪些书（列表存Book对象）

    def get_email(self):
        return self._email

    def borrow_book(self, book):
        self._borrowed_books.append(book)

    def return_book(self, book):
        if book in self._borrowed_books:
            self._borrowed_books.remove(book)

    def get_borrowed_count(self):
        return len(self._borrowed_books)
```

### 3.2 搭积木——3个数据结构（必须自己写！）

#### data_structures/doubly_linked_list.py（双向链表）

用途：存借阅历史记录，支持前后遍历。相当于一列火车，每节车厢连着前后。

```python
class Node:
    """链表里的一个节点"""
    def __init__(self, data):
        self.data = data      # 存什么数据
        self.prev = None      # 指向前一个节点
        self.next = None      # 指向后一个节点


class DoublyLinkedList:
    """双向链表：head=头车厢，tail=尾车厢"""
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        """在链表末尾添加一个节点"""
        node = Node(data)
        if self.head is None:       # 第一次添加，头尾都指向新节点
            self.head = self.tail = node
        else:                         # 否则挂在尾巴后面
            self.tail.next = node
            node.prev = self.tail
            self.tail = node
        self.size += 1

    def get_all(self):
        """从头到尾遍历一遍，返回所有数据"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def remove(self, data):
        """删除指定数据的节点"""
        current = self.head
        while current:
            if current.data == data:
                # 把前后节点连起来，跳过当前节点
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
                self.size -= 1
                return True
            current = current.next
        return False

    def is_empty(self):
        return self.size == 0
```

#### data_structures/hash_map.py（哈希表）

用途：按ID快速查书/查会员，O(1)速度。相当于字典：用字的读音（哈希值）直接定位页码。

```python
class HashMap:
    """哈希表：用key算出位置，直接定位数据，速度极快"""
    def __init__(self, size=100):
        self.size = size
        self.buckets = [[] for _ in range(size)]  # 100个桶，每个桶是个列表

    def _hash(self, key):
        """把key变成0~99之间的数字（哈希函数）"""
        return hash(key) % self.size

    def put(self, key, value):
        """存入数据：key是什么，数据是什么"""
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:              # key已存在？覆盖它
                bucket[i] = (key, value)
                return
        bucket.append((key, value))   # 不存在？加进去

    def get(self, key):
        """取数据：给定key直接返回结果"""
        index = self._hash(key)
        bucket = self.buckets[index]
        for k, v in bucket:
            if k == key:
                return v
        return None                    # 找不到返回None

    def delete(self, key):
        """删除数据"""
        index = self._hash(key)
        bucket = self.buckets[index]
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return True
        return False

    def get_all(self):
        """获取所有数据"""
        result = []
        for bucket in self.buckets:
            for k, v in bucket:
                result.append(v)
        return result

    def contains(self, key):
        """判断key是否存在"""
        return self.get(key) is not None
```

#### data_structures/stack.py（栈）

用途：撤销最近操作、图书浏览历史。后进先出，像叠盘子。

```python
class Stack:
    """栈：后进先出，最后放上去的最先拿"""
    def __init__(self):
        self._items = []

    def push(self, item):
        """放一个东西到栈顶"""
        self._items.append(item)

    def pop(self):
        """从栈顶拿出一个"""
        if self.is_empty():
            return None
        return self._items.pop()

    def peek(self):
        """看一眼栈顶是什么（但不动它）"""
        return self._items[-1] if self._items else None

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)
```

### 3.3 粘合剂——Library核心管理类

把上面所有东西组合在一起。

#### models/library.py

```python
from data_structures.doubly_linked_list import DoublyLinkedList
from data_structures.hash_map import HashMap
from data_structures.stack import Stack

class Library:
    """
    图书馆核心管理器
    【组合关系】把HashMap、双向链表、栈组合在一起
    """
    def __init__(self):
        self.book_map = HashMap()                    # 用哈希表存图书，按ID快速查
        self.member_map = HashMap()                   # 用哈希表存会员
        self.loan_history = DoublyLinkedList()        # 用双向链表存借阅记录
        self.undo_stack = Stack()                     # 用栈存操作历史（撤销）

    def add_book(self, book):
        self.book_map.put(book.get_id(), book)

    def get_book(self, book_id):
        return self.book_map.get(book_id)

    def add_member(self, member):
        self.member_map.put(member.get_id(), member)

    def get_member(self, member_id):
        return self.member_map.get(member_id)

    def search_book(self, keyword):
        """搜索书名包含关键词的书（遍历）"""
        results = []
        for book in self.book_map.get_all():
            if keyword.lower() in book.get_name().lower():
                results.append(book)
        return results

    def get_all_books(self):
        return self.book_map.get_all()

    def get_all_members(self):
        return self.member_map.get_all()

    def add_loan(self, loan):
        """添加借阅记录"""
        self.loan_history.append(loan)

    def get_loan_history(self):
        return self.loan_history.get_all()
```

### A同学检查清单

- models/entity.py 和 models/user.py 写好了吗？
- 双向链表 append/get_all/remove 三个方法都能用吗？
- 哈希表 put/get/delete/get_all 四个方法都能用吗？
- 栈 push/pop/peek 三个方法都能用吗？
- Library 类组合了 HashMap、双向链表、栈吗？
- 所有属性都用 _ 前缀表示私有了吗？
- 继承用了 super().__init__() 吗？

---

## 四、B同学任务详解（核心业务逻辑）

### B同学要做的事一句话：让系统真正能用，能借书、还书、查书。

### 4.1 写书类（继承关系）

#### models/book.py

```python
class Book(Entity):
    """所有书的公共类"""
    def __init__(self, id, title, author, isbn, category):
        super().__init__(id, title)    # 继承父类的id和name
        self._author = author
        self._isbn = isbn
        self._category = category
        self._is_borrowed = False      # 默认可借

    def borrow(self):
        """借书操作"""
        if self._is_borrowed:
            return False, "这本书已经被借走了"
        self._is_borrowed = True
        return True, "借书成功"

    def return_book(self):
        """还书操作"""
        self._is_borrowed = False

    def get_isbn(self):
        return self._isbn

    def get_author(self):
        return self._author

    def is_available(self):
        return not self._is_borrowed

    def display_info(self):
        """【多态演示】不同类型书显示不同信息"""
        status = "可借" if self.is_available() else "已借出"
        return f"ID:{self._id} | 书名:{self._name} | 作者:{self._author} | ISBN:{self._isbn} | 状态:{status}"

    def to_dict(self):
        """用于保存到文件"""
        return {
            "_id": self._id, "_name": self._name,
            "_author": self._author, "_isbn": self._isbn,
            "_category": self._category, "_is_borrowed": self._is_borrowed,
            "_type": self.__class__.__name__
        }


class FictionBook(Book):
    """小说类——继承Book，多一个体裁属性"""
    def __init__(self, id, title, author, isbn, genre):
        super().__init__(id, title, author, isbn, "小说")
        self._genre = genre      # 体裁：科幻/悬疑/爱情/历史/奇幻

    def display_info(self):
        """【多态】重写display_info，显示体裁"""
        return super().display_info() + f" | 体裁:{self._genre}"

    def to_dict(self):
        d = super().to_dict()
        d["_genre"] = self._genre
        return d


class NonFictionBook(Book):
    """非虚构类——继承Book，多一个学科属性"""
    def __init__(self, id, title, author, isbn, subject):
        super().__init__(id, title, author, isbn, "非虚构")
        self._subject = subject  # 学科：物理/历史/编程/数学/心理

    def display_info(self):
        return super().display_info() + f" | 学科:{self._subject}"

    def to_dict(self):
        d = super().to_dict()
        d["_subject"] = self._subject
        return d
```

#### models/member.py

```python
class Member(User):
    """普通会员：最多借3本"""
    def __init__(self, id, name, email, member_type="普通会员"):
        super().__init__(id, name, email)
        self._member_type = member_type
        self._max_borrow = 3    # 普通会员限借3本

    def get_max_borrow(self):
        return self._max_borrow

    def can_borrow_more(self):
        """判断还能不能继续借书"""
        return len(self._borrowed_books) < self._max_borrow

    def display_info(self):
        status = f"已借{len(self._borrowed_books)}/{self._max_borrow}本"
        return f"ID:{self._id} | 姓名:{self._name} | 邮箱:{self._email} | {status}"

    def to_dict(self):
        return {
            "_id": self._id, "_name": self._name,
            "_email": self._email, "_member_type": self._member_type,
            "_max_borrow": self._max_borrow, "_borrowed_books": [b.get_id() for b in self._borrowed_books],
            "_type": self.__class__.__name__
        }


class Student(Member):
    """学生会员：最多借5本"""
    def __init__(self, id, name, email, student_id):
        super().__init__(id, name, email, "学生")
        self._max_borrow = 5
        self._student_id = student_id

    def to_dict(self):
        d = super().to_dict()
        d["_student_id"] = self._student_id
        return d


class Staff(Member):
    """职工会员：最多借10本"""
    def __init__(self, id, name, email, staff_id):
        super().__init__(id, name, email, "职工")
        self._max_borrow = 10
        self._staff_id = staff_id

    def to_dict(self):
        d = super().to_dict()
        d["_staff_id"] = self._staff_id
        return d
```

### 4.2 写借阅和预约类

#### models/loan.py

```python
class Loan:
    """一条借阅记录"""
    def __init__(self, loan_id, book, member, due_date):
        self._loan_id = loan_id
        self._book = book
        self._member = member
        self._loan_date = "2026-04-16"
        self._due_date = due_date
        self._returned = False

    def return_book(self):
        self._returned = True

    def is_overdue(self):
        return not self._returned

    def get_book(self):
        return self._book

    def get_member(self):
        return self._member

    def display_info(self):
        status = "已还" if self._returned else "未还"
        return f"借阅ID:{self._loan_id} | 书:{self._book.get_name()} | 会员:{self._member.get_name()} | 状态:{status}"

    def to_dict(self):
        return {
            "_loan_id": self._loan_id,
            "_book_id": self._book.get_id(),
            "_member_id": self._member.get_id(),
            "_loan_date": self._loan_date,
            "_due_date": self._due_date,
            "_returned": self._returned
        }
```

#### models/reservation.py

```python
class Reservation:
    """一条预约记录"""
    def __init__(self, book, member, reserve_date):
        self._book = book
        self._member = member
        self._reserve_date = reserve_date
        self._fulfilled = False

    def fulfill(self):
        self._fulfilled = True

    def is_fulfilled(self):
        return self._fulfilled

    def display_info(self):
        status = "已满足" if self._fulfilled else "等待中"
        return f"预约:{self._book.get_name()} | 会员:{self._member.get_name()} | {status}"

    def to_dict(self):
        return {
            "_book_id": self._book.get_id(),
            "_member_id": self._member.get_id(),
            "_reserve_date": self._reserve_date,
            "_fulfilled": self._fulfilled
        }
```

### 4.3 队列（预约等待队列）

#### data_structures/queue.py

```python
class Queue:
    """队列：先进先出，像排队买票"""
    def __init__(self):
        self._items = []

    def enqueue(self, item):
        """加入队列尾部"""
        self._items.append(item)

    def dequeue(self):
        """从队列头部取出"""
        if self.is_empty():
            return None
        return self._items.pop(0)

    def peek(self):
        """看一眼队列头部"""
        return self._items[0] if self._items else None

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def get_all(self):
        return list(self._items)
```

### 4.4 核心业务逻辑

#### services/library_service.py

```python
from models.loan import Loan
from models.reservation import Reservation
from data_structures.queue import Queue

class LibraryService:
    """处理借书/还书/预约的业务逻辑——这是系统的核心"""
    def __init__(self, library):
        self._library = library
        self._reservation_queue = Queue()   # 预约等待队列

    def borrow_book(self, book_id, member_id):
        """借书流程"""
        book = self._library.get_book(book_id)
        member = self._library.get_member(member_id)

        # 检查1：书存在吗？
        if not book:
            return "错误：找不到这本书"
        # 检查2：会员存在吗？
        if not member:
            return "错误：找不到这个会员"
        # 检查3：还能借吗？
        if not member.can_borrow_more():
            return f"错误：你已达到最大借书数量（{member.get_max_borrow()}本）"
        # 检查4：书可借吗？
        if not book.is_available():
            return "错误：这本书已被借走"

        # 借书成功！
        success, msg = book.borrow()
        if success:
            member.borrow_book(book)
            # 存入双向链表（历史记录）
            loan = Loan(f"L{book_id}_{member_id}", book, member, "2026-05-16")
            self._library.add_loan(loan)
            # 存入栈（撤销用）
            self._library.undo_stack.push(("borrow", book, member))
        return msg

    def return_book(self, book_id, member_id):
        """还书流程"""
        book = self._library.get_book(book_id)
        member = self._library.get_member(member_id)
        if book and member:
            book.return_book()
            member.return_book(book)
            self._library.undo_stack.push(("return", book, member))
            return "还书成功"
        return "错误：书或会员不存在"

    def undo(self):
        """撤销最近一次操作"""
        op = self._library.undo_stack.pop()
        if not op:
            return "没有可撤销的操作"
        action, book, member = op
        if action == "borrow":
            book.return_book()
            member.return_book(book)
            return "已撤销借书操作"
        elif action == "return":
            book.borrow()
            member.borrow_book(book)
            return "已撤销还书操作"

    def search_book(self, keyword):
        """搜索图书"""
        return self._library.search_book(keyword)

    def add_book(self, book):
        """添加图书"""
        existing = self._library.get_book(book.get_id())
        if existing:
            return f"错误：图书ID {book.get_id()} 已存在"
        self._library.add_book(book)
        return "添加成功"

    def add_member(self, member):
        """添加会员"""
        existing = self._library.get_member(member.get_id())
        if existing:
            return f"错误：会员ID {member.get_id()} 已存在"
        self._library.add_member(member)
        return "添加成功"

    def save_data(self):
        """保存所有数据到文件"""
        from storage.data_manager import DataManager
        dm = DataManager()
        data = {
            "books": [b.to_dict() for b in self._library.get_all_books()],
            "members": [m.to_dict() for m in self._library.get_all_members()],
            "loans": [l.to_dict() for l in self._library.get_loan_history()]
        }
        dm.save(data)
```

### B同学检查清单

- FictionBook 和 NonFictionBook 继承自 Book 了吗？
- Student 和 Staff 继承自 Member 了吗？
- 不同类型会员的借书限额不同（3/5/10本）吗？
- display_info() 重写了吗（多态）？
- borrow_book() 验证了所有4个条件（书存在、会员存在、有库存、没超限）吗？
- 借还书操作存入了双向链表和栈吗？
- 队列 enqueue/dequeue 能用吗？

---

## 五、C同学任务详解（界面+持久化）

### C同学要做的事一句话：用户能操作程序，关了电脑再打开数据还在。

### 5.1 菜单系统

#### ui/menu_system.py

```python
class MenuSystem:
    """给用户看的文字菜单——程序和用户之间的桥梁"""

    def __init__(self, library_service):
        self._service = library_service
        self._running = True

    def show_main_menu(self):
        print("\n" + "="*35)
        print("       图书馆管理系统")
        print("="*35)
        print(" 1. 添加图书")
        print(" 2. 查找图书")
        print(" 3. 借书")
        print(" 4. 还书")
        print(" 5. 显示所有图书")
        print(" 6. 会员管理")
        print(" 7. 撤销操作")
        print(" 8. 保存并退出")
        print("="*35)

    def run(self):
        """主循环——程序一直运行，直到用户选8退出"""
        print("=== 欢迎使用图书馆系统 ===")
        while self._running:
            self.show_main_menu()
            choice = self._get_choice()

            if choice == 1:   self._add_book()
            elif choice == 2: self._search_book()
            elif choice == 3: self._borrow_book()
            elif choice == 4: self._return_book()
            elif choice == 5: self._show_all_books()
            elif choice == 6: self._manage_member()
            elif choice == 7: self._undo()
            elif choice == 8:
                self._service.save_data()
                print("数据已保存，再见！")
                self._running = False
            else:
                print("无效选择，请输入1-8")

    def _get_choice(self):
        """获取用户输入，有错误保护——程序永远不会崩溃"""
        try:
            return int(input("请选择(1-8): ").strip())
        except ValueError:
            return 0

    def _add_book(self):
        """添加图书"""
        try:
            print("\n--- 添加图书 ---")
            bid = input("图书ID: ").strip()
            title = input("书名: ").strip()
            author = input("作者: ").strip()
            isbn = input("ISBN: ").strip()
            book_type = input("类型(1=小说, 2=非虚构): ").strip()

            if not bid or not title:
                print("⚠ ID和书名不能为空！")
                return

            # 根据类型创建不同的书
            if book_type == "1":
                genre = input("体裁(科幻/悬疑/爱情/历史/奇幻): ").strip()
                from models.book import FictionBook
                book = FictionBook(bid, title, author, isbn, genre)
            else:
                subject = input("学科(物理/历史/编程/数学/心理): ").strip()
                from models.book import NonFictionBook
                book = NonFictionBook(bid, title, author, isbn, subject)

            result = self._service.add_book(book)
            print(f"📖 {result}")
        except Exception as e:
            print(f"⚠ 出错了: {e}")

    def _search_book(self):
        """搜索图书"""
        keyword = input("输入书名关键词: ").strip()
        if not keyword:
            print("⚠ 关键词不能为空！")
            return
        results = self._service.search_book(keyword)
        if results:
            print(f"\n找到 {len(results)} 本书:")
            for b in results:
                print(f"  {b.display_info()}")
        else:
            print("没有找到匹配的书")

    def _borrow_book(self):
        """借书"""
        book_id = input("图书ID: ").strip()
        member_id = input("会员ID: ").strip()
        result = self._service.borrow_book(book_id, member_id)
        print(f"📖 {result}")

    def _return_book(self):
        """还书"""
        book_id = input("图书ID: ").strip()
        member_id = input("会员ID: ").strip()
        result = self._service.return_book(book_id, member_id)
        print(f"📖 {result}")

    def _show_all_books(self):
        """显示所有图书"""
        from models.library import Library
        # 这个方法需要在library_service里暴露
        pass

    def _manage_member(self):
        """会员管理"""
        print("\n--- 会员管理 ---")
        print("1. 添加会员  2. 查看会员")
        choice = input("选择: ").strip()
        if choice == "1":
            mid = input("会员ID: ").strip()
            name = input("姓名: ").strip()
            email = input("邮箱: ").strip()
            mtype = input("类型(1=学生, 2=职工): ").strip()
            if mtype == "1":
                sid = input("学号: ").strip()
                from models.member import Student
                member = Student(mid, name, email, sid)
            else:
                from models.member import Staff
                sid = input("工号: ").strip()
                member = Staff(mid, name, email, sid)
            result = self._service.add_member(member)
            print(f"👤 {result}")

    def _undo(self):
        """撤销操作"""
        result = self._service.undo()
        print(f"↩️  {result}")
```

### 5.2 数据持久化

#### storage/data_manager.py

```python
import json
from pathlib import Path

class DataManager:
    """把数据保存到文件里，下次打开还能读出来"""

    def __init__(self, filepath="data/library_data.json"):
        self._filepath = filepath
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)

    def save(self, data):
        """把数据保存到JSON文件"""
        with open(self._filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✅ 已保存 {len(data.get('books', []))} 本书, {len(data.get('members', []))} 个会员")

    def load(self):
        """从文件读取数据"""
        if not Path(self._filepath).exists():
            print("📁 第一次运行，需要初始化数据")
            return None
        with open(self._filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"📂 已加载 {len(data.get('books', []))} 本书, {len(data.get('members', []))} 个会员")
        return data

    def file_exists(self):
        return Path(self._filepath).exists()
```

### 5.3 自动生成初始数据

#### storage/data_initializer.py

```python
from models.book import FictionBook, NonFictionBook
from models.member import Student, Staff
import random

class DataInitializer:
    """首次运行自动生成50+条图书和10个会员数据"""

    @staticmethod
    def generate():
        books = []
        members = []

        genres = ["科幻", "悬疑", "爱情", "历史", "奇幻"]
        subjects = ["物理", "历史", "编程", "数学", "心理"]
        authors_1 = ['王', '李', '张', '刘', '陈', '赵', '孙', '周']
        authors_2 = ['周', '吴', '郑', '赵', '孙', '钱', '郑', '何']

        # 生成20本小说
        for i in range(1, 21):
            books.append(FictionBook(
                id=f"B{i:04d}",
                title=f"《小说书名{i}》",
                author=f"{random.choice(authors_1)}某某",
                isbn=f"978-7-{100000+i:06d}",
                genre=random.choice(genres)
            ))

        # 生成20本非虚构书
        for i in range(21, 41):
            books.append(NonFictionBook(
                id=f"B{i:04d}",
                title=f"《知识书籍{i}》",
                author=f"{random.choice(authors_2)}某某",
                isbn=f"978-7-{100000+i:06d}",
                subject=random.choice(subjects)
            ))

        # 生成5个学生会员
        for i in range(1, 6):
            members.append(Student(
                id=f"S{i:03d}",
                name=f"学生{i}",
                email=f"student{i}@school.edu",
                student_id=f"2024{i:04d}"
            ))

        # 生成5个职工会员
        for i in range(1, 6):
            members.append(Staff(
                id=f"T{i:03d}",
                name=f"职工{i}",
                email=f"staff{i}@school.edu",
                staff_id=f"EMP{i:04d}"
            ))

        return books, members
```

### 5.4 程序入口

#### main.py

```python
from storage.data_manager import DataManager
from storage.data_initializer import DataInitializer
from models.library import Library
from services.library_service import LibraryService
from ui.menu_system import MenuSystem

def main():
    library = Library()
    service = LibraryService(library)
    data_mgr = DataManager()

    # === 关键：判断首次运行还是加载已有数据 ===
    if data_mgr.file_exists():
        print("📂 检测到已有数据，正在加载...")
        data = data_mgr.load()
        if data:
            # 从保存的数据重建对象
            # （具体实现根据需要来，B同学配合）
            pass
    else:
        print("🆕 首次运行，正在生成初始化数据...")
        books, members = DataInitializer.generate()
        for book in books:
            library.add_book(book)
        for member in members:
            library.add_member(member)
        print(f"✅ 初始化完成！{len(books)} 本书, {len(members)} 个会员")

    # 启动菜单
    menu = MenuSystem(service)
    menu.run()

if __name__ == "__main__":
    main()
```

### C同学检查清单

- 菜单循环不会因输入错误崩溃（try/except包裹了所有输入）？
- JSON文件用utf-8编码，能保存中文？
- main.py 能判断首次/二次运行吗？
- 首次运行自动生成50+条数据？
- 所有菜单选项都有对应的处理函数？
- 保存数据后，下次重启能正确加载？

---

## 六、D同学任务详解（测试+异常）

### D同学要做的事一句话：给系统找bug，保证程序永远不会因为用户乱输入而崩溃。

### 6.1 自定义异常

#### exceptions/library_exceptions.py

```python
# 所有异常的基类
class LibraryError(Exception):
    """图书馆系统异常基类"""
    def __init__(self, message="图书馆系统错误"):
        self.message = message
        super().__init__(self.message)


class InvalidInputError(LibraryError):
    """输入无效"""
    def __init__(self, field, value):
        super().__init__(f"无效的输入 [{field}={value}]")
        self.field = field
        self.value = value


class ItemNotFoundError(LibraryError):
    """找不到东西"""
    def __init__(self, item_type, item_id):
        super().__init__(f"找不到{item_type}: {item_id}")
        self.item_type = item_type
        self.item_id = item_id


class DuplicateError(LibraryError):
    """重复添加"""
    def __init__(self, item_type, item_id):
        super().__init__(f"{item_type} {item_id} 已存在，不能重复添加")


class OverdueError(LibraryError):
    """超期"""
    def __init__(self, loan_id, days):
        super().__init__(f"借阅记录 {loan_id} 已超期 {days} 天")
```

### 6.2 单元测试

#### tests/test_doubly_linked_list.py

```python
import unittest
from data_structures.doubly_linked_list import DoublyLinkedList

class TestDoublyLinkedList(unittest.TestCase):
    def test_append_single(self):
        dll = DoublyLinkedList()
        dll.append("book1")
        self.assertEqual(dll.size, 1)

    def test_append_multiple(self):
        dll = DoublyLinkedList()
        dll.append("a")
        dll.append("b")
        dll.append("c")
        self.assertEqual(dll.size, 3)

    def test_get_all(self):
        dll = DoublyLinkedList()
        dll.append(1)
        dll.append(2)
        dll.append(3)
        self.assertEqual(dll.get_all(), [1, 2, 3])

    def test_remove_from_middle(self):
        dll = DoublyLinkedList()
        dll.append("a")
        dll.append("b")
        dll.append("c")
        dll.remove("b")
        self.assertEqual(dll.get_all(), ["a", "c"])
        self.assertEqual(dll.size, 2)

    def test_remove_nonexistent(self):
        dll = DoublyLinkedList()
        self.assertFalse(dll.remove("notexist"))

    def test_empty_list(self):
        dll = DoublyLinkedList()
        self.assertEqual(dll.get_all(), [])
        self.assertTrue(dll.is_empty())

if __name__ == "__main__":
    unittest.main()
```

#### tests/test_hash_map.py

```python
import unittest
from data_structures.hash_map import HashMap

class TestHashMap(unittest.TestCase):
    def test_put_and_get(self):
        h = HashMap()
        h.put("book1", {"title": "Python入门", "author": "张三"})
        result = h.get("book1")
        self.assertIsNotNone(result)
        self.assertEqual(result["title"], "Python入门")

    def test_get_nonexistent(self):
        h = HashMap()
        self.assertIsNone(h.get("notexist"))

    def test_update(self):
        h = HashMap()
        h.put("key1", "value1")
        h.put("key1", "value2")
        self.assertEqual(h.get("key1"), "value2")

    def test_delete(self):
        h = HashMap()
        h.put("book1", "data")
        self.assertTrue(h.delete("book1"))
        self.assertFalse(h.delete("notexist"))
        self.assertIsNone(h.get("book1"))

    def test_get_all(self):
        h = HashMap()
        h.put("a", 1)
        h.put("b", 2)
        h.put("c", 3)
        self.assertEqual(len(h.get_all()), 3)
```

#### tests/test_stack.py

```python
import unittest
from data_structures.stack import Stack

class TestStack(unittest.TestCase):
    def test_push_pop(self):
        s = Stack()
        s.push("a")
        s.push("b")
        self.assertEqual(s.pop(), "b")   # 后进先出
        self.assertEqual(s.pop(), "a")

    def test_peek(self):
        s = Stack()
        s.push("x")
        self.assertEqual(s.peek(), "x")
        self.assertEqual(s.size(), 1)     # peek不动栈

    def test_empty_pop(self):
        s = Stack()
        self.assertIsNone(s.pop())
```

#### tests/test_queue.py

```python
import unittest
from data_structures.queue import Queue

class TestQueue(unittest.TestCase):
    def test_enqueue_dequeue(self):
        q = Queue()
        q.enqueue("a")
        q.enqueue("b")
        self.assertEqual(q.dequeue(), "a")   # 先进先出
        self.assertEqual(q.dequeue(), "b")

    def test_empty_dequeue(self):
        q = Queue()
        self.assertIsNone(q.dequeue())
```

#### tests/test_system.py（集成测试）

```python
import unittest
from models.library import Library
from models.book import Book
from models.member import Student
from services.library_service import LibraryService

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        """每个测试前自动执行，初始化干净的环境"""
        self.library = Library()
        self.service = LibraryService(self.library)
        self.book = Book("B001", "Python入门", "张三", "978-7-111-00001", "编程")
        self.student = Student("S001", "小明", "xiaoming@test.com", "20240001")
        self.library.add_book(self.book)
        self.library.add_member(self.student)

    def test_borrow_success(self):
        result = self.service.borrow_book("B001", "S001")
        self.assertIn("成功", result)
        self.assertFalse(self.book.is_available())

    def test_borrow_book_not_found(self):
        result = self.service.borrow_book("B999", "S001")
        self.assertIn("找不到", result)

    def test_borrow_member_not_found(self):
        result = self.service.borrow_book("B001", "S999")
        self.assertIn("找不到", result)

    def test_borrow_already_borrowed(self):
        self.service.borrow_book("B001", "S001")
        result = self.service.borrow_book("B001", "S001")
        self.assertIn("已借走", result)

    def test_return_book(self):
        self.service.borrow_book("B001", "S001")
        result = self.service.return_book("B001", "S001")
        self.assertIn("成功", result)
        self.assertTrue(self.book.is_available())

    def test_return_not_borrowed(self):
        result = self.service.return_book("B001", "S001")
        self.assertIn("成功", result)

    def test_undo_borrow(self):
        self.service.borrow_book("B001", "S001")
        result = self.service.undo()
        self.assertIn("撤销", result)
        self.assertTrue(self.book.is_available())
```

### 6.3 运行测试

```bash
# 运行所有测试
cd library_system
python -m unittest discover -s tests -v

# 运行单个文件
python -m unittest tests.test_hash_map -v

# 预期结果：All tests passed!
```

### D同学检查清单

- LibraryError 基类 + 4个子类都写了吗？
- 每个数据结构的每个方法都有测试吗？
- 测试了边界情况（空数据、不存在的key、重复删除）吗？
- 集成测试覆盖了完整借还书流程吗？
- python -m unittest discover -s tests -v 全部通过了吗？
- 故意传入错误数据时，程序不会崩溃吗？

---

## 七、E同学任务详解（树+报告+视频）

### E同学要做的事一句话：最酷的数据结构（树），还要写LaTeX报告和录视频。

### 7.1 树结构

#### data_structures/tree.py（通用树）

```python
class TreeNode:
    """树的节点"""
    def __init__(self, name, data=None):
        self._name = name           # 分类名称
        self._data = data           # 可以存书列表
        self._children = []         # 子节点列表

    def add_child(self, child):
        self._children.append(child)

    def get_children(self):
        return self._children

    def get_name(self):
        return self._name

    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data


class CategoryTree:
    """
    图书分类树
    示例：自然科学 → 物理 → 量子力学
                 → 化学 → 有机化学
          社会科学 → 历史 → 世界史
    """
    def __init__(self, root_name):
        self._root = TreeNode(root_name)

    def add_path(self, path):
        """
        添加一条分类路径
        path = ["自然科学", "物理", "量子力学"]
        效果：在树中创建 自然科学→物理→量子力学 的路径
        """
        current = self._root
        for name in path:
            found = None
            for child in current.get_children():
                if child.get_name() == name:
                    found = child
                    break
            if not found:
                found = TreeNode(name)
                current.add_child(found)
            current = found

    def find_node(self, name):
        """在树中查找节点"""
        return self._find_recursive(self._root, name)

    def _find_recursive(self, node, name):
        if node.get_name() == name:
            return node
        for child in node.get_children():
            result = self._find_recursive(child, name)
            if result:
                return result
        return None

    def get_root(self):
        return self._root
```

#### data_structures/binary_search_tree.py（二叉搜索树）

```python
class BSTNode:
    def __init__(self, book):
        self._book = book
        self._left = None
        self._right = None


class BinarySearchTree:
    """
    二叉搜索树：左子树 < 根 < 右子树
    用途：按ISBN排序存储图书，支持高效范围查询
    """
    def __init__(self):
        self._root = None

    def insert(self, book):
        """插入一本书，按ISBN排序"""
        isbn = book.get_isbn()
        if self._root is None:
            self._root = BSTNode(book)
            return
        self._insert_recursive(self._root, isbn, book)

    def _insert_recursive(self, node, isbn, book):
        if isbn < node._book.get_isbn():
            if node._left is None:
                node._left = BSTNode(book)
            else:
                self._insert_recursive(node._left, isbn, book)
        else:
            if node._right is None:
                node._right = BSTNode(book)
            else:
                self._insert_recursive(node._right, isbn, book)

    def search(self, isbn):
        """搜索指定ISBN的书"""
        return self._search_recursive(self._root, isbn)

    def _search_recursive(self, node, isbn):
        if node is None:
            return None
        if isbn == node._book.get_isbn():
            return node._book
        elif isbn < node._book.get_isbn():
            return self._search_recursive(node._left, isbn)
        else:
            return self._search_recursive(node._right, isbn)

    def get_all_sorted(self):
        """获取所有书（按ISBN排序）"""
        result = []
        self._inorder_recursive(self._root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node is None:
            return
        self._inorder_recursive(node._left, result)
        result.append(node._book)
        self._inorder_recursive(node._right, result)
```

### 7.2 递归遍历算法

#### data_structures/traversal.py

```python
class TreeTraversal:
    """递归树遍历——展示算法的递归之美"""

    @staticmethod
    def preorder(node):
        """
        前序遍历：根 → 左子树 → 右子树
        用途：先处理根节点，再处理子树
        """
        if node is None:
            return []
        result = [node.get_name()]
        for child in node.get_children():
            result += TreeTraversal.preorder(child)
        return result

    @staticmethod
    def postorder(node):
        """
        后序遍历：左子树 → 右子树 → 根
        用途：先处理子节点，再处理根（如计算目录大小）
        """
        if node is None:
            return []
        result = []
        for child in node.get_children():
            result += TreeTraversal.postorder(child)
        result.append(node.get_name())
        return result

    @staticmethod
    def count_nodes(node):
        """
        递归统计节点数量
        时间复杂度：O(n)，每个节点访问一次
        """
        if node is None:
            return 0
        count = 1
        for child in node.get_children():
            count += TreeTraversal.count_nodes(child)
        return count

    @staticmethod
    def bst_inorder(node, result):
        """
        BST中序遍历：左 → 根 → 右
        BST中序遍历结果是有序的！
        """
        if node is None:
            return
        TreeTraversal.bst_inorder(node._left, result)
        result.append(node._book)
        TreeTraversal.bst_inorder(node._right, result)
```

### 7.3 LaTeX报告（使用从MyAberdeen下载的模板）

报告分4个部分，每部分有固定内容：

**第一节：问题与系统设计（约2页）**

```latex
\section{问题与系统设计}
本小组开发了一个图书馆借阅管理系统，用于管理图书借还、会员信息及预约记录。

\subsection{现实场景}
本系统建模图书馆借阅场景，包含以下核心实体：
\begin{itemize}
    \item 图书（Book）：包括小说类（FictionBook）和非虚构类（NonFictionBook）
    \item 会员（Member）：包括学生（Student）和职工（Staff），具有不同借书限额
    \item 借阅记录（Loan）：关联图书和会员，记录借还时间
    \item 预约记录（Reservation）：记录会员对某本书的预约
\end{itemize}

\subsection{为什么用OOP而非脚本}
我们选择面向对象架构的原因：
\begin{itemize}
    \item 代码复用：继承关系使小说类和非虚构类复用图书基类代码
    \item 职责分离：每个类有明确职责，易于维护
    \item 扩展性：新功能只需添加新类，不影响现有代码
    \item 真实建模：用类映射现实实体，更直观
\end{itemize}
```

**第二节：技术设计（约3页）**

```latex
\section{技术设计}
\subsection{面向对象结构}
\begin{itemize}
    \item 抽象基类：Entity定义了所有实体的公共接口（get_id, get_name）
    \item 继承层次：
    \begin{itemize}
        \item Book $\leftarrow$ FictionBook / NonFictionBook
        \item User $\leftarrow$ Member $\leftarrow$ Student / Staff
    \end{itemize}
    \item 组合关系：Library类组合了HashMap、链表、栈、队列、树
    \item 多态：不同类型Book的display_info()方法显示不同信息
\end{itemize}

\subsection{数据结构设计}
\begin{itemize}
    \item 哈希表：O(1)查询图书和会员（给定ID直接定位）
    \item 双向链表：O(n)遍历借阅历史记录（支持前进后退）
    \item 栈：支持撤销最近操作（后进先出）
    \item 队列：处理预约等待列表（先进先出）
    \item 树：表示图书分类层级（自然科学 $\rightarrow$ 物理 $\rightarrow$ 量子力学）
    \item 二叉搜索树：按ISBN排序存储图书，支持高效范围查询
\end{itemize}
```

**第三节：开发与测试（约3页）**

```latex
\section{开发与测试}
\subsection{开发过程}
本项目采用迭代开发：
\begin{enumerate}
    \item 第1-2天：搭建框架，定义基类
    \item 第3-4天：实现数据结构
    \item 第5-6天：实现业务逻辑
    \item 第7天：首次集成测试
    \item 第8-11天：完善功能，修复bug
    \item 第12-14天：测试、报告、视频
\end{enumerate}

\subsection{关键问题与解决}
\textbf{问题1：哈希表冲突处理}
\begin{itemize}
    \item 现象：多个key映射到同一哈希值时发生冲突
    \item 解决：采用链地址法，每个桶是列表，冲突元素依次追加
\end{itemize}

\textbf{问题2：BST插入边界条件}
\begin{itemize}
    \item 现象：空树时插入第一个节点会报错
    \item 解决：在insert方法开头检查root是否为None
\end{itemize}

\subsection{测试策略}
\begin{itemize}
    \item 单元测试：测试每个数据结构和每个类的方法
    \item 集成测试：测试完整的借还书流程
    \item 边界测试：空数据、重复添加、不存在的key
    \item 错误处理：验证程序不会因用户错误输入崩溃
\end{itemize}
```

**第四节：反思（约2页）**

```latex
\section{反思}
\subsection{运行良好的方面}
\begin{itemize}
    \item 模块化设计：各部分解耦，便于独立开发和测试
    \item 数据结构自实现：深刻理解了底层原理
    \item Git协作：每天push，进度透明
\end{itemize}

\subsection{当前设计的局限性}
\begin{itemize}
    \item 未实现图形界面，命令行操作不够直观
    \item 未使用数据库，数据量大时效率有限
    \item 未实现网络功能，不能多用户同时访问
\end{itemize}

\subsection{如果继续开发}
\begin{itemize}
    \item 添加图形用户界面（GUI）
    \item 使用SQLite数据库替代文件存储
    \item 添加逾期罚款计算功能
    \item 实现会员密码登录系统
\end{itemize}

\subsection{对软件设计的新认识}
通过这个项目，我们认识到好的软件设计不是一蹴而就的，而是通过不断迭代、测试、重构逐步完善的。OOP的核心理念是用代码映射现实，这使程序更易理解和维护。
```

### 7.4 视频录制

**演示视频（≤10分钟）脚本：**

| 时间 | 内容 |
|------|------|
| 0:00-1:00 | 启动程序，自动生成50+条数据 |
| 1:00-3:00 | 演示借书（输入会员ID、图书ID→成功→显示借阅记录） |
| 3:00-4:00 | 演示还书 |
| 4:00-5:30 | 演示搜索功能 |
| 5:30-7:00 | 演示错误输入处理（故意输错ID，看程序不崩溃） |
| 7:00-8:30 | 演示撤销功能 |
| 8:30-10:00 | 保存退出，再启动，数据加载成功 |

**流程视频（≤10分钟）脚本：**

每人2分钟，说明：
1. 我负责了什么
2. 遇到了什么问题
3. 怎么解决的
4. 这个项目让我学到了什么

### E同学检查清单

- CategoryTree 能正确添加分类路径吗？
- BinarySearchTree 按ISBN排序插入正确吗？
- 三种递归遍历（preorder/postorder/count_nodes）都能用吗？
- 报告4节都写完并且≤10页了吗？
- 演示视频≤10分钟，覆盖了所有功能吗？
- 流程视频≤10分钟，标注了每个成员的具体贡献吗？

---

## 八、两周每日任务（极简版速查）

### 第一周：打基础

| 天 | A（架构+结构） | B（业务逻辑） | C（界面+持久化） | D（测试+异常） | E（树+报告） |
|---|-------------|-------------|----------------|--------------|-------------|
| **Day1** | 画整体类图，写Entity和User基类 | 确认业务实体，写Book接口 | 设计菜单草图 | 设计异常类清单 | 设计树接口 |
| **Day2** | 写双向链表 | 写Book类+Fiction/NonFiction | 写MenuSystem框架 | 为链表写测试 | 写TreeNode |
| **Day3** | 写哈希表 | 写Member类+Student/Staff | 写DataManager | 为B的类写测试 | 写BinarySearchTree |
| **Day4** | **集成A+B**，确认接口 | 写Loan/Reservation类 | 写DataInitializer | 写Queue测试 | 写递归遍历函数 |
| **Day5** | 写Library组合类 | 写LibraryService业务逻辑 | 集成异常+D集成菜单 | 写HashMap测试 | 写报告第1节 |
| **Day6** | 写Stack（撤销） | 写搜索功能 | 写数据保存加载 | 写DataManager测试 | 写报告第2节 |
| **Day7** | **周日集成**：全员联调，修bug | 修bug | 修bug | 记录bug和修复 | 拍流程视频v1 |

### 第二周：完善+提交

| 天 | A（架构+结构） | B（业务逻辑） | C（界面+持久化） | D（测试+异常） | E（树+报告） |
|---|-------------|-------------|----------------|--------------|-------------|
| **Day8** | 代码审查+优化 | 写搜索效率分析 | 完善菜单所有功能 | 系统集成测试 | 写报告第3节 |
| **Day9** | 完善docstring和注释 | 修测试发现的bug | 修bug | 补充边界测试 | 写报告第4节 |
| **Day10** | 最终整合 | 最终整合 | 确保持久化正常 | 写测试报告 | LaTeX排版 |
| **Day11** | **全员联调** | 全员联调 | 全员联调 | 全员联调 | LaTeX终稿 |
| **Day12** | 录演示视频 | 协助视频 | 录流程视频 | 协助视频 | 视频剪辑 |
| **Day13** | **全组审查** | **全组审查** | **全组审查** | **全组审查** | **全组审查** |
| **Day14** | 打包zip，提交！ | 确认文件完整 | 确认文件完整 | 确认文件完整 | 确认文件完整 |

---

## 九、必须掌握的OOP知识点（在代码中体现）

| 知识点 | 在代码中的体现位置 |
|--------|-----------------|
| 类与对象 | Book, Member, Loan 等都是类，book1 = Book(...) 是对象 |
| 封装 | self._id 加下划线，外部通过 get_id() 访问 |
| 继承 | FictionBook(Book)，Student(Member) |
| 多态 | FictionBook.display_info() 重写了 Book.display_info() |
| 组合 | Library 里有 book_map, loan_history, undo_stack |
| 抽象类 | Entity 是基类，给 Book 和 User 继承 |
| 自定义异常 | ItemNotFoundError, DuplicateError 等 |

## 十、必须掌握的数据结构知识点（在代码中体现）

| 结构 | 用途 | 关键方法 |
|------|------|---------|
| 双向链表 | 借阅历史 | append, get_all, remove |
| 哈希表 | 快速查书/会员 | put, get, delete, get_all |
| 栈 | 撤销操作 | push, pop, peek |
| 队列 | 预约等待 | enqueue, dequeue, peek |
| 树 | 图书分类 | add_path, find_node |
| 二叉搜索树 | ISBN排序索引 | insert, search, get_all_sorted |
| 递归遍历 | 树操作 | preorder, postorder, count_nodes |

---
