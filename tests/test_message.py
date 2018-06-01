import unittest
import mock
from gravity import Gravity
from gravity.message import Message
from gravity.instance import set_shared_gravity_instance

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
core_unit = "ZGV"


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grv = Gravity(
            nobroadcast=True,
            wif=[wif]
        )
        # from getpass import getpass
        # self.grv.wallet.unlock(getpass())
        set_shared_gravity_instance(self.grv)

    def test_sign_message(self):
        def new_refresh(self):
            dict.__init__(
                self, {
                    "name": "init0",
                    "options": {
                        "memo_key": "ZGV6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV"
                    }})

        with mock.patch(
            "gravity.account.Account.refresh",
            new=new_refresh
        ):
            p = Message("message foobar").sign()
            Message(p).verify()

    def test_verify_message(self):
        Message(
            "-----BEGIN gravity SIGNED MESSAGE-----\n"
            "message foobar\n"
            "-----BEGIN META-----\n"
            "account=init0\n"
            "memokey=ZGV6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV\n"
            "block=6615231\n"
            "timestamp=2018-01-24T10:48:00\n"
            "-----BEGIN SIGNATURE-----\n"
            "204c9f6ef77f5f13e0c94eed16a25a9ffaef794fef4b8101e0f0728e5cc962a0126e650d7d611b88ef8ae2eb9c486e6b8352cc13510b68beb588b3639a55faf2b9\n"
            "-----END gravity SIGNED MESSAGE-----\n"
        ).verify()

        Message(
            "\n\n\n"
            "-----BEGIN gravity SIGNED MESSAGE-----"
            "message foobar\n"
            "-----BEGIN META-----"
            "account=init0\n"
            "memokey=ZGV6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV\n"
            "block=6615231\n"
            "timestamp=2018-01-24T10:48:00\n"
            "-----BEGIN SIGNATURE-----"
            "204c9f6ef77f5f13e0c94eed16a25a9ffaef794fef4b8101e0f0728e5cc962a0126e650d7d611b88ef8ae2eb9c486e6b8352cc13510b68beb588b3639a55faf2b9\n"
            "-----END gravity SIGNED MESSAGE-----\n"
            "\n\n\n"
        ).verify()
