from message_queue import MessageQueue, DEFAULT_COUNT, BLOCK_FOREVER

def make_chat_key(broadcaster):
    """
    根据给定的主播ID，构建出相应的消息队列键，用于存储直播间发出的弹幕。
    例子："Chat:Peter"、"Chat:10086"等。
    """
    return "Chat:{}".format(broadcaster)

class Chat:

    def __init__(self, client, broadcaster):
        """
        根据给定的主播ID，为其构建存储直播间弹幕的消息队列。
        """
        self.client = client
        self.broadcaster = broadcaster
        self.key = make_chat_key(broadcaster)
        # 因为消息队列默认从队列开头开始返回元素，所以这里需要
        # 传入特殊值"$"作为ID，让队列只返回阻塞之后出现的新消息
        self.mq = MessageQueue(self.client, self.key, "$")

    def send(self, uid, content, donate=0):
        """
        根据给定的用户ID和内容，向直播间发送一条弹幕。
        如果donate参数的值不为0，那么说明这是一条付费弹幕（super chat）。
        """
        if donate == 0:
            msg = {"uid": uid, "content": content}
        else:
            msg = {"uid": uid, "content": content, "donate": donate}
        # 将弹幕发送至消息队列中
        return self.mq.send(msg)

    def receive(self, count=DEFAULT_COUNT):
        """
        从直播间接收并返回最多count条弹幕，默认为10条。
        如果上次调用之后还有未接收的弹幕存在，那么先接收已有的弹幕，再接收新出现的弹幕。
        """
        # 尝试从消息队列中取出弹幕
        # 若队列为空就一直阻塞直到有弹幕可弹出为止
        return self.mq.receive(count, BLOCK_FOREVER)

    def show(self):
        """
        简易的弹幕打印器。
        """
        while True:
            # 一直接收弹幕
            for item in self.receive():
                # 丢弃消息ID，只获取消息本身
                msg = item["msg"]
                if "donate" not in msg:
                    # 打印普通弹幕
                    print("{0}: {1}".format(msg["uid"], msg["content"]))
                else:
                    # 打印付费弹幕
                    print("+"*10 + "SUPER CHAT" + "+"*10)
                    print("{0}: {1}".format(msg["uid"], msg["content"]))
                    print("Donate: {}".format(msg["donate"]))
                    print("-"*10 + "SUPER CHAT" + "-"*10)
