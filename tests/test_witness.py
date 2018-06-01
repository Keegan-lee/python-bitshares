import unittest
from gravity import Gravity
from gravity.witness import Witnesses


class Testcases(unittest.TestCase):

    def test__contains__(self):
        witnesses = Witnesses(gravity_instance=Gravity())
        self.assertIn("init0", witnesses)
        self.assertIn("1.2.7", witnesses)
        self.assertIn("1.6.1", witnesses)
        self.assertNotIn("nathan", witnesses)
