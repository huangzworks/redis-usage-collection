class Lottery:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def join(self, player):
        """
        将给定的参与者添加到抽奖活动的名单当中。
        添加成功时返回True，若用户已在名单中则返回False。
        """
        return self.client.sadd(self.key, player) == 1

    def draw(self, number, remove=False):
        """
        随机抽取指定数量的获奖者。
        当可选参数remove的值为True时，获奖者将从名单中被移除。
        """
        if remove is True:
            return self.client.spop(self.key, number)
        else:
            return self.client.srandmember(self.key, number)

    def size(self):
        """
        返回参加抽奖活动的人数。
        """
        return self.client.scard(self.key)
