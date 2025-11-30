class PostNode:
    def __init__(self, post):
        self.post = post
        self.next = None


class LinkedListPosts:
    def __init__(self):
        self.head = None
        self.count = 0

    def add(self, post):
        node = PostNode(post)
        node.next = self.head
        self.head = node
        self.count += 1

    def remove(self, post_id):
        if not self.head:
            return False
        if self.head.post.id == post_id:
            self.head = self.head.next
            self.count -= 1
            return True
        current = self.head
        while current.next:
            if current.next.post.id == post_id:
                current.next = current.next.next
                self.count -= 1
                return True
            current = current.next
        return False

    def find(self, post_id):
        current = self.head
        while current:
            if current.post.id == post_id:
                return current.post
            current = current.next
        return None

    def get_all(self):
        result = []
        current = self.head
        while current:
            result.append(current.post)
            current = current.next
        return result

    def size(self):
        return self.count

    def __iter__(self):
        current = self.head
        while current:
            yield current.post
            current = current.next
