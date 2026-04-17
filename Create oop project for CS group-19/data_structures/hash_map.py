#按ID快速查书/查会员，O(1)速度。相当于字典：用字的读音（哈希值）直接定位页码。
class HashMap:
    def __init__(self,size=100):
        self.size=size
        self.table=[[] for _ in range(size)]
    def _index(self,key):
        return hash(key)%self.size
    def put(self,key,value):
        index=self._index(key)
        bucket=self.table[index]
        for i,(k,v) in enumerate(bucket):
            if k==key:
                bucket[i]=(key,value)
                return
        bucket.append((key,value))
    def get(self,key):
        index=self._index(key)
        for k,v in self.table[index]:
            if k==key:
                return v
        return None
    def delete(self,key):
        index=self._index(key)
        bucket=self.table[index]
        for i,(k,v) in enumerate(bucket):
            if k==key:
                del bucket[i]
                return True
        return False
    def is_existent(self,key):
        return self.get(key) is not None