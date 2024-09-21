from random import randint, random

def random_key_generator(client, count):
    """
    创建出指定数量的随机类型键。
    """
    for i in range(count):
        # 构建随机键名，比如："Key:3325812056"
        key = "Key:{}".format(str(random())[2:12])
        # 生成一个随机数，并根据它的值创建对应类型的键
        t = randint(1, 6)
        if t == 1: client.set(key, "")
        elif t == 2: client.hset(key, "", "")
        elif t == 3: client.rpush(key, "")
        elif t == 4: client.sadd(key, "")
        elif t == 5: client.zadd(key, {"":0.0})
        elif t == 6: client.xadd(key, {"":""}, "*")
