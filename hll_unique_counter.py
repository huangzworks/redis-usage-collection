class HllUniqueCounter:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def include(self, item):
        """
        尝试对给定元素进行计数。
        如果该元素之前没有被计数过，那么返回True，否则返回False。
        """
        return self.client.pfadd(self.key, item) == 1

    def exclude(self, item):
        """
        尝试将被计数的元素移出计数器。
        移除成功返回True，因元素尚未被计数而导致移除失败则返回False。
        """
        raise NotImplementedError

    def count(self):
        """
        返回计数器当前已计数的元素数量。
        如果计数器为空，那么返回0作为结果。
        """
        return self.client.pfcount(self.key)

class HllUniqueCounterMerger:

    def __init__(self, client, result_key):
        self.client = client
        self.result_key = result_key

    def merge(self, *keys):
        return self.client.pfmerge(self.result_key, *keys)
