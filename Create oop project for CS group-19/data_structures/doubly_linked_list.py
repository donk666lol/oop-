#双端链表存借阅历史记录，支持前后遍历。
class DoublyLinkedList:
    class Node:
        def __init__(self, data):
            self._data = data
            self._next = None
            self._prev = None
            
    def __init__(self):
        '''双向链表：head=头车厢，tail=尾车厢'''
        self._head = None
        self._tail = None
    def append(self, data):
        '''在链表末尾添加节点'''
        new_node = self.Node(data)
        if not self._head:
            self._head = self._tail = new_node
        else:
            new_node._prev = self._tail
            self._tail._next = new_node
            self._tail = new_node
    def prepend(self, data):
        '''在链表头部添加节点'''
        new_node = self.Node(data)
        if not self._head:
            self._head = self._tail = new_node
        else:
            new_node._next = self._head
            self._head._prev = new_node
            self._head = new_node
    def display_forward(self):
        '''从头到尾显示链表内容'''
        current = self._head
        while current:
            print(current._data, end=" <-> ")
            current = current._next
        print("None")
    def display_backward(self):
        '''从尾到头显示链表内容'''
        current = self._tail
        while current:
            print(current._data, end=" <-> ")
            current = current._prev
        print("None")
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