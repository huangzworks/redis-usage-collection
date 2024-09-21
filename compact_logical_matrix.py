from itertools import batched

def calc_index(row, col, col_size):
    """
    将矩阵的行列索引转换为对应的一维位图索引
    """
    return row*col_size+col

def make_matrix_key(matrix_id):
    return "CompactLogicalMatrix:{}".format(matrix_id)

class CompactLogicalMatrix:

    def __init__(self, client, matrix_id, row_size, col_size):
        self.client = client
        self.key = make_matrix_key(matrix_id)
        self.ROW_SIZE = row_size
        self.COL_SIZE = col_size

    def init(self, elements=None):
        """
        根据给定数据对矩阵进行初始化。
        如果没有给定数据，那么将矩阵的所有元素初始化为0。
        """
        # 位图的所有位默认都被初始化为0，无需另外进行设置
        if elements is None: return

        # 遍历矩阵的每个行和列，对其进行设置
        tx = self.client.pipeline()
        for row in range(self.ROW_SIZE):
            for col in range(self.COL_SIZE):
                index = calc_index(row, col, self.COL_SIZE)
                tx.setbit(self.key, index, elements[row][col])
        tx.execute()

    def set(self, row, col, value):
        """
        对矩阵指定行列上的二进制位进行设置。
        """
        index = calc_index(row, col, self.COL_SIZE)
        self.client.setbit(self.key, index, value)

    def get(self, row, col):
        """
        获取矩阵指定行列上的二进制位。
        """
        index = calc_index(row, col, self.COL_SIZE)
        return self.client.getbit(self.key, index)

    def get_row(self, row):
        """
        获取矩阵指定行中所有列的二进制位。
        """
        tx = self.client.pipeline()
        # 遍历组成给定行的所有列
        for col in range(self.COL_SIZE):
            index = calc_index(row, col, self.COL_SIZE)
            tx.getbit(self.key, index)
        return tx.execute()

    def get_all(self):
        """
        获取整个矩阵的所有二进制位。
        """
        tx = self.client.pipeline()
        # 直接以一维方式，遍历组成整个矩阵的所有二进制位
        for i in range(self.ROW_SIZE*self.COL_SIZE):
            tx.getbit(self.key, i)
        all_bits = tx.execute()
        # 将执行事务得到的一维位图转换为二维矩阵（Python>=3.12）
        return [list(row) for row in batched(all_bits, self.COL_SIZE)]
