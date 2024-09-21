from math import ceil  # 向下取整函数

DEFAULT_SIZE = 10  # 默认每页返回10个元素

class Timeline:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def add(self, *items):
        """
        将给定的一个或多个项添加到时间线中，其中每个项由一个元素和一个时间戳组成。
        成功时返回时间线当前包含的项数量作为结果。
        """
        # 为了跟分页程序同名方法的返回值保持一致
        # 此方法会多执行一个ZCARD命令以获取时间线最新的大小
        tx = self.client.pipeline()
        tx.zadd(self.key, *items)  # 添加元素
        tx.zcard(self.key)    # 获取时间线大小
        return tx.execute()[1] # 返回时间线大小

    def get(self, page, size=DEFAULT_SIZE):
        """
        从指定分页中取出指定数量的元素（不包含时间戳）。
        """
        # 根据给定的页数和元素数量计算出索引范围
        start = (page-1)*size
        end = page*size-1
        # 根据索引从有序集合中获取元素
        return self.client.zrange(self.key, start, end, desc=True)

    def get_with_time(self, page, size=DEFAULT_SIZE):
        """
        从指定分页中取出指定数量的项（包括元素和时间戳）。
        """
        # 根据给定的页数和元素数量计算出索引范围
        start = (page-1)*size
        end = page*size-1
        # 根据索引从有序集合中获取元素及其分值
        result = self.client.zrange(self.key, start, end, desc=True, withscores=True)
        # 将结果中的每个项从元组(elem, time)转换为字典{elem: time}
        return list(map(lambda tuple: {tuple[0]: tuple[1]}, result))

    def get_by_time_range(self, min, max, page, size=DEFAULT_SIZE):
        """
        对位于指定时间戳范围内的项进行分页。
        """
        # 计算分页的起始偏移量
        offset = (page-1)*size
        # 获取指定时间戳范围内的元素，然后再对这些元素实施分页
        result = self.client.zrange(self.key, max, min, 
                                    byscore=True, desc=True, withscores=True,
                                    offset=offset, num=size)
        # 将结果中的每个项从元组(elem, time)转换为字典{elem: time}
        return list(map(lambda tuple: {tuple[0]: tuple[1]}, result))

    def length(self):
        """
        返回时间线包含的元素总数量。
        """
        return self.client.zcard(self.key)

    def number(self, size=DEFAULT_SIZE):
        """
        返回在获取指定数量的元素时，时间线包含的页数量。
        如果时间线为空则返回0。
        """
        return ceil(self.length()/size)
