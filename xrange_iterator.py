DEFAULT_COUNT = 10

START_OF_STREAM = "-"
END_OF_STREAM = "+"

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

    def next(self,count=DEFAULT_COUNT):
        """
        迭代流元素并以列表形式返回它们，其中每个元素的格式为{"id":id, "msg":msg}。
        可选的count参数用于指定每次迭代能够返回的最大元素数量，默认为10。
        """
        messages = self.client.xrange(self.key, self._cursor, END_OF_STREAM, count=count)
        if messages == []:
            return []
        else:
            # 获取本次迭代最后一条消息的ID
            # 并通过给它加上前缀"("来保证下次迭代时新消息的ID必定大于它
            self._cursor = "(" + messages[-1][0]
            return list(map(tuple_to_dict, messages))

    def rewind(self, cursor=START_OF_STREAM):
        """
        将游标重置至可选参数cursor指定的位置，若省略该参数则默认重置至流的开头。
        """
        self._cursor = cursor
