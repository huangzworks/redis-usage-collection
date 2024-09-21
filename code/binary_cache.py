from cache import Cache

class BinaryCache:

    def __init__(self, client):
        self.cache = Cache(client)

    def set(self, name, path, ttl=None):
        """
        根据给定的名字和文件路径，缓存指定的二进制文件数据。
        可选的ttl参数用于设置缓存的生存时间。
        """
        # 以二进制方式打开文件，并读取文件中的数据
        file = open(path, "rb")
        data = file.read()
        file.close()
        # 缓存二进制数据
        self.cache.set(name, data, ttl)

    def get(self, name):
        """
        尝试获取指定名字的缓存内容，若缓存不存在则返回None。
        """
        return self.cache.get(name)
