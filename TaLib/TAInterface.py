from abc import ABCMeta
from abc import abstractclassmethod
from abc import abstractmethod
from abc import abstractstaticmethod

import pandas as pd
from pandas import DataFrame

from Exceptions.TaLibBaseException import TaLibBaseException


class TAInterface(object):
    __metaclass__ = ABCMeta

    @property
    def modules(self):
        return self.__function_groups.keys()

    @abstractmethod
    def __init__(
        self, max_rows: int = 1000, max_columns: int = 1000, width: int = 1000
    ):
        pass
        # pd.set_option("display.max_rows", max_rows)
        # pd.set_option("display.max_columns", max_columns)
        # pd.set_option("display.width", width)

    @abstractclassmethod
    @abstractstaticmethod
    def is_valid_dataframe(func):
        def wrapper(*args, **kwargs):
            if kwargs.get("df") is not None:
                if isinstance(kwargs.get("df"), DataFrame):
                    columns = list(map(lambda x: x, kwargs.get("df").columns))
                    if (
                        "Open"
                        and "High"
                        and "Low"
                        and "Close"
                        and "Volume" not in columns
                    ):
                        raise TaLibBaseException(err="DataFrame is not valid")
                    else:
                        print("df is valid")
                else:
                    raise TaLibBaseException(err="kwargs.get('df') is not DataFrame")

            result = func(**kwargs)
            return result

        return wrapper

    __function_groups = {
        "Cycle Indicators": [
            "HT_DCPERIOD",
            "HT_DCPHASE",
            "HT_PHASOR",
            "HT_SINE",
            "HT_TRENDMODE",
        ],
        "Math Operators": [
            "ADD",
            "DIV",
            "MAX",
            "MAXINDEX",
            "MIN",
            "MININDEX",
            "MINMAX",
            "MINMAXINDEX",
            "MULT",
            "SUB",
            "SUM",
        ],
        "Math Transform": [
            "ACOS",
            "ASIN",
            "ATAN",
            "CEIL",
            "COS",
            "COSH",
            "EXP",
            "FLOOR",
            "LN",
            "LOG10",
            "SIN",
            "SINH",
            "SQRT",
            "TAN",
            "TANH",
        ],
        "Momentum Indicators": [
            "ADX",
            "ADXR",
            "APO",
            "AROON",
            "AROONOSC",
            "BOP",  #
            "CCI",
            "CMO",
            "DX",
            "MACD",
            "MACDEXT",
            "MACDFIX",
            "MFI",
            "MINUS_DI",
            "MINUS_DM",
            "MOM",
            "PLUS_DI",
            "PLUS_DM",
            "PPO",
            "ROC",
            "ROCP",
            "ROCR",
            "ROCR100",
            "RSI",
            "STOCH",
            "STOCHF",
            "STOCHRSI",
            "TRIX",
            "ULTOSC",
            "WILLR",
        ],
        "Overlap Studies": [
            "BBANDS",
            "DEMA",
            "EMA",
            "HT_TRENDLINE",
            "KAMA",
            "MA",
            "MAMA",
            "MAVP",
            "MIDPOINT",
            "MIDPRICE",
            "SAR",
            "SAREXT",
            "SMA",
            "T3",
            "TEMA",
            "TRIMA",
            "WMA",
        ],
        "Pattern Recognition": [
            "CDL2CROWS",
            "CDL3BLACKCROWS",
            "CDL3INSIDE",
            "CDL3LINESTRIKE",
            "CDL3OUTSIDE",
            "CDL3STARSINSOUTH",
            "CDL3WHITESOLDIERS",
            "CDLABANDONEDBABY",
            "CDLADVANCEBLOCK",
            "CDLBELTHOLD",
            "CDLBREAKAWAY",
            "CDLCLOSINGMARUBOZU",
            "CDLCONCEALBABYSWALL",
            "CDLCOUNTERATTACK",
            "CDLDARKCLOUDCOVER",
            "CDLDOJI",
            "CDLDOJISTAR",
            "CDLDRAGONFLYDOJI",
            "CDLENGULFING",
            "CDLEVENINGDOJISTAR",
            "CDLEVENINGSTAR",
            "CDLGAPSIDESIDEWHITE",
            "CDLGRAVESTONEDOJI",
            "CDLHAMMER",
            "CDLHANGINGMAN",
            "CDLHARAMI",
            "CDLHARAMICROSS",
            "CDLHIGHWAVE",
            "CDLHIKKAKE",
            "CDLHIKKAKEMOD",
            "CDLHOMINGPIGEON",
            "CDLIDENTICAL3CROWS",
            "CDLINNECK",
            "CDLINVERTEDHAMMER",
            "CDLKICKING",
            "CDLKICKINGBYLENGTH",
            "CDLLADDERBOTTOM",
            "CDLLONGLEGGEDDOJI",
            "CDLLONGLINE",
            "CDLMARUBOZU",
            "CDLMATCHINGLOW",
            "CDLMATHOLD",
            "CDLMORNINGDOJISTAR",
            "CDLMORNINGSTAR",
            "CDLONNECK",
            "CDLPIERCING",
            "CDLRICKSHAWMAN",
            "CDLRISEFALL3METHODS",
            "CDLSEPARATINGLINES",
            "CDLSHOOTINGSTAR",
            "CDLSHORTLINE",
            "CDLSPINNINGTOP",
            "CDLSTALLEDPATTERN",
            "CDLSTICKSANDWICH",
            "CDLTAKURI",
            "CDLTASUKIGAP",
            "CDLTHRUSTING",
            "CDLTRISTAR",
            "CDLUNIQUE3RIVER",
            "CDLUPSIDEGAP2CROWS",
            "CDLXSIDEGAP3METHODS",
        ],
        "Price Transform": [
            "AVGPRICE",
            "MEDPRICE",
            "TYPPRICE",
            "WCLPRICE",
        ],
        "Statistic Functions": [
            "BETA",
            "CORREL",
            "LINEARREG",
            "LINEARREG_ANGLE",
            "LINEARREG_INTERCEPT",
            "LINEARREG_SLOPE",
            "STDDEV",
            "TSF",
            "VAR",
        ],
        "Volatility Indicators": [
            "ATR",
            "NATR",
            "TRANGE",
        ],
        "Volume Indicators": ["AD", "ADOSC", "OBV"],
    }
