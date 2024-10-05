from redis import Redis
from cache import Cache

ID = 10086
TTL = 60
REQUEST_TIMES = 5

client = Redis(decode_responses=True)
cache = Cache(client)

def get_content_from_db(id):
    # 模拟从数据库中取出数据
    return "Hello World!"

def get_post_from_template(id):
    # 模拟使用数据和模板生成HTML页面
    content = get_content_from_db(id)
    return "<html><p>{}</p></html>".format(content)

for _ in range(REQUEST_TIMES):
    # 尝试直接从缓存中取出HTML页面
    post = cache.get(ID)
    if post is None:
        # 缓存不存在，访问数据库并生成HTML页面
        # 然后把它放入缓存以便之后访问
        post = get_post_from_template(ID)
        cache.set(ID, post, TTL)
        print("Fetch post from database&template.")
    else:
        # 缓存存在，无需访问数据库也无需生成HTML页面
        print("Fetch post from cache.")
