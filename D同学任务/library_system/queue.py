from library_exceptions import EmptyStructureError

class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise EmptyStructureError()
        return self.items.pop(0)

    def front(self):
        if self.is_empty():
            raise EmptyStructureError()
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0