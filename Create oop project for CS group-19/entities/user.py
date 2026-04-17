from enum import Enum

class UserType(Enum):
    student = 'student'
    teacher = 'teacher'
    staff = 'staff'
    admin = 'admin'


#不同用户类型的最大借阅数
class User:
    max_borrow={
        UserType.student: 5,
        UserType.staff: 3,
        UserType.admin: 20,
        UserType.teacher: 10
    }

    def __init__(self, user_id: str, name: str, user_type: UserType):
        self._user_id = user_id
        self._name = name
        self._user_type = user_type
        self._status = '正常'
        self._current_borrow_count = 0

    @property
    def user_id(self):
        return self._user_id

    @property
    def user_name(self):
        return self.user_name
    
    @property
    def user_type(self):
        return self.user_type
    
    @property
    def user_current_borrow_count(self):
        return self.user_current_borrow_count
    
    @property
    def status(self):
        return self._status
    
    @status.setter
    def status(self,value):
        if value in['正常','暂停','删除']:
            self._status = value


    def get_max_borrow(self):
        return self.max_borrow.get(self._user_type,3)
    
    def can_borrow(self):
        if self._status != '正常':
            if self._status !='正常':
                return False
            return self._current_borrow_count < self.get_max_borrow()
        
    def increase_borrow(self):
        self._current_borrow_count += 1

    def decrease_borrow(self):
        if self._current_borrow_count > 0:
            self._current_borrow_count -= 1

    def __str__(self):
        return f'User({self._user_id}, {self._name},{self._user_type})'