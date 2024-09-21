TYPES = {"i8", "i16", "i32", "i64", "u8", "u16", "u32", "u63"}

class CompactCounter:

    def __init__(self, client, key, index, type="i64"):
        if type not in TYPES:
            raise("Counter type must be one of:{}.".format(type))
        self.client = client
        self.bfop = client.bitfield(key)
        self.type = type
        self.offset = "#{}".format(index)

    def increase(self, n=1):
        """
        将计数器的值加上指定的数字。
        """
        self.bfop.incrby(self.type, self.offset, n)
        return self.bfop.execute()[0]

    def decrease(self, n=1):
        """
        将计数器的值减去指定的数字。
        """
        self.bfop.incrby(self.type, self.offset, 0-n)
        return self.bfop.execute()[0]

    def get(self):
        """
        返回计数器的当前值。
        """
        self.bfop.get(self.type, self.offset)
        return self.bfop.execute()[0]

    def reset(self, n=0):
        """
        将计数器的值重置为指定的数字，并返回重置之前的旧值。
        """
        self.bfop.set(self.type, self.offset, n)
        return self.bfop.execute()[0]
