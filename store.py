import memcache
import redis


MEMCACHE_PORT = 11211
REDIS_PORT = 6379
RETRY_COUNT = 4


class Store(object):
    def __init__(self, client_type, address='127.0.0.1', port=None, timeout=20):
        clients = {
            'redis': RedisClient,
            'memcache': MemCacheClient,
        }
        self.client = clients.get(client_type, MemCacheClient)(address, port, timeout)
        self.retry_count = RETRY_COUNT

    def _get(self, key):
        value = self.client.get(key)
        if value is None:
            for _ in range(self.retry_count):
                value = self.client.get(key)
                if value is not None:
                    break
        return value

    def get(self, key):
        value = self._get(key)
        if value is None:
            raise IOError('Cache Reading Error')
        return value

    def cache_get(self, key):
        return self._get(key)

    def cache_set(self, key, value, time):
        result = self.client.set(key, value, time)
        if result == 0:
            for _ in range(self.retry_count):
                value = self.client.get(key)
                if value:
                    return True
                else:
                    return 0
        return True


class MemCacheClient(object):
    def __init__(self, ip_address, port, timeout):
        self.port = port or MEMCACHE_PORT
        self.connection = self.get_connection(ip_address, timeout)

    def get_connection(self, ip_address, timeout):
        address = "{0}:{1}".format(ip_address, self.port)
        return memcache.Client([address], socket_timeout=timeout)

    def get(self, key):
        return self.connection.get(key)

    def set(self, key, value, time):
        return self.connection.set(key, value, time)


def test_connection(func):
    def deco(self, *args):
        if self.connection is None:
            self.connection = self.get_connection()
            if self.connection is None:
                return None
        return func(self, *args)
    return deco


class RedisClient(object):
    def __init__(self, ip_address, port, timeout):
        self.port = port or REDIS_PORT
        self.ip_address = ip_address
        self.timeout = timeout
        self.connection = self.get_connection()

    def get_connection(self):
        try:
            return redis.StrictRedis(host=self.ip_address, port=self.port, db=0, socket_timeout=self.timeout)
        except redis.ConnectionError:
            return None

    @test_connection
    def get(self, key):
        try:
            return self.connection.get(key)
        except redis.ConnectionError:
            return None

    @test_connection
    def set(self, key, value, time):
        try:
            return self.connection.set(key, value, ex=time)
        except redis.ConnectionError:
            return 0
