import random

MAX_SEARCH_SIZE = 10
CACHE_TTL = 60

def make_neighbour_key(user):
    """
    附近用户名单缓存。
    """
    return "Location:{}:neighbours".format(user)

class Location:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def pin(self, user, long, lati):
        """
        记录用户所在的坐标。
        """
        self.client.geoadd(self.key, (long, lati, user))

    def locate(self, user):
        """
        获取用户的坐标。
        """
        return self.client.geopos(self.key, user)[0]

    def distance(self, user_x, user_y):
        """
        以公里为单位返回两个用户之间的直线距离。
        """
        return self.client.geodist(self.key, user_x, user_y, "km")

    def size(self):
        """
        获取已储存的用户位置数量。
        """
        return self.client.zcard(self.key)

    def search(self, user, radius, limit=MAX_SEARCH_SIZE):
        """
        以给定用户为圆心，搜索指定公里数范围内的其他用户。
        """
        result = self.client.geosearch(self.key, member=user, unit="km", radius=radius, count=limit)
        result.remove(user)  # 移除结果中包含的用户自身
        return result

    def random_neighbour(self, user, limit=MAX_SEARCH_SIZE):
        """
        随机返回给定用户1公里以内的另一名用户。
        """
        neighbours = self.search(user, 1, limit)
        if neighbours != []:
            return random.choice(neighbours)

    def cached_random_neighbour(self, user, limit=MAX_SEARCH_SIZE):
        """
        缓存版的random_neighbour()函数，结果最多每分钟刷新一次。
        """
        # 尝试直接返回已缓存的结果……
        cache_key = make_neighbour_key(user)
        cached_neighbour = self.client.zrandmember(cache_key)
        if cached_neighbour is not None:
            return cached_neighbour  # 返回缓存结果

        # 缓存不存在……
        # 那么更新缓存、设置过期时间，最后返回随机结果
        tx = self.client.pipeline()
        tx.geosearchstore(cache_key, self.key, member=user, unit="km", radius=1, count=limit)
        tx.zrem(cache_key, user)  # 从结果中移除用户自身
        tx.expire(cache_key, CACHE_TTL)  # 设置过期时间
        tx.zrandmember(cache_key)  # 从缓存中随机获取某个用户
        return tx.execute()[-1]  # 返回结果
