class FollowGraph:
    def __init__(self):
        self.adj_list = {}

    def add_user(self, user_id):
        if user_id not in self.adj_list:
            self.adj_list[user_id] = set()

    def follow(self, follower_id, followed_id):
        self.add_user(follower_id)
        self.add_user(followed_id)
        self.adj_list[follower_id].add(followed_id)

    def unfollow(self, follower_id, followed_id):
        if follower_id in self.adj_list:
            self.adj_list[follower_id].discard(followed_id)

    def is_following(self, follower_id, followed_id):
        if follower_id in self.adj_list:
            return followed_id in self.adj_list[follower_id]
        return False

    def get_following(self, user_id):
        return list(self.adj_list.get(user_id, set()))

    def get_followers(self, user_id):
        followers = []
        for uid, following in self.adj_list.items():
            if user_id in following:
                followers.append(uid)
        return followers

    def get_suggestions(self, user_id, limit=5):
        following = self.adj_list.get(user_id, set())
        suggestions = set()
        for followed_id in following:
            for friend_of_friend in self.adj_list.get(followed_id, set()):
                if friend_of_friend != user_id and friend_of_friend not in following:
                    suggestions.add(friend_of_friend)
        return list(suggestions)[:limit]
