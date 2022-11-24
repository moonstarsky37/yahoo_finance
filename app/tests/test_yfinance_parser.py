import logging

import unittest
from tests import *

from jobs.yfinance_parser import get_new_finance

logging.getLogger().setLevel(logging.INFO)


class YfinanceParserTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_yfinance_parser(self):
        get_new_finance()
