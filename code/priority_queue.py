BLOCK_FOREVER = 0

def none_or_single_queue_item(result):
    """
    以{item: priority}形式返回result列表中包含的单个优先队列元素。
    若result为空列表则直接返回None。
    """
    if result == []:
        return None
    else:
        item, priority = result[0]
        return {item: priority}

class PriorityQueue:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def insert(self, item, priority):
        """
        将带有指定优先级的元素添加至队列，如果元素已存在那么更新它的优先级。
        """
        self.client.zadd(self.key, {item: priority}) 

    def remove(self, item):
        """
        尝试从队列中移除指定的元素。
        移除成功时返回True，返回False则表示由于元素不存在而导致移除失败。
        """
        return self.client.zrem(self.key, item) == 1

    def min(self):
        """
        获取队列中优先级最低的元素及其优先级，如果队列为空则返回None。
        """
        result = self.client.zrange(self.key, 0, 0, withscores=True)
        return none_or_single_queue_item(result)

    def max(self):
        """
        获取队列中优先级最高的元素及其优先级，如果队列为空则返回None。
        """
        result = self.client.zrange(self.key, -1, -1, withscores=True)
        return none_or_single_queue_item(result)

    def pop_min(self):
        """
        弹出并返回队列中优先级最低的元素及其优先级，如果队列为空则返回None。
        """
        result = self.client.zpopmin(self.key)
        return none_or_single_queue_item(result)

    def pop_max(self):
        """
        弹出并返回队列中优先级最高的元素及其优先级，如果队列为空则返回None。
        """
        result = self.client.zpopmax(self.key)
        return none_or_single_queue_item(result)

    def length(self):
        """
        返回队列的长度，也即是队列包含的元素数量。
        """
        return self.client.zcard(self.key)

    def blocking_pop_min(self, timeout=BLOCK_FOREVER):
        """
        尝试从队列中弹出优先级最低的元素及其优先级，若队列为空则阻塞。
        可选参数timeout用于指定最大阻塞秒数，默认将一直阻塞到有元素可弹出为止。
        """
        result = self.client.bzpopmin(self.key, timeout)
        if result is not None:
            zset_name, item, priority = result
            return {item: priority}

    def blocking_pop_max(self, timeout=BLOCK_FOREVER):
        """
        尝试从队列中弹出优先级最高的元素及其优先级，若队列为空则阻塞。
        可选参数timeout用于指定最大阻塞秒数，默认将一直阻塞到有元素可弹出为止。
        """
        result = self.client.bzpopmax(self.key, timeout)
        if result is not None:
            zset_name, item, priority = result
            return {item: priority}
