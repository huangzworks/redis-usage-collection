DEFAULT_SEPARATOR = "\n"

class CompactString:

    def __init__(self, client, key, separator=DEFAULT_SEPARATOR):
        """
        可选的separator参数用于指定分隔各个字符串的分隔符，默认为\n。
        """
        self.client = client
        self.key = key
        self.separator = separator

    def append(self, string):
        """
        将给定的字符串添加至已有字符串值的末尾。
        """
        content = string + self.separator
        return self.client.append(self.key, content)

    def get_bytes(self, start=0, end=-1):
        """
        可选的索引参数用于指定想要获取的字符串数据的范围。
        如果没有给定索引范围则默认返回所有字符串。
        这个方法将返回一个列表，其中可以包含零个或任意多个字符串。
        （在指定索引范围的情况下，位于索引两端的字符串可能是不完整的。）
        """
        # 根据索引范围获取字符串数据
        content = self.client.getrange(self.key, start, end)
        # 基于字符串数据的内容对其进行处理
        if content == "":
            # 内容为空
            return []
        elif self.separator not in content:
            # 内容只包含单个不完整的字符串
            return [content]
        else:
            # 内容包含至少一个完整的字符串，基于分隔符对其进行分割
            list_of_strings = content.split(self.separator)
            # 移除split()方法可能在列表中包含的空字符串值
            if "" in list_of_strings:
                list_of_strings.remove("")
            return list_of_strings
