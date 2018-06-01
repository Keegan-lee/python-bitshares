import time
import unittest
from gravity import Gravity, exceptions
from gravity.instance import set_shared_gravity_instance
from gravity.blockchainobject import BlockchainObject, ObjectCache


test_objects = [
  {'id': '1.19.5',
   "test": "passed"},
  {'id': '1.2.0',
   "name": "committee-account-passed"
  }

]


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grv = Gravity(
            nobroadcast=True,
        )
        set_shared_gravity_instance(self.grv)

    def test_cache(self):
        cache = ObjectCache(default_expiration=1)
        self.assertEqual(str(cache), "ObjectCache(n=0, default_expiration=1)")

        # Data
        cache["foo"] = "bar"
        self.assertIn("foo", cache)
        self.assertEqual(cache["foo"], "bar")
        self.assertEqual(cache.get("foo", "New"), "bar")

        # Expiration
        time.sleep(2)
        self.assertNotIn("foo", cache)

        # Get
        self.assertEqual(cache.get("foo", "New"), "New")

    def test_predefined_data(self):
        from gravity.account import Account
        # Inject test data into cache
        _cache = ObjectCache(default_expiration=60 * 60 * 1)
        for i in test_objects:
            _cache[i["id"]] = i
        self.assertEqual(_cache['1.19.5']["test"], "passed")

        BlockchainObject._cache = _cache

        account = Account("1.2.0")
        self.assertEqual(account["name"], "committee-account-passed")
