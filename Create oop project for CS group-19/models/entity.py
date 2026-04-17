#书，会员大类，所有东西（书、会员）都有ID和名字，写成公共类供你们继承
class Entity:
    def __init__(self, id, name):
        self._id = id         
        self._name = name
    def get_id(self):
        return self._id
    def get_name(self):
        return self._name
    def set_name(self, name):
        self._name = name