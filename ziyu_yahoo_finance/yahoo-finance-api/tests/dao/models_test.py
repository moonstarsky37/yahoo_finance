import unittest
from dao.models.postgresql_yfinance import YfinanceModel
from dao.crud_yahoo_finance import YfinanceDao
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configs import settings
from datetime import datetime

class DBModelsParserTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(settings().v0.db.dsn)
        self.session = sessionmaker(bind=self.engine)

    def tearDown(self):
        self.engine.dispose()
        # return super().tearDown()

    def test_models(self):
        with self.session.begin() as session:
            _ = session.query(YfinanceModel).limit(1).all()
        self.assertEqual(True, True)

class DaoTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(settings().v0.db.dsn)
        self.session = sessionmaker(bind=self.engine)

    def tearDown(self):
        self.engine.dispose()

    def test_models(self):
        t = datetime.strptime(
            "2022-11-25 00:00:00+08:00",
            '%Y-%m-%d %H:%M:%S%z')
        
        with self.session.begin() as session:
            yfinance_dao: YfinanceDao = YfinanceDao()
            res = yfinance_dao.get_by_time_and_ticker(
                session, t, '2330.TW')
        self.assertIsInstance(res, YfinanceModel)
    

    def test_time_interval(self):
        start_t = datetime.strptime(
            "2022-11-25 00:00:00+08:00",
            '%Y-%m-%d %H:%M:%S%z')
        end_t = datetime.strptime(
        "2022-12-01 00:00:00+08:00",
        '%Y-%m-%d %H:%M:%S%z')

        with self.session.begin() as session:
            yfinance_dao: YfinanceDao = YfinanceDao()
            res = yfinance_dao.get_by_time_interval_and_ticker(
                session, start_t, end_t, '2330.TW')
        
        self.assertIsInstance(res, list)
        list(map(lambda ins: self.assertIsInstance(ins, YfinanceModel), res))
        