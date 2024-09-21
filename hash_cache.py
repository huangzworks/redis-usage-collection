class HashCache:

    def __init__(self, client):
        self.client = client

    def set(self, name, content, ttl=None):
        """
        为指定名字的缓存设置内容。
        可选的ttl参数用于设置缓存的生存时间。
        """
        if ttl is None:
            self.client.hset(name, mapping=content)
        else:
            tx = self.client.pipeline()
            tx.hset(name, mapping=content)
            tx.expire(name, ttl)
            tx.execute()

    def get(self, name):
        """
        尝试获取指定名字的缓存内容，若缓存不存在则返回None。
        """
        result = self.client.hgetall(name)
        if result != {}:
            return result
