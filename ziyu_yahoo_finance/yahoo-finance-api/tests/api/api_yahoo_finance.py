import unittest
import json
from fastapi.testclient import TestClient
from fastapi import status
from init.api import app
from api.api_yahoo_finance import GetYfinanceByTimeIntervalAndTickerResponse

class YfinanceRouterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.client = TestClient(app=app)
        
        # return super().setUp()
    def tearDown(self) -> None:
        # return super().tearDown()
        pass

    # def test_read_docs(self):
    #     response = self.client.get("/docs")
    #     assert response.status_code == 200
    #     # assert type(response.json()) == dict



    def test_yfinance_router_home(self):
        route:str = "/yfinance/"
        response = self.client.get(route, params={
            "start_datetime_str":"2022-11-25 00:00:00+08:00",
            "end_datetime_str":"2022-11-30 00:00:00+08:00",
            "ticker_code":"2330,TW,0050.TW"
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = GetYfinanceByTimeIntervalAndTickerResponse(**response.json())
        self.assertIsInstance(response_json, GetYfinanceByTimeIntervalAndTickerResponse)
        

    
    def test_yfinance_router_home_with_tickers(self):
        route:str = "/yfinance/tickers"
        response = self.client.get(route, params={
            "start_datetime_str":"2022-11-25 00:00:00+08:00",
            "end_datetime_str":"2022-11-30 00:00:00+08:00",
            "tickers_code":"0050.TW"
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_json = GetYfinanceByTimeIntervalAndTickerResponse(**response.json())
        self.assertIsInstance(response_json, GetYfinanceByTimeIntervalAndTickerResponse)
        