from abc import ABC

import talib
from pandas.core.frame import DataFrame

from TaLib.TAInterface import TAInterface


class VolatilityIndicators(TAInterface, ABC):
    def __init__(self, max_rows: int, max_columns: int, width: int):
        super().__init__(max_rows=max_rows, max_columns=max_columns, width=width)

    @staticmethod
    @TAInterface.is_valid_dataframe
    def ATR(df: DataFrame, timeperiod: int) -> DataFrame:
        output = df
        output[f"ATR {timeperiod}"] = talib.ATR(
            df["High"], df["Low"], df["Close"], timeperiod=timeperiod
        )
        return output

    @staticmethod
    @TAInterface.is_valid_dataframe
    def NATR(df: DataFrame, timeperiod: int) -> DataFrame:
        output = df
        output[f"NATR {timeperiod}"] = talib.NATR(
            df["High"], df["Low"], df["Close"], timeperiod=timeperiod
        )
        return output

    @staticmethod
    @TAInterface.is_valid_dataframe
    def TRANGE(df: DataFrame) -> DataFrame:
        output = df
        output["TRANGE"] = talib.TRANGE(
            df["High"],
            df["Low"],
            df["Close"],
        )
        return output
