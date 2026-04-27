class Reservation:
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