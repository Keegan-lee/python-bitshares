import unittest
from pprint import pprint
from gravity import Gravity
from gravitybase.operationids import getOperationNameForId
from gravity.instance import set_shared_gravity_instance

wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"


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
        self.grv.set_default_account("init0")

    def test_finalizeOps_proposal(self):
        grv = self.grv
        # proposal = grv.new_proposal(grv.tx())
        proposal = grv.proposal()
        self.grv.transfer("init1", 1, "ZGV", append_to=proposal)
        tx = grv.tx().json()  # default tx buffer
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "proposal_create")
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(
            getOperationNameForId(prop["proposed_ops"][0]["op"][0]),
            "transfer")

    def test_finalizeOps_proposal2(self):
        grv = self.grv
        proposal = grv.new_proposal()
        # proposal = grv.proposal()
        self.grv.transfer("init1", 1, "ZGV", append_to=proposal)
        tx = grv.tx().json()  # default tx buffer
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "proposal_create")
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(
            getOperationNameForId(prop["proposed_ops"][0]["op"][0]),
            "transfer")

    def test_finalizeOps_combined_proposal(self):
        grv = self.grv
        parent = grv.new_tx()
        proposal = grv.new_proposal(parent)
        self.grv.transfer("init1", 1, "ZGV", append_to=proposal)
        self.grv.transfer("init1", 1, "ZGV", append_to=parent)
        tx = parent.json()
        ops = tx["operations"]
        self.assertEqual(len(ops), 2)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "proposal_create")
        self.assertEqual(
            getOperationNameForId(ops[1][0]),
            "transfer")
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(
            getOperationNameForId(prop["proposed_ops"][0]["op"][0]),
            "transfer")

    def test_finalizeOps_changeproposer_new(self):
        grv = self.grv
        proposal = grv.proposal(proposer="init5")
        grv.transfer("init1", 1, "ZGV", append_to=proposal)
        tx = grv.tx().json()
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "proposal_create")
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(prop["fee_paying_account"], "1.2.12")
        self.assertEqual(
            getOperationNameForId(prop["proposed_ops"][0]["op"][0]),
            "transfer")

    def test_finalizeOps_changeproposer_legacy(self):
        grv = self.grv
        grv.proposer = "init5"
        tx = grv.transfer("init1", 1, "ZGV")
        ops = tx["operations"]
        self.assertEqual(len(ops), 1)
        self.assertEqual(
            getOperationNameForId(ops[0][0]),
            "proposal_create")
        prop = ops[0][1]
        self.assertEqual(len(prop["proposed_ops"]), 1)
        self.assertEqual(prop["fee_paying_account"], "1.2.12")
        self.assertEqual(
            getOperationNameForId(prop["proposed_ops"][0]["op"][0]),
            "transfer")

    def test_new_proposals(self):
        grv = self.grv
        p1 = grv.new_proposal()
        p2 = grv.new_proposal()
        self.assertIsNotNone(id(p1), id(p2))

    def test_new_txs(self):
        grv = self.grv
        p1 = grv.new_tx()
        p2 = grv.new_tx()
        self.assertIsNotNone(id(p1), id(p2))
