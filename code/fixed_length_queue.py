from fifo_queue import FifoQueue

class FixedLengthQueue(FifoQueue):

    def __init__(self, client, key, max_length):
        """
        初始化一个带有最大长度限制的先进先出队列。
        其中max_length参数用于指定队列的最大长度。
        """
        self.client = client
        self.key = key
        self.max_length = max_length

    def enqueue(self, *items):
        """
        尝试将给定的一个或多个新元素推入至队列末尾。
        当队列的长度到达最大限制之后，超过限制的元素将被丢弃。
        这个方法将返回成功推入且被最终保留的元素数量作为结果。
        """
        # 计算合法元素所处的列表索引区间
        start = 0
        end = self.max_length-1

        # 执行推入操作，并截断超过长度限制的部分
        tx = self.client.pipeline()
        tx.rpush(self.key, *items)
        tx.ltrim(self.key, start, end)
        current_length, _ = tx.execute()

        # 根据列表添加新元素之后的长度来计算有多少个新元素会被保留
        if current_length < self.max_length:
            # 未引起截断操作，所有新元素均被保留
            return len(items)
        else:
            # 列表过长，引发截断
            # 先计算出被截断的元素数量，再计算出被保留的元素数量
            trim_size = current_length - self.max_length
            return len(items) - trim_size
