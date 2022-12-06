import unittest
from unittest.mock import patch, MagicMock
from unittest import mock
from datetime import datetime
from dao.models.postgresql_yfinance import YfinanceModel
from dao.crud_yahoo_finance import YfinanceDao
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configs import settings
from jobs.yfinance_crawler import insert_stocks_models
from decimal import Decimal


class YFinanceCrawlerTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(settings().v0.db.dsn)
        self.session = sessionmaker(bind=self.engine)

    def tearDown(self):
        self.engine.dispose()

    # @mock.patch('jobs.yfinance_crawler')
    def test_models(self):
        res = insert_stocks_models(self.session, commit=False)
        self.assertIsInstance(res, list)
        for row in res:
            self.assertIsInstance(row[0], datetime)  # datetime(pk):TIMESTAMP
            self.assertIsInstance(row[1], str)  # ticker(pk)  :VARCHAR(10)
            self.assertIsInstance(row[2], Decimal)  # adjclose    :NUMERIC
            self.assertIsInstance(row[3], Decimal)  # close       :NUMERIC
            self.assertIsInstance(row[4], Decimal)  # high        :NUMERIC
            self.assertIsInstance(row[5], Decimal)  # low         :NUMERIC
            self.assertIsInstance(row[6], Decimal)  # open        :NUMERIC
            self.assertIsInstance(row[7], int)  # volume      :BIGINT
            self.assertIsInstance(row[8], datetime)  # createdat   :TIMESTAMP
            self.assertIsInstance(row[9], datetime)  # updatedat   :TIMESTAMP
            self.assertIsInstance(row[9], None)  # deletedat   :TIMESTAMP
