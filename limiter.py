class Limiter:

    def __init__(self, client, key, timeout, maximum):
        self.client = client
        self.key = key
        self.timeout = timeout
        self.maximum = maximum

    def is_valid(self):
        """
        判断是否可以继续执行指定操作，可以执行返回True，否则返回False。
        """
        # 使用事务保证安全性
        transaction = self.client.pipeline()
        transaction.incr(self.key)
        transaction.expire(self.key, self.timeout, nx=True)
        result = transaction.execute()
        current = result[0]
        return current <= self.maximum

    def remaining_time(self):
        """
        返回还可以执行指定操作的次数。
        """
        value = self.client.get(self.key)
        if value is None:
            return None

        current = int(value)
        if current > self.maximum:
            return 0
        else:
            return self.maximum - current
