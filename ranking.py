def turn_tuple_into_dict(result_item):
    """
    将客户端返回的有序集合项从原来的元组(item, weight)转换为字典{item: weight}，
    并将权重的类型从浮点数转换为整数。
    """
    item, weight = result_item
    return {item: int(weight)}

class Ranking:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def set_weight(self, item, weight):
        """
        将排行榜中指定项的权重设置/更新为给定的值。
        如果项尚未存在，那么将其添加至排行榜中。
        返回True表示这是一次添加操作，返回False则表示这是一次更新操作。
        """
        return self.client.zadd(self.key, {item: weight}) == 1

    def get_weight(self, item):
        """
        返回指定项在排行榜中的权重，返回None则表示指定项不存在。
        """
        result = self.client.zscore(self.key, item)
        if result is not None: 
            return int(result)

    def update_weight(self, item, change):
        """
        根据change参数的值更新指定项的权重。
        传入正数表示执行加法，传入负数则表示执行减法。
        返回值为指定项在执行更新之后的权重。
        """
        return self.client.zincrby(self.key, change, item)

    def remove(self, item):
        """
        从排行榜中删除指定的项。
        删除成功返回True，返回False则表示指定项不存在并且删除失败。
        """
        return self.client.zrem(self.key, item) == 1
        
    def length(self):
        """
        返回排行榜的长度，也即是其包含的项数量。
        """
        return self.client.zcard(self.key)

    def top(self, N):
        """
        以降序方式返回排行榜前N个项及其权重。
        """
        start = 0
        end = N-1
        result = self.client.zrange(self.key, start, end, withscores=True, desc=True)
        return list(map(turn_tuple_into_dict, result))

    def bottom(self, N):
        """
        以升序方式返回排行榜后N个项及其权重。
        """
        start = 0
        end = N-1
        result = self.client.zrange(self.key, start, end, withscores=True)
        return list(map(turn_tuple_into_dict, result))
