class CommentNode:
    def __init__(self, comment):
        self.comment = comment
        self.next = None


class CommentList:
    def __init__(self):
        self.head = None
        self.count = 0

    def add(self, comment):
        node = CommentNode(comment)
        if not self.head:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
        self.count += 1

    def remove(self, comment_id):
        if not self.head:
            return False
        if self.head.comment.id == comment_id:
            self.head = self.head.next
            self.count -= 1
            return True
        current = self.head
        while current.next:
            if current.next.comment.id == comment_id:
                current.next = current.next.next
                self.count -= 1
                return True
            current = current.next
        return False

    def get_all(self):
        result = []
        current = self.head
        while current:
            result.append(current.comment)
            current = current.next
        return result

    def size(self):
        return self.count

    def __iter__(self):
        current = self.head
        while current:
            yield current.comment
            current = current.next

    def __len__(self):
        return self.count
