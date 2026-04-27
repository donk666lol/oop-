from entities.user import User

class Member(User):
    def __init__(self, id, name, email, member_type="普通会员"):
        super().__init__(id, name, email)
        self._member_type = member_type
        self._max_borrow = 3

    def get_max_borrow(self):
        return self._max_borrow

    def can_borrow_more(self):
        return len(self._borrowed_books) < self._max_borrow

    def display_info(self):
        status = f"已借{len(self._borrowed_books)}/{self._max_borrow}本"
        return f"ID:{self._id} | 姓名:{self._name} | 邮箱:{self._email} | {status}"

    def to_dict(self):
        return {
            "_id": self._id, "_name": self._name,
            "_email": self._email, "_member_type": self._member_type,
            "_max_borrow": self._max_borrow,
            "_borrowed_books": [b.get_id() for b in self._borrowed_books],
            "_type": self.__class__.__name__
        }


class Student(Member):
    def __init__(self, id, name, email, student_id):
        super().__init__(id, name, email, "学生")
        self._max_borrow = 5
        self._student_id = student_id

    def to_dict(self):
        d = super().to_dict()
        d["_student_id"] = self._student_id
        return d


class Staff(Member):
    def __init__(self, id, name, email, staff_id):
        super().__init__(id, name, email, "职工")
        self._max_borrow = 10
        self._staff_id = staff_id

    def to_dict(self):
        d = super().to_dict()
        d["_staff_id"] = self._staff_id
        return d