class Counter:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def increase(self, n=1):
        """
        将计数器的值加上指定的数字。
        """
        return self.client.incr(self.key, n)

    def decrease(self, n=1):
        """
        将计数器的值减去指定的数字。
        """
        return self.client.decr(self.key, n)

    def get(self):
        """
        返回计数器的当前值。
        """
        value = self.client.get(self.key)
        return 0 if value is None else int(value)

    def reset(self, n=0):
        """
        将计数器的值重置为参数n指定的数字，并返回计数器在重置之前的旧值。
        参数n是可选的，若省略则默认将计数器重置为0。
        """
        value = self.client.set(self.key, n, get=True)
        return 0 if value is None else int(value)
