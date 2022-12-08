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


class YFinanceCrawlerTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(settings().v0.db.dsn)
        self.session = sessionmaker(bind=self.engine)

    def tearDown(self):
        self.engine.dispose()

    @mock.patch('jobs.insert_stocks_models')
    def test_models(self, mock_insert_stocks_models):
        mock_insert_stocks_models.return_value = []
        res = insert_stocks_models(self.session)
        self.assertIsInstance(res, list)
        # print(dir(res[0]), res[0].datetime)
        list(map(lambda ins: self.assertIsInstance(ins, YfinanceModel), res))
