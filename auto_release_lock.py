VALUE_OF_LOCK = ""

class AutoReleaseLock:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def acquire(self, timeout, unit="sec"):
        """
        尝试获取一个能够在指定时长之后自动释放的锁。
        timeout参数用于设置锁的最大加锁时长。
        可选的unit参数则用于设置时长的单位，
        它的值可以是代表秒的'sec'或是代表毫秒的'ms'，默认为'sec'。
        """
        if unit == "sec":
            return self.client.set(self.key, VALUE_OF_LOCK, nx=True, ex=timeout) is True
        elif unit == "ms":
            return self.client.set(self.key, VALUE_OF_LOCK, nx=True, px=timeout) is True
        else:
            raise ValueError("Unit must be 'sec' or 'ms'!")

    def release(self):
        """
        尝试释放锁，成功时返回True，失败时则返回False。
        """
        return self.client.delete(self.key) == 1
