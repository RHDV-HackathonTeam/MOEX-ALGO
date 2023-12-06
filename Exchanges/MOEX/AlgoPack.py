from moexalgo import Market, Ticker
from pandas import DataFrame
from Exchanges.ExchangesInterface import ExchangesInterface, MOEXTimePeriods
from Exceptions import MOEXAlgoPackException
from typing import Any
from typing import List
from typing import Optional
from typing import Union
from pandas import DataFrame
import pandas as pd


class MOEX(ExchangesInterface):
    def __init__(self, apiKeys: Optional[List[str]] = None):
        super().__init__(apiKeys)

    @staticmethod
    def _generator_to_dataframe(generator_data) -> pd.DataFrame:
        return pd.DataFrame(generator_data)

    @staticmethod
    def _handle_error(error):
        error_message = f"Error occurred: {error}"
        raise MOEXAlgoPackException(error_message)

    def get_candles(self, ticker: str, date: str, till_date: str, period: MOEXTimePeriods) -> pd.DataFrame:
        stock = Ticker(ticker)
        try:
            candles_data = stock.candles(date=date, till_date=till_date, period=period.value)
            return self._generator_to_dataframe(candles_data)
        except Exception as e:
            self._handle_error(e)

    def get_tradestats(self, ticker: str, date: str, till_date: str) -> pd.DataFrame:
        stock = Ticker(ticker)
        try:
            tradestats_data = stock.tradestats(date=date, till_date=till_date)
            return self._generator_to_dataframe(tradestats_data)
        except Exception as e:
            self._handle_error(e)

    def get_orderstats(self, ticker: str, date: str, till_date: str) -> pd.DataFrame:
        stock = Ticker(ticker)
        try:
            orderstats_data = stock.orderstats(date=date, till_date=till_date)
            return self._generator_to_dataframe(orderstats_data)
        except Exception as e:
            self._handle_error(e)

    def get_obstats(self, ticker: str, date: str, till_date: str) -> pd.DataFrame:
        stock = Ticker(ticker)
        try:
            obstats_data = stock.obstats(date=date, till_date=till_date)
            return self._generator_to_dataframe(obstats_data)
        except Exception as e:
            self._handle_error(e)

    def get_tickers(self):
        stocks = Market('stocks')

        output = list()

        for ticker in stocks.tickers():
            output.append(ticker['SECID'])

        return output

