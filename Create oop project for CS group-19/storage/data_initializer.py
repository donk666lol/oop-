from models.book import FictionBook, NonFictionBook
from models.member import Student, Staff
import random

class DataInitializer:

    @staticmethod
    def generate():
        books = []
        members = []

        genres = ["科幻", "悬疑", "爱情", "历史", "奇幻"]
        subjects = ["物理", "历史", "编程", "数学", "心理"]
        authors_1 = ['王', '李', '张', '刘', '陈', '赵', '孙', '周']
        authors_2 = ['周', '吴', '郑', '赵', '孙', '钱', '郑', '何']

        for i in range(1, 21):
            books.append(FictionBook(
                id=f"B{i:04d}",
                title=f"《小说书名{i}》",
                author=f"{random.choice(authors_1)}某某",
                isbn=f"978-7-{100000+i:06d}",
                genre=random.choice(genres)
            ))

        for i in range(21, 41):
            books.append(NonFictionBook(
                id=f"B{i:04d}",
                title=f"《知识书籍{i}》",
                author=f"{random.choice(authors_2)}某某",
                isbn=f"978-7-{100000+i:06d}",
                subject=random.choice(subjects)
            ))

        for i in range(1, 6):
            members.append(Student(
                id=f"S{i:03d}",
                name=f"学生{i}",
                email=f"student{i}@school.edu",
                student_id=f"2024{i:04d}"
            ))

        for i in range(1, 6):
            members.append(Staff(
                id=f"T{i:03d}",
                name=f"职工{i}",
                email=f"staff{i}@school.edu",
                staff_id=f"EMP{i:04d}"
            ))

        return books, members
```