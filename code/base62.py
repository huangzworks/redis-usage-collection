import string

BASE = 62
CHARSET = string.digits + string.ascii_letters  # 0..9a..zA..Z

def base62(number):
    """
    将输入整数从10进制转换为62进制。
    """
    # 如果输入值为 0 则直接返回 '0' 作为结果
    if number == 0: return CHARSET[0]

    result = ""
    while number != 0:
        number, i = divmod(number, BASE)
        result = (CHARSET[i]+result)

    return result
