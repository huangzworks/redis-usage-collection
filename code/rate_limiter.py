def make_limiter_key(uid, action):
    """
    构建用于记录用户执行指定行为次数的计数器键。
    例子： RateLimiter:Peter:login
    """
    return "RateLimiter:{0}:{1}".format(uid, action)

class RateLimiter:

    def __init__(self, client, action, interval, maximum):
        """
        根据给定的行为、间隔和最大次数参数，创建相应行为的速率限制器实例。
        """
        self.client = client
        self.action = action
        self.interval = interval
        self.maximum = maximum

    def is_permitted(self, uid):
        """
        判断给定用户当前是否可以执行指定行为。
        """
        key = make_limiter_key(uid, self.action)
        # 更新计数器并在有需要时为其设置过期时间
        tx = self.client.pipeline()
        tx.incr(key)
        tx.expire(key, self.interval, nx=True)
        current_times, _ = tx.execute()
        # 根据计数器的当前值判断本次行为是否可以执行
        return current_times <= self.maximum

    def remaining(self, uid):
        """
        返回给定用户当前还可以执行指定行为的次数。
        """
        # 根据键获取计数器中储存的值
        key = make_limiter_key(uid, self.action)
        current_times = self.client.get(key)
        # 值为空则表示给定用户当前并未执行过指定行为
        if current_times is None:
            return self.maximum
        # 将值转换为数字，然后通过计算获取剩余的可执行次数
        current_times = int(current_times)
        if current_times > self.maximum:
            return 0
        else:
            return self.maximum - current_times

    def duration(self, uid):
        """
        计算距离给定用户允许再次执行指定行为需要多长时间，单位为秒。
        返回None则表示给定用户当前无需等待，仍然可以执行指定行为。
        """
        # 同时取出计数器的当前值和它的剩余生存时间
        key = make_limiter_key(uid, self.action)
        tx = self.client.pipeline()
        tx.get(key)
        tx.ttl(key)
        current_times, remaining_ttl = tx.execute()
        # 仅在计数器非空并且次数已超限的情况下计算需等待时长
        if current_times is not None:
            if int(current_times) >= self.maximum:
                return remaining_ttl

    def revoke(self, uid):
        """
        撤销对用户执行指定行为的限制。
        """
        key = make_limiter_key(uid, self.action)
        self.client.delete(key)
