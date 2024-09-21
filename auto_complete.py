DEFAULT_WEIGHT = 1.0
DEFAULT_NUM = 10
DEFAULT_TTL = 300

def make_ac_key(subject, segment):
    """
    基于给定的主题和输入片段，构建保存建议项的建议表。
    """
    return "AutoComplete:{0}:{1}".format(subject, segment)

def create_segments(content):
    """
    根据输入的字符串为其创建片段。
    例子：对于输入"abc"，将创建输出["a", "ab", "abc"]
    """
    return [content[:i] for i in range(1, len(content)+1)]

class AutoComplete:

    def __init__(self, client, subject):
        self.client = client
        self.subject = subject

    def feed(self, content, weight=DEFAULT_WEIGHT):
        """
        根据输入内容构建自动补全建议表。
        可选的weight参数用于指定需要增加的输入权重。
        """
        tx = self.client.pipeline()
        # 将输入分解为片段，然后对其相应的建议表执行操作
        for seg in create_segments(content):
            # 构建建议表键名
            key = make_ac_key(self.subject, seg)
            # 更新输入在该表中的权重
            tx.zincrby(key, weight, content)
        tx.execute()

    def hint(self, segment, num=DEFAULT_NUM):
        """
        根据给定的片段返回指定数量的补全建议，各个建议项之间按权重从高到低排列。
        """
        # 构建建议表键名
        key = make_ac_key(self.subject, segment)
        # 获取补全建议
        return self.client.zrange(key, 0, num-1, desc=True)

    def set(self, content, weight):
        """
        为输入内容设置指定的权重。
        """
        tx = self.client.pipeline()
        for seg in create_segments(content):
            key = make_ac_key(self.subject, seg)
            # 直接设置权重
            tx.zadd(key, {content: weight})
        tx.execute()

    def feedex(self, content, weight=DEFAULT_WEIGHT, ttl=DEFAULT_TTL):
        """
        根据输入内容构建自动补全建议表。
        可选的weight参数用于指定需要增加的输入权重。
        可选的ttl参数用于指定建议表的生存时间，默认为300秒（5分钟）。
        """
        tx = self.client.pipeline()
        for seg in create_segments(content):
            key = make_ac_key(self.subject, seg)
            tx.zincrby(key, weight, content)
            # 为建议表设置生存时间
            tx.expire(key, ttl)
        tx.execute()
