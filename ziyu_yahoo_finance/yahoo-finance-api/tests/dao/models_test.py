import unittest
from dao.models.postgresql_yfinance import YfinanceModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configs import settings


class DBModelsParserTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(settings().v0.db.dsn)
        self.Session_Maker = sessionmaker(bind=self.engine)
        self.session = self.Session_Maker()

    def tearDown(self):
        self.session.close()
        self.engine.dispose()
        # return super().tearDown()

    def test_models(self):
        with self.session.begin() as session:
            _ = self.session.query(YfinanceModel).limit(1).all()
        self.assertEqual(True, True)