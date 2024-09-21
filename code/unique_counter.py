class UniqueCounter:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def include(self, item):
        """
        尝试对给定元素进行计数。
        如果该元素之前没有被计数过，那么返回True，否则返回False。
        """
        return self.client.sadd(self.key, item) == 1

    def exclude(self, item):
        """
        尝试将被计数的元素移出计数器。
        移除成功返回True，因元素尚未被计数而导致移除失败则返回False。
        """
        return self.client.srem(self.key, item) == 1

    def count(self):
        """
        返回计数器当前已计数的元素数量。
        如果计数器为空，那么返回0作为结果。
        """
        return self.client.scard(self.key)

    @staticmethod
    def inter(client, *count_keys):
        """
        静态方法，对多个计数器执行交集计算并返回结果的元素数量。
        """
        return client.sintercard(len(count_keys), count_keys)

    @staticmethod
    def union(client, *count_keys):
        """
        静态方法，对多个计数器执行并集计算并返回结果的元素数量。
        """
        union_items = client.sunion(*count_keys)
        return len(union_items)

    @staticmethod
    def diff(client, counter_x, counter_y):
        """
        静态方法，对两个计数器执行差集计算并返回结果的元素数量。
        """
        diff_items = client.sdiff(counter_x, counter_y)
        return len(diff_items)
