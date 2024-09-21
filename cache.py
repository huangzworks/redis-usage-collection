class Cache:

    def __init__(self, client):
        self.client = client

    def set(self, name, content, ttl=None):
        """
        为指定名字的缓存设置内容。
        可选的ttl参数用于设置缓存的生存时间。
        """
        if ttl is None:
            self.client.set(name, content)
        else:
            self.client.set(name, content, ex=ttl)

    def get(self, name):
        """
        尝试获取指定名字的缓存内容，若缓存不存在则返回None。
        """
        return self.client.get(name)
