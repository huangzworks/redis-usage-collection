def calc_offset(row, col, M, N):
    if row >= M:
        raise ValueError("Row must be less than {}.".format(M))
    if col >= N:
        raise ValueError("Col must be less than {}.".format(N))
    return "#{}".format(row*N+col)

class Matrix:

    def __init__(self, client, key, M, N, type="i64"):
        self.client = client
        self.bfop = client.bitfield(key)
        self.M = M
        self.N = N
        self.type = type

    def set(self, row, col, value):
        offset = calc_offset(row, col, self.M, self.N)
        self.bfop.set(self.type, offset, value)
        return self.bfop.execute()[0]

    def get(self, row, col):
        offset = calc_offset(row, col, self.M, self.N)
        self.bfop.get(self.type, offset)
        return self.bfop.execute()[0]

    def get_row(self, row):
        # 将获取整个行所需的全部GET子命令放到一条BITFIELD命令里面执行
        for col in range(self.N):
            offset = calc_offset(row, col, self.M, self.N)
            self.bfop.get(self.type, offset)
        return self.bfop.execute()

    def get_all(self):
        # 将获取整个矩阵所需的全部GET子命令放到一条BITFIELD命令里面执行
        for i in range(self.M*self.N):
            offset = "#{}".format(i)
            self.bfop.get(self.type, offset)
        all_values = self.bfop.execute()
        # 计算出矩阵每一行在all_values列表中的起始索引和结束索引，
        # 然后将各行分别推入至matrix列表中，形成二维矩阵
        matrix = []
        for i in range(self.M):
            start = i*self.N
            end = (i+1)*self.N
            matrix.append(all_values[start:end])
        return matrix
        # 在Python 3.12或以上版本中，上述for循环可以用以下语句来代替：
        # for row in batched(all_values, self.N):
        #     matrix.append(row)
        # 此外，程序还需要在源码开头加上：
        # from itertools import batched
