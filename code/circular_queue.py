NON_BLOCK = -1

class CircularQueue:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def insert(self, *items):
        """
        将给定的一个或多个元素插入至队列末尾，然后返回队列的长度作为结果。
        """
        return self.client.rpush(self.key, *items)

    def remove(self, item, count=0):
        """
        从队列中移除指定元素，然后返回被移除元素的数量作为结果。
        可选的count参数用于指定具体的移除方式：
        - 值为0表示移除队列中出现的所有指定元素，这是默认行为；
        - 值大于0表示移除队列从开头到末尾最先遇到的前count个指定元素；
        - 值小于0表示移除队列从末尾到开头最先遇到的前abs(count)个指定元素。
        """
        return self.client.lrem(self.key, count, item)

    def rotate(self, block_time=NON_BLOCK):
        """
        将队列开头的元素移动至队列末尾，然后返回被移动的元素。
        可选的block_time参数用于指定是否使用阻塞功能：
        - 值为0表示一直阻塞以等待值；
        - 值为大于0的N表示最多阻塞N秒钟以等待值；
        默认情况下不使用该参数则代表不启用阻塞功能。
        """
        if block_time == NON_BLOCK:
            return self.client.lmove(self.key, self.key)
        else:
            return self.client.blmove(self.key, self.key, block_time)

    def front(self):
        """
        获取队列第一个元素，如果队列为空则返回None。
        """
        return self.client.lindex(self.key, 0)

    def rear(self):
        """
        获取队列最后一个元素，如果队列为空则返回None。
        """
        return self.client.lindex(self.key, -1)

    def length(self):
        """
        返回队列长度，也即是队列包含的元素数量。
        """
        return self.client.llen(self.key)
