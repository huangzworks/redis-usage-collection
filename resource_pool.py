from redis import WatchError

def available_key(pool_name):
    return "ResourcePool:{0}:available".format(pool_name)

def occupied_key(pool_name):
    return "ResourcePool:{0}:occupied".format(pool_name)

class ResourcePool:

    def __init__(self, client, pool_name):
        """
        基于给定的资源池名字创建出相应的资源池对象。
        """
        self.client = client
        self.available_set = available_key(pool_name)
        self.occupied_set = occupied_key(pool_name)

    def associate(self, resource):
        """
        将指定资源关联到资源池中。
        返回True表示关联成功，返回False表示资源已存在，关联失败。
        返回None则表示关联过程中操作失败，需要重新尝试。
        """
        tx = self.client.pipeline()
        try:
            # 监视两个集合，观察它们是否在操作中途变化
            tx.watch(self.available_set, self.occupied_set)
            # 检查给定资源是否存在于两个集合之中
            if tx.sismember(self.available_set, resource) or \
               tx.sismember(self.occupied_set, resource):
                # 资源已存在，放弃添加
                tx.unwatch()
                return False
            else:
                # 资源未存在，尝试添加
                tx.multi()
                tx.sadd(self.available_set, resource)
                return tx.execute()[0]==1  # 添加是否成功？
        except WatchError:
            # 操作过程中集合键发生了变化，需要重试
            pass
        finally:
            tx.reset()

    def disassociate(self, resource):
        """
        将指定资源从资源池中移除。
        移除成功返回True，因资源不存在而导致移除失败返回False。
        """
        # 使用事务同时向两个集合发出SREM命令
        # 当资源存在于池中时，其中一个集合将返回1作为SREM命令的结果
        tx = self.client.pipeline()
        tx.srem(self.available_set, resource)
        tx.srem(self.occupied_set, resource)
        ret1, ret2 = tx.execute()
        return ret1==1 or ret2==1

    def acquire(self):
        """
        尝试从资源池中获取并返回可用的资源。
        返回None表示资源池为空，或者获取操作过程中失败。
        """
        tx = self.client.pipeline()
        try:
            # 监视两个集合，观察它们是否在操作中途变化
            tx.watch(self.available_set, self.occupied_set)
            # 尝试从可用集合中随机获取一项资源
            resource = tx.srandmember(self.available_set)
            if resource is not None:
                # 将资源从可用集合移动到已占用集合
                tx.multi()
                tx.smove(self.available_set, self.occupied_set, resource)
                smove_ret = tx.execute()[0]
                if smove_ret == 1:
                    return resource
        except WatchError:
            # 操作过程中集合键发生了变化，需要重试
            pass
        finally:
            tx.reset()

    def release(self, resource):
        """
        将给定的一项已被占用的资源回归至资源池。
        回归成功时返回True，因资源不属于资源池而导致回归失败时返回False。
        """
        # 将资源从已占用集合移动至可用集合
        return self.client.smove(self.occupied_set, self.available_set, resource)

    def available_count(self):
        """
        返回资源池中目前可用的资源数量。
        """
        return self.client.scard(self.available_set)

    def occupied_count(self):
        """
        返回资源池中目前已被占用的资源数量。
        """
        return self.client.scard(self.occupied_set)

    def total_count(self):
        """
        返回资源池中（包括可用和已占用）资源的总数量。
        """
        tx = self.client.pipeline()
        tx.scard(self.available_set)
        tx.scard(self.occupied_set)
        available_count, occupied_count = tx.execute()
        return available_count + occupied_count

    def is_available(self, resource):
        """
        检查指定资源是否可用，是的话返回True，否则返回False。
        """
        return self.client.sismember(self.available_set, resource)==1

    def is_occupied(self, resource):
        """
        检查给定资源是否已被占用，是的话返回True，否则返回False。
        """
        return self.client.sismember(self.occupied_set, resource)==1

    def has(self, resource):
        """
        检查给定资源是否存在于资源池（包括可用或已占用）。
        """
        tx = self.client.pipeline()
        tx.sismember(self.available_set, resource)
        tx.sismember(self.occupied_set, resource)
        is_available, is_occupied = tx.execute()
        return is_available or is_occupied
