class HashCounter:

    def __init__(self, client, key, name):
        """
        创建一个哈希键计数器对象。
        其中key参数用于指定包含多个计数器的哈希键的键名，
        而name参数则用于指定具体的计数器在该键中的名字。
        """
        self.client = client
        self.key = key
        self.name = name

    def increase(self, n=1):
        """
        将计数器的值加上指定的数字。
        """
        return self.client.hincrby(self.key, self.name, n)

    def decrease(self, n=1):
        """
        将计数器的值减去指定的数字。
        """
        return self.client.hincrby(self.key, self.name, 0-n)

    def get(self):
        """
        返回计数器的当前值。
        """
        value = self.client.hget(self.key, self.name)
        if value is None:
            return 0
        else:
            return int(value)

    def reset(self, n=0):
        """
        将计数器的值重置为参数n指定的数字，并返回计数器在重置之前的旧值。
        参数n是可选的，若省略则默认将计数器重置为0。
        """
        tx = self.client.pipeline()
        tx.hget(self.key, self.name)  # 获取旧值
        tx.hset(self.key, self.name, n)  # 设置新值
        old_value, _ = tx.execute()
        if old_value is None:
            return 0
        else:
            return int(old_value)
