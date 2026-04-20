from enum import Enum
from datetime import datetime, timedelta


class BorrowStatus(Enum):
    borrowed = '已借出'
    returned = '已归还'
    overdue = '已逾期'
    renewed = '已续借'

class BorrowRecord:

    borrow_duration={
        'student': 30,
        'teacher': 60,
        'staff': 14,
        'admin': 90

    }

    max_count = 2

    def __init__(self, record_id: str, book_id: str, user_id: str, user_type: str):
        self._record_id = record_id
        self._book_id = book_id
        self._user_id = user_id
        self._user_type = user_type
        self._borrow_date = datetime.now()
        self._due_date = self._borrow_date + timedelta(days=self.borrow_duration.get(user_type, 30))
        self._return_date = None
        self._status = BorrowStatus.borrowed
        self._renew_count = 0


    @property
    def record_id(self):
        return self._record_id 
    
    @property
    def book_id(self):
        return self._book_id
    
    @property
    def user_id(self):
        return self._user_id
    
    @property
    def borrow_date(self):
        return self._borrow_date
    
    @property
    def due_date(self):
        return self._due_date
    
    @property
    def return_date(self):
        return self._return_date
    
    @property
    def status(self):
        return self._status
    
    @property
    def renew_count(self):
        return self._renew_count
    

    def renew(self):
        if self._renew_count >= self.max_count:
            return False
        self._due_date += timedelta(days = self.borrow_duration.get(self._user_type, 30))
        self._renew_count += 1
        return True
    
    def return_book(self):
        self._return_date = datetime.now()
        self._status = BorrowStatus.returned


    def is_overdue(self):
        if self._status == BorrowStatus.returned:
            return False
        return datetime.now() > self._due_date

    def get_overdue_days(self):
        if not self.is_overdue():
            return 0
        return (datetime.now() - self._due_date).days

    def __str__(self):
        return f'borrowrecord({self._record_id},{self._book_id},{self._user_id},{self._status.value})'


