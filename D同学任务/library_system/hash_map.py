class HashMap:
    def __init__(self):
        self.size = 10
        self.map = [[] for _ in range(self.size)]

    def _hash(self, key):
        return hash(key) % self.size

    def put(self, key, value):
        index = self._hash(key)
        for i, (k, v) in enumerate(self.map[index]):
            if k == key:
                self.map[index][i] = (key, value)
                return
        self.map[index].append((key, value))

    def get(self, key):
        index = self._hash(key)
        for k, v in self.map[index]:
            if k == key:
                return v
        return None

    def contains(self, key):
        return self.get(key) is not None

    def keys(self):
        keys = []
        for bucket in self.map:
            for k, v in bucket:
                keys.append(k)
        return keys