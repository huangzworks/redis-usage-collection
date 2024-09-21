def vote_up_key(subject):
    """
    记录投支持票用户的集合。
    """
    return "Vote:{}:up".format(subject)

def vote_down_key(subject):
    """
    记录投反对票用户的集合。
    """
    return "Vote:{}:down".format(subject)

class Vote:

    def __init__(self, client, subject):
        self.client = client
        self.vote_up_set = vote_up_key(subject)
        self.vote_down_set = vote_down_key(subject)

    def up(self, user):
        """
        尝试为用户投下支持票。
        返回True表示投票成功，返回False表示投票失败。
        """
        tx = self.client.pipeline()
        tx.sadd(self.vote_up_set, user)
        tx.srem(self.vote_down_set, user)  # 移除可能存在的反对票
        sadd_result, _ = tx.execute()
        return sadd_result == 1

    def down(self, user):
        """
        尝试为用户投下反对票。
        返回True表示投票成功，返回False表示投票失败。
        """
        tx = self.client.pipeline()
        tx.sadd(self.vote_down_set, user)
        tx.srem(self.vote_up_set, user)  # 移除可能存在的支持票
        sadd_result, _ = tx.execute()
        return sadd_result == 1

    def is_voted(self, user):
        """
        检查用户是否已投票。
        返回True表示已投票，返回False则表示未投票。
        """
        tx = self.client.pipeline()
        tx.sismember(self.vote_up_set, user)
        tx.sismember(self.vote_down_set, user)
        is_up_voted, is_down_voted = tx.execute()
        return is_up_voted or is_down_voted

    def unvote(self, user):
        """
        取消用户的投票。
        若取消成功则返回True，返回False则表示用户尚未投票。
        """
        tx = self.client.pipeline()
        tx.srem(self.vote_up_set, user)
        tx.srem(self.vote_down_set, user)
        unvote_up, unvote_down = tx.execute()
        return unvote_up == 1 or unvote_down == 1

    def up_count(self):
        """
        返回目前投支持票的用户数量。
        """
        return self.client.scard(self.vote_up_set)

    def down_count(self):
        """
        返回目前投反对票的用户数量。
        """
        return self.client.scard(self.vote_down_set)

    def total(self):
        """
        返回目前参与投票的用户总数。
        """
        tx = self.client.pipeline()
        tx.scard(self.vote_up_set)
        tx.scard(self.vote_down_set)
        up_count, down_count = tx.execute()
        return up_count + down_count
