from redis import WatchError

class IdentityLock:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def acquire(self, password):
        """
        尝试获取一个带有密码保护功能的锁，
        成功时返回True，失败时则返回False。
        password参数用于设置上锁/解锁密码。
        """
        return self.client.set(self.key, password, nx=True) is True

    def release(self, password):
        """
        根据给定的密码，尝试释放锁。
        锁存在并且密码正确时返回True，
        返回False则表示密码不正确或者锁已不存在。
        """
        tx = self.client.pipeline()
        try:
            # 监视锁键以防它发生变化
            tx.watch(self.key)
            # 获取锁键存储的密码
            lock_password = tx.get(self.key)
            # 比对密码
            if lock_password == password:
                # 情况1：密码正确，尝试解锁
                tx.multi()
                tx.delete(self.key)
                return tx.execute()[0]==1  # 返回删除结果
            else:
                # 情况2：密码不正确
                tx.unwatch()
        except WatchError:
            # 尝试解锁时发现键已变化
            pass
        finally:
            # 确保连接正确回归连接池，redis-py的要求
            tx.reset()
        # 密码不正确或者尝试解锁时失败
        return False
