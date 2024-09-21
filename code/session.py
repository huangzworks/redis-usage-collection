import random
import secrets

# 会话的默认过期时间
DEFAULT_TIMEOUT = 60*60*24*30  # 一个月

# 会话令牌的字节长度
TOKEN_LENGTH = 64

# 会话状态
SESSION_TOKEN_NOT_EXISTS = "TOKEN_NOT_EXISTS"
SESSION_TOKEN_CORRECT = "TOKEN_CORRECT"
SESSION_TOKEN_INCORRECT = "TOKEN_INCORRECT"

def make_token_key(uid):
    return "User:{}:token".format(uid)

class Session:

    def __init__(self, client, uid):
        """
        为给定的用户创建会话对象。
        """
        self.client = client
        self.uid = uid

    def create(self, timeout=DEFAULT_TIMEOUT):
        """
        为给定用户生成会话令牌。
        可选的timeout参数用于指定令牌的过期时限秒数，默认为一个月。
        """
        # 生成令牌
        token = secrets.token_hex(TOKEN_LENGTH)
        # 指定存储令牌的字符串键
        token_key = make_token_key(self.uid)
        # 为用户关联令牌并为其设置过期时间
        self.client.set(token_key, token, ex=timeout)
        # 返回令牌
        return token

    def validate(self, input_token):
        """
        检查给定令牌是否与用户的会话令牌匹配，其结果可以是：
        - SESSION_TOKEN_NOT_EXISTS，令牌不存在或已过期；
        - SESSION_TOKEN_CORRECT，令牌正确；
        - SESSION_TOKEN_INCORRECT，令牌不正确。
        """
        # 构建令牌键并尝试获取令牌
        token_key = make_token_key(self.uid)
        user_token = self.client.get(token_key)
        # 根据令牌的值决定返回何种状态
        if user_token is None:
            return SESSION_TOKEN_NOT_EXISTS
        elif user_token == input_token:
            return SESSION_TOKEN_CORRECT
        else:
            return SESSION_TOKEN_INCORRECT

    def destroy(self):
        """
        销毁用户的会话令牌。
        """
        # 找出令牌对应的键，然后删除它
        token_key = make_token_key(self.uid)
        self.client.delete(token_key)
