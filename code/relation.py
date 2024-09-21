from time import time

def following_key(user):
    """
    正在关注名单，记录了给定用户当前正在关注的所有人。
    """
    return "Relation:{}:following".format(user)

def followers_key(user):
    """
    关注者名单，记录了当前正在关注给定用户的所有人。
    """
    return "Relation:{}:followers".format(user)

class Relation:

    def __init__(self, client, user):
        self.client = client
        self.user = user

    def follow(self, target):
        """
        尝试让当前用户关注目标用户。
        成功时返回True，失败或者已关注时返回False。
        """
        # 构建名单键名
        following_zset = following_key(self.user)
        followers_zset = followers_key(target)
        # 获取当前时间戳
        current_time = time()
        tx = self.client.pipeline()
        # 将目标用户添加至当前用户的正在关注名单中
        tx.zadd(following_zset, {target: current_time})
        # 将当前用户添加至目标用户的关注者名单中
        tx.zadd(followers_zset, {self.user: current_time})
        result = tx.execute()
        return result[0] == result[1] == 1  # 判断执行结果

    def unfollow(self, target):
        """
        尝试取消当前用户对目标用户的关注。
        成功时返回True，取消失败或者尚未关注时返回False。
        """
        # 构建名单键名
        following_zset = following_key(self.user)
        followers_zset = followers_key(target)
        tx = self.client.pipeline()
        # 从当前用户的正在关注名单中移除目标用户
        tx.zrem(following_zset, target)
        # 从目标用户的关注者名单中移除当前用户
        tx.zrem(followers_zset, self.user)
        result = tx.execute()
        return result[0] == result[1] == 1  # 判断执行结果

    def is_following(self, target):
        """
        检测当前用户是否正在关注目标用户，是的话返回True，否则返回False。
        """
        following_zset = following_key(self.user)
        # 如果结果不为空，那么表示目标存在于正在关注名单中
        return self.client.zrank(following_zset, target) is not None

    def is_following_by(self, target):
        """
        检测当前用户是否正在被目标用户关注，是的话返回True，否则返回False。
        """
        followers_zset = followers_key(self.user)
        # 如果结果不为空，那么表示目标存在于关注者名单中
        return self.client.zrank(followers_zset, target) is not None

    def is_following_each_other(self, target):
        """
        检测当前用户和目标用户是否互相关注了对方，是的话返回True，否则返回False。
        """
        # 分别为当前用户和目标用户构建正在关注名单键
        user_following_zset = following_key(self.user)
        target_following_zset = following_key(target)
        # 分别从两个正在关注名单中查找对方是否存在
        tx = self.client.pipeline()
        tx.zrank(user_following_zset, target)
        tx.zrank(target_following_zset, self.user)
        result = tx.execute()
        # 若两个查找结果都非空，那么证明他们互相关注了彼此
        return result[0] is not None and result[1] is not None

    def following_count(self):
        """
        返回当前用户正在关注的人数。
        """
        following_zset = following_key(self.user)
        return self.client.zcard(following_zset)

    def followers_count(self):
        """
        返回当前用户的关注者人数。
        """
        followers_zset = followers_key(self.user)
        return self.client.zcard(followers_zset)
