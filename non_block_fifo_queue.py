class FifoQueue:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def enqueue(self, *items):
        """
        以先进先出顺序将给定的一个或多个元素推入队列。
        执行之后返回队列的当前长度作为结果。
        """
        return self.client.rpush(self.key, *items)

    def dequeue(self):
        """
        以先进先出顺序弹出队列中的一个元素。
        如果队列为空则返回None。
        """
        return self.client.lpop(self.key)

    def length(self):
        """
        返回队列的长度。
        """
        return self.client.llen(self.key)
