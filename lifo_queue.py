class LifoQueue:

    def __init__(self, client, key):
        self.client = client
        self.key = key

    def enqueue(self, *items):
        return self.client.rpush(self.key, *items)

    def dequeue(self):
        return self.client.rpop(self.key)

    def length(self):
        return self.client.llen(self.key)
