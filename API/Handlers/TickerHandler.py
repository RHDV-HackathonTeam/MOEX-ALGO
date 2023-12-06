from datetime import datetime
from logging import getLogger
from typing import Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from Exchanges.MOEX.AlgoPack import *

from TaLib.Modules.CycleIndicators import CycleIndicators
from TaLib.Modules.MathOperators import MathOperators
from TaLib.Modules.MathTransform import MathTransform
from TaLib.Modules.MomentumIndicators import MomentumIndicators
from TaLib.Modules.OverlapStudies import OverlapStudies
from TaLib.Modules.PatternRecognition import PatternRecognition
from TaLib.Modules.PriceTransform import PriceTransform
from TaLib.Modules.StatisticFunctions import StatisticFunctions
from TaLib.Modules.VolatilityIndicators import VolatilityIndicators
from TaLib.Modules.VolumeIndicators import VolumeIndicators


mi = MomentumIndicators(max_rows=1000, max_columns=1000, width=1000)
ci = CycleIndicators(max_rows=1000, max_columns=1000, width=1000)
mo = MathOperators(max_rows=1000, max_columns=1000, width=1000)
mt = MathTransform(max_rows=1000, max_columns=1000, width=1000)
os = OverlapStudies(max_rows=1000, max_columns=1000, width=1000)
pr = PatternRecognition(max_rows=1000, max_columns=1000, width=1000)
pt = PriceTransform(max_rows=1000, max_columns=1000, width=1000)
sf = StatisticFunctions(max_rows=1000, max_columns=1000, width=1000)
volat_ind = VolatilityIndicators(max_rows=1000, max_columns=1000, width=1000)
volume_ind = VolumeIndicators(max_rows=1000, max_columns=1000, width=1000)

moex = MOEX()

logger = getLogger(__name__)

ticker_router = APIRouter()


@ticker_router.post("/get_candles")
async def get_candles(ticker_data: dict):
    try:
        ticker = ticker_data.get('ticker')
        from_date = ticker_data.get('from_date')
        to_date = ticker_data.get('to_date')
        time_period = MOEXTimePeriods(ticker_data.get('time_period'))

        time_period = MOEXTimePeriods(time_period)

        df = moex.get_candles(ticker, from_date, to_date, time_period)
        df = df.rename(columns={'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'value': 'Value', 'volume': 'Volume', 'begin': 'Begin', 'end': 'End'})
        return df.to_json(orient='values')

    except Exception as e:
        logger.error(f"Error fetching candles data: {e}")
        raise HTTPException(status_code=500, detail="Error fetching candles data")


@ticker_router.get("/ticker_list")
async def get_candles():
    try:
        ticker_list = moex.get_tickers()
        return ticker_list

    except Exception as e:
        logger.error(f"Error fetching candles data: {e}")
        raise HTTPException(status_code=500, detail="Error fetching candles data")



