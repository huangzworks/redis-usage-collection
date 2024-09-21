from xread_iterator import StreamIterator, START_OF_STREAM

NON_BLOCK = None
BLOCK_FOREVER = 0

DEFAULT_COUNT = 10

START_OF_MQ = START_OF_STREAM

class MessageQueue:

    def __init__(self, client, key, cursor=START_OF_MQ):
        """
        根据给定的键，创建与之对应的消息队列。
        消息队列的起始访问位置可以通过可选参数cursor指定。
        默认情况下，cursor指向消息队列的最开头。
        """
        self.client = client
        self.key = key
        self._iterator = StreamIterator(self.client, self.key, cursor)

    def send(self, message):
        """
        接受一个键值对形式的消息，并将其放入队列。
        完成之后返回消息在队列中的ID作为结果。
        """
        return self.client.xadd(self.key, message)

    def receive(self, count=DEFAULT_COUNT, timeout=NON_BLOCK):
        """
        根据消息的入队顺序，访问队列中的消息。
        可选的count参数用于指定每次访问最多能够获取多少条消息，默认为10。
        可选的timeout参数用于指定方法在未发现消息时是否阻塞，它的值可以是：
        - NON_BLOCK，不阻塞直接返回，这是默认值；
        - BLOCK_FOREVER，一直阻塞直到有消息可读为止；
        - 一个大于零的整数，用于代表阻塞的最大毫秒数
        """
        return self._iterator.next(count, timeout)

    def get(self, message_id):
        """
        获取指定ID对应的消息。
        """
        ret = self.client.xrange(self.key, message_id, message_id)
        if ret != []:
            return ret[0][1]

    def length(self):
        """
        返回整个消息队列目前包含的消息总数量。
        """
        return self.client.xlen(self.key)
