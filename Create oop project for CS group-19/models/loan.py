class Loan:
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