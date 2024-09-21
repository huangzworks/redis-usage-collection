DEFAULT_COUNT = 10

from db_iterator import DbIterator

class DbSampler:

    def __init__(self, client, count=DEFAULT_COUNT):
        self.client = client
        self.count = count
        self.total = 0
        self.record = dict()
        self.iterator = DbIterator(self.client, count)

    def sample(self):
        """
        对数据库键进行采样。
        """
        keys = self.iterator.next()
        # 如果迭代已完成，那么直接返回
        if keys is None: 
            return None

        # 根据迭代结果更新采样记录
        tx = self.client.pipeline()
        for key in keys:
            tx.type(key)
        types = tx.execute()
        for type in types:
            # 初始化键类型计数器
            if type not in self.record:
                self.record[type] = 0
            # 更新键类型计数器的值
            self.record[type] += 1
        # 更新总采样键数量
        self.total += len(keys)
        # 返回本次被采样的键数量
        return len(keys)

    def show_stats(self):
        """
        打印目前的采样结果。
        """
        print("Total {} key(s) sampled.".format(self.total))
        print("-"*25)
        for type in self.record:
            title = type.capitalize()
            number = self.record[type]
            percent = int(round(number/self.total,2)*100)
            print("{0} key(s): {1}, ~{2}% of total.".format(title, number, percent))
