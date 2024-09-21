CACHE_TTL = 60

def make_target_key(target):
    """
    目标的标签集合，用于记录目标关联的所有标签。
    """
    return "Tag:target:{}".format(target)

def make_tag_key(tag):
    """
    标签的目标集合，用于记录带有该标签的所有目标。
    """
    return "Tag:tag:{}".format(tag)

def make_cached_targets_key(tags):
    """
    缓存多标签交集运算结果的集合。
    """
    # 使用sorted确保多个集合输入无论如何排列都会产生相同的缓存键
    return "Tag:cached_targets:{}".format(sorted(tags))

class Tag:

    def __init__(self, client):
        self.client = client

    def add(self, target, tags):
        """
        尝试为目标添加任意多个标签，并返回成功添加的标签数量作为结果。
        """
        tx = self.client.pipeline()
        # 将target添加至每个给定tag对应的集合中
        for tag_key in map(make_tag_key, tags):
            tx.sadd(tag_key, target)
        # 将所有给定tag添加至target对应的集合中
        target_key = make_target_key(target)
        tx.sadd(target_key, *tags)
        return tx.execute()[-1]  # 返回成功添加的标签数量

    def remove(self, target, tags):
        """
        尝试移除目标带有的任意多个标签，并返回成功移除的标签数量作为结果。
        """
        tx = self.client.pipeline()
        # 从每个给定tag对应的集合中移除target
        for tag_key in map(make_tag_key, tags):
            tx.srem(tag_key, target)
        # 从target对应的集合中移除所有给定tag
        target_key = make_target_key(target)
        tx.srem(target_key, *tags)
        return tx.execute()[-1]  # 返回成功移除的标签数量

    def get_tags_by_target(self, target):
        """
        获取目标的所有标签。
        """
        target_key = make_target_key(target)
        return self.client.smembers(target_key)

    def get_target_by_tags(self, tags):
        """
        根据给定的任意多个标签找出同时带有这些标签的目标。
        """
        # 找出所有给定tag对应的集合，然后对它们执行交集运算
        tag_keys = map(make_tag_key, tags)
        return self.client.sinter(*tag_keys)

    def get_cached_target_by_tags(self, tags):
        """
        缓存版本的get_target_by_tags()方法，结果最多每分钟刷新一次。
        """
        # 尝试直接从缓存中获取给定标签的交集结果……
        cache_key = make_cached_targets_key(tags)
        cached_targets = self.client.smembers(cache_key)
        if cached_targets != set():
            return cached_targets  # 返回缓存结果

        # 缓存不存在……
        # 那么先计算并储存交集，然后再设置过期时间，最后再返回交集元素
        tx = self.client.pipeline()
        tx.sinterstore(cache_key, map(make_tag_key, tags))
        tx.expire(cache_key, CACHE_TTL)
        tx.smembers(cache_key)
        return tx.execute()[-1]  # 执行事务并返回交集元素
