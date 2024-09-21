def make_row_key(matrix_id, row):
    return "matrix:{0}:{1}".format(id, row)

class BitmapMatrix:

    def __init__(self, client, matrix_id, M, N, type="i64"):
        """
        创建一个使用ID标识，由指定数量的行和列组成的矩阵。
        可选的type参数用于指定矩阵元素的类型。
        """
        self.client = client
        self.matrix_id = matrix_id
        self.M = M
        self.N = N
        self.type = type

    def init(self, elements=None):
        """
        根据给定数据对矩阵进行初始化。
        如果没有给定数据，那么将矩阵的所有元素初始化为0。
        """
        # 这个函数只能在矩阵不存在的情况下执行
        key = make_row_key(self.matrix_id, 0)
        assert(self.client.exists(key)==0)

        # 如果未给定初始化矩阵，那么创建一个全为0的矩阵
        if elements is None:
            # 位图的所有位置默认都被设置为0，无需另行设置
            return 

        # 检查矩阵的行数是否正确
        if len(elements) != self.M:
            raise ValueError("Incorrect row number, it should be {}.".format(self.M))
        # 检查矩阵中每个行的列数是否正确
        for row in range(self.M):
            if len(elements[row]) != self.N:
                raise ValueError("Incorrect col number, it should be {}.".format(self.N))

        # 遍历矩阵的每个行
        for row in range(self.M):
            key = make_row_key(self.matrix_id, row)
            bfop = self.client.bitfield(key)
            # 对行中的每一列进行设置
            for col in range(self.N):
                bfop.set(self.type, "#{}".format(col), elements[row][col])
            bfop.execute()

    def set(self, row, col, value):
        """
        将指定行列上的元素设置为给定的值。
        """
        key = make_row_key(self.matrix_id, row)
        bfop = self.client.bitfield(key)
        bfop.set(self.type, "#{}".format(col), value)
        bfop.execute()

    def get(self, row, col):
        """
        获取指定行列的值。
        """
        key = make_row_key(self.matrix_id, row)
        bfop = self.client.bitfield(key)
        bfop.get(self.type, "#{}".format(col))
        return bfop.execute()[0]

    def get_row(self, row):
        """
        获取指定行上所有列的值。
        """
        key = make_row_key(self.matrix_id, row)
        bfop = self.client.bitfield(key)
        # 遍历该行的所有列，获取它们的值
        for col in range(self.N):
            bfop.get(self.type, "#{}".format(col))
        return bfop.execute()

    def get_all(self):
        """
        获取整个矩阵的所有行和列。
        """
        matrix = []
        # 遍历并获取矩阵的每一行
        for row in range(self.M):
            matrix.append(self.get_row(row))
        return matrix
