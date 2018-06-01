import unittest
from gravity import Gravity
from gravity.instance import set_shared_gravity_instance

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grv = Gravity(
            nobroadcast=True,
            # We want to bundle many operations into a single transaction
            bundle=True,
            # Overwrite wallet to use this list of wifs only
            wif=[wif],
            offline=True
        )
        self.grv.set_default_account("init0")
        set_shared_gravity_instance(self.grv)

    def test_get_pub_from_wif(self):
        self.assertEqual(
            self.grv.wallet._get_pub_from_wif(wif),
            "ZGV6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"
        )
