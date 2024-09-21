DEFAULT_COUNT = 10

class DbIterator:

    def __init__(self, client, count=DEFAULT_COUNT):
        """
        初始化数据库迭代器。
        可选的count参数用于建议迭代器每次返回的键数量。
        """
        self.client = client
        self.count = count
        self._cursor = 0

    def next(self):
        """
        迭代数据库，并以列表形式返回本次被迭代的键。
        """
        # 迭代已结束，直接返回None作为标志
        if self._cursor is None: return

        new_cursor, keys = self.client.scan(self._cursor, count=self.count)
        # 通过命令返回的新游标来判断迭代是否已结束
        if new_cursor == 0:
            # 迭代已结束
            self._cursor = None
        else:
            # 迭代未结束，更新游标
            self._cursor = new_cursor

        # 返回被迭代的键
        return keys

    def rewind(self):
        """
        重置迭代游标以便从头开始对数据库进行迭代。
        """
        self._cursor = 0
