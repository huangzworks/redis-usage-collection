from url_shorty import UrlShorty

URL_MAPPING_CACHE = "UrlShorty:mapping_cache"

class UrlShortyWithCache(UrlShorty):

    def shorten(self, url):
        """
        为给定的网址创建并记录一个对应的短网址ID，然后将其返回。
        如果该网址之前已经创建过相应的短网址ID，那么直接返回之前创建的ID。
        """
        # 尝试在缓存中寻找与原网址对应的短网址ID
        # 如果找到就直接返回已有的短网址ID，无需重新生成
        cached_short_id = self.client.hget(URL_MAPPING_CACHE, url)
        if cached_short_id is not None:
            return cached_short_id

        # 原网址尚未创建过短网址ID……
        # 调用父类的shorten()方法，为原网址创建短网址ID
        short_id = super().shorten(url)
        # 在缓存映射中关联原网址和短网址ID
        self.client.hset(URL_MAPPING_CACHE, url, short_id)
        # 返回短网址ID
        return short_id
