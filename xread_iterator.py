DEFAULT_COUNT = 10
NON_BLOCK = None
START_OF_STREAM = 0

def tuple_to_dict(tpl):
    """
    将流返回的元素从元组(id, msg)转换为字典{"id":id, "msg":msg}。
    """
    return {"id": tpl[0], "msg": tpl[1]}

class StreamIterator:

    def __init__(self, client, key, cursor=START_OF_STREAM):
        """
        初始化流迭代器，参数key用于指定被迭代的流。
        可选的cursor参数用于指定迭代的游标，默认为流的开头。
        """
        self.client = client
        self.key = key
        self._cursor = cursor

    def next(self,count=DEFAULT_COUNT,block=NON_BLOCK):
        """
        迭代流元素并以列表形式返回它们，其中每个元素的格式为{"id":id, "msg":msg}。
        可选的count参数用于指定每次迭代能够返回的最大元素数量，默认为10。
        可选的block参数用于指定迭代时阻塞的最长时限，单位为毫秒，默认非阻塞。
        """
        ret = self.client.xread({self.key: self._cursor}, count=count, block=block)
        if ret == []:
            return []
        else:
            messages = ret[0][1]
            self._cursor = messages[-1][0] # 本次迭代最后一条消息的ID
            return list(map(tuple_to_dict, messages))

    def rewind(self, cursor=START_OF_STREAM):
        """
        将游标重置至可选参数cursor指定的位置，若省略该参数则默认重置至流的开头。
        """
        self._cursor = cursor
