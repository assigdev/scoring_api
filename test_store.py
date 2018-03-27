import unittest
import store


class MemcacheTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store('memcache')

    def test_cache_set(self):
        self.assertTrue(self.store.cache_set('key', 'value', 60))
        self.assertTrue(self.store.cache_set('key', 1, 60))

    def test_get(self):
        self.store.cache_set('key_get', 'value_get', 60)
        self.assertEqual(self.store.get('key_get'), 'value_get')

    def test_get_bad_key(self):
        with self.assertRaises(Exception) as context:
            self.store.get('key_none')
        self.assertTrue('Cache Reading Error' in context.exception)

    def test_cache_get(self):
        self.store.cache_set('key_get', 'value_get', 60)
        self.assertEqual(self.store.cache_get('key_get'), 'value_get')

    def test_cache_get_bad_key(self):
        self.assertEqual(self.store.cache_get('key_none'), None)


class RedisTestCase(unittest.TestCase):
    def setUp(self):
        self.store = store.Store('redis')

    def test_cache_set(self):
        self.assertTrue(self.store.cache_set('key', 'value', 60))
        self.assertTrue(self.store.cache_set('key', 1, 60))

    def test_get(self):
        self.store.cache_set('key_get', 'value_get', 60)
        self.assertEqual(self.store.get('key_get'), 'value_get')

    def test_get_bad_key(self):
        with self.assertRaises(Exception) as context:
            self.store.get('key_none')
        self.assertTrue('Cache Reading Error' in context.exception)

    def test_cache_get(self):
        self.store.cache_set('key_get', 'value_get', 60)
        self.assertEqual(self.store.cache_get('key_get'), 'value_get')

    def test_cache_get_bad_key(self):
        self.assertEqual(self.store.cache_get('key_none'), None)


class CloseConnectionMemcacheTestCase(unittest.TestCase):
    def setUp(self):
        self.wrong_store = store.Store('memcache')
        self.wrong_store.client.connection.buckets.pop()

    def test_cache_set(self):
        self.assertEqual(self.wrong_store.cache_set('key', 'value', 60), 0)
        self.assertEqual(self.wrong_store.cache_set('key', 1, 60), 0)

    def test_get(self):
        with self.assertRaises(Exception) as context:
            self.wrong_store.get('key_get')
        self.assertTrue('Cache Reading Error' in context.exception)

    def test_cache_get(self):
        self.assertIsNone(self.wrong_store.cache_get('key_get'))


class CloseConnectionRedisTestCase(unittest.TestCase):
    def setUp(self):
        self.wrong_store = store.Store('redis')
        self.wrong_store.client.connection.shutdown()

    def test_cache_set(self):
        self.assertEqual(self.wrong_store.cache_set('key', 'value', 60), 0)
        self.assertEqual(self.wrong_store.cache_set('key', 1, 60), 0)

    def test_get(self):
        with self.assertRaises(Exception) as context:
            self.wrong_store.get('key_get')
        self.assertTrue('Cache Reading Error' in context.exception)

    def test_cache_get(self):
        self.assertIsNone(self.wrong_store.cache_get('key_get'))


if __name__ == "__main__":
    unittest.main()
