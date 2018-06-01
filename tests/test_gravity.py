import mock
import string
import unittest
import random

from pprint import pprint

from gravity import Gravity
from gravity.amount import Amount
from gravity.instance import set_shared_gravity_instance
from gravity.blockchainobject import BlockchainObject, ObjectCache

from gravitybase.account import PrivateKey
from gravitybase.operationids import getOperationNameForId

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"
core_unit = "ZGV"

account_id = '1.2.7'
_objects = [{
    'active': {'account_auths': [],
               'address_auths': [],
               'key_auths': [[str(PrivateKey(wif).pubkey),
                              1]],
               'weight_threshold': 1},
    'active_special_authority': [0, {}],
    'blacklisted_accounts': [],
    'blacklisting_accounts': [],
    'cashback_vb': '1.13.0',
    'id': '1.2.7',
    'lifetime_referrer': '1.2.7',
    'lifetime_referrer_fee_percentage': 8000,
    'membership_expiration_date': '1969-12-31T23:59:59',
    'name': 'init0',
    'network_fee_percentage': 2000,
    'options': {'extensions': [],
                'memo_key': str(PrivateKey(wif).pubkey),
                'num_committee': 0,
                'num_witness': 0,
                'votes': [],
                'voting_account': '1.2.5'},
    'owner': {'account_auths': [],
              'address_auths': [],
              'key_auths': [[str(PrivateKey(wif).pubkey),
                             1]],
              'weight_threshold': 1},
    'owner_special_authority': [0, {}],
    'referrer': '1.2.7',
    'referrer_rewards_percentage': 0,
    'registrar': '1.2.7',
    'statistics': '2.6.7',
    'top_n_control_flags': 0,
    'whitelisted_accounts': [],
    'whitelisting_accounts': []
}, {
    'committee_member_account': '1.2.7',
    'id': '1.5.0',
    'total_votes': 0,
    'url': '',
    'vote_id': '0:11'}
]


class Testcases(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.grv = Gravity(
            nobroadcast=True,
            wif={"active": wif}
        )
        set_shared_gravity_instance(self.grv)
        self.grv.set_default_account("init0")
        self.mock()

    def mock(self):
        # Inject test data into cache
        _cache = ObjectCache(default_expiration=60 * 60 * 1, no_overwrite=True)
        for i in _objects:
            _cache[i["id"]] = i
        BlockchainObject._cache = _cache

    def test_connect(self):
        self.grv.connect()

    def test_set_default_account(self):
        self.grv.set_default_account("init0")

    def test_info(self):
        info = self.grv.info()
        for key in ['current_witness',
                    'head_block_id',
                    'head_block_number',
                    'id',
                    'last_irreversible_block_num',
                    'next_maintenance_time',
                    'random',
                    'recently_missed_count',
                    'time']:
            self.assertTrue(key in info)

    def test_finalizeOps(self):
        grv = self.grv
        tx1 = grv.new_tx()
        tx2 = grv.new_tx()
        self.grv.transfer("init1", 1, core_unit, append_to=tx1)
        self.grv.transfer("init1", 2, core_unit, append_to=tx2)
        self.grv.transfer("init1", 3, core_unit, append_to=tx1)
        tx1 = tx1.json()
        tx2 = tx2.json()
        ops1 = tx1["operations"]
        ops2 = tx2["operations"]
        self.assertEqual(len(ops1), 2)
        self.assertEqual(len(ops2), 1)

    def test_transfer(self):
        grv = self.grv
        tx = grv.transfer(
            "1.2.8", 1.33, core_unit, memo="Foobar", account="1.2.7")
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "transfer"
        )
        op = tx["operations"][0][1]
        self.assertIn("memo", op)
        self.assertEqual(op["from"], "1.2.7")
        self.assertEqual(op["to"], "1.2.8")
        amount = Amount(op["amount"])
        self.assertEqual(float(amount), 1.33)

    def test_create_account(self):
        grv = self.grv
        name = ''.join(random.choice(string.ascii_lowercase) for _ in range(12))
        key1 = PrivateKey()
        key2 = PrivateKey()
        key3 = PrivateKey()
        key4 = PrivateKey()
        tx = grv.create_account(
            name,
            registrar="init0",   # 1.2.7
            referrer="init1",    # 1.2.8
            referrer_percent=33,
            owner_key=str(key1.pubkey),
            active_key=str(key2.pubkey),
            memo_key=str(key3.pubkey),
            additional_owner_keys=[str(key4.pubkey)],
            additional_active_keys=[str(key4.pubkey)],
            additional_owner_accounts=["committee-account"],  # 1.2.0
            additional_active_accounts=["committee-account"],
            proxy_account="init0",
            storekeys=False
        )
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "account_create"
        )
        op = tx["operations"][0][1]
        role = "active"
        self.assertIn(
            str(key2.pubkey),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            str(key4.pubkey),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            "1.2.0",
            [x[0] for x in op[role]["account_auths"]])
        role = "owner"
        self.assertIn(
            str(key1.pubkey),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            str(key4.pubkey),
            [x[0] for x in op[role]["key_auths"]])
        self.assertIn(
            "1.2.0",
            [x[0] for x in op[role]["account_auths"]])
        self.assertEqual(
            op["options"]["voting_account"],
            "1.2.7")
        self.assertEqual(
            op["registrar"],
            "1.2.7")
        self.assertEqual(
            op["referrer"],
            "1.2.8")
        self.assertEqual(
            op["referrer_percent"],
            33 * 100)

    def test_weight_threshold(self):
        grv = self.grv

        auth = {'account_auths': [['1.2.0', '1']],
                'extensions': [],
                'key_auths': [
                    ['ZGV55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n', 1],
                    ['ZGV7GM9YXcsoAJAgKbqW2oVj7bnNXFNL4pk9NugqKWPmuhoEDbkDv', 1]],
                'weight_threshold': 3}  # threshold fine
        grv._test_weights_treshold(auth)
        auth = {'account_auths': [['1.2.0', '1']],
                'extensions': [],
                'key_auths': [
                    ['ZGV55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n', 1],
                    ['ZGV7GM9YXcsoAJAgKbqW2oVj7bnNXFNL4pk9NugqKWPmuhoEDbkDv', 1]],
                'weight_threshold': 4}  # too high

        with self.assertRaises(ValueError):
            grv._test_weights_treshold(auth)

    def test_allow(self):
        grv = self.grv
        tx = grv.allow(
            "ZGV55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n",
            weight=1,
            threshold=1,
            permission="owner"
        )
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertIn("owner", op)
        self.assertIn(
            ["ZGV55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n", '1'],
            op["owner"]["key_auths"])
        self.assertEqual(op["owner"]["weight_threshold"], 1)

    """ Disable this test until we can test with an actual setup on the
        main/testnet
    def test_disallow(self):
        grv = self.grv
        with self.assertRaisesRegex(ValueError, ".*Changes nothing.*"):
            grv.disallow(
                "ZGV55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n",
                weight=1,
                threshold=1,
                permission="owner"
            )
        with self.assertRaisesRegex(ValueError, ".*Cannot have threshold of 0.*"):
            grv.disallow(
                "ZGV6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV",
                weight=1,
                threshold=1,
                permission="owner"
            )
    """

    def test_update_memo_key(self):
        grv = self.grv
        tx = grv.update_memo_key("ZGV55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n")
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertEqual(
            op["new_options"]["memo_key"],
            "ZGV55VCzsb47NZwWe5F3qyQKedX9iHBHMVVFSc96PDvV7wuj7W86n")

    def test_approvewitness(self):
        grv = self.grv
        tx = grv.approvewitness("1.6.1")
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "1:0",
            op["new_options"]["votes"])

    def test_approvecommittee(self):
        grv = self.grv
        tx = grv.approvecommittee("1.5.0")
        self.assertEqual(
            getOperationNameForId(tx["operations"][0][0]),
            "account_update"
        )
        op = tx["operations"][0][1]
        self.assertIn(
            "0:11",
            op["new_options"]["votes"])
