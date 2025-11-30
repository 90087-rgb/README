class HashSet:
    def __init__(self):
        self.buckets = [[] for _ in range(16)]
        self.count = 0

    def _hash(self, key):
        return hash(key) % len(self.buckets)

    def add(self, key):
        idx = self._hash(key)
        if key not in self.buckets[idx]:
            self.buckets[idx].append(key)
            self.count += 1
            return True
        return False

    def remove(self, key):
        idx = self._hash(key)
        if key in self.buckets[idx]:
            self.buckets[idx].remove(key)
            self.count -= 1
            return True
        return False

    def contains(self, key):
        idx = self._hash(key)
        return key in self.buckets[idx]

    def size(self):
        return self.count

    def get_all(self):
        result = []
        for bucket in self.buckets:
            result.extend(bucket)
        return result
