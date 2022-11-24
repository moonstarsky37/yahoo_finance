import unittest
from tests import *

from jobs.yfinance_parser import get_new_finance


class YfinanceParserTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_yfinance_parser(self):
        get_new_finance()


suite = unittest.TestSuite()
suite.addTest(YfinanceParserTestCase("test_yfinance_parser"))
unittest.TextTestRunner(verbosity=2).run(suite)
