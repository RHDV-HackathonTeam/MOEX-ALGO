from logging import getLogger
import numpy as np

from fastapi import APIRouter
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


@ticker_router.post("/add_indicators")
async def add_indicators(indicators_data: dict):
    try:
        ticker = indicators_data.get('ticker')
        from_date = indicators_data.get('from_date')
        to_date = indicators_data.get('to_date')
        time_period = MOEXTimePeriods(indicators_data.get('time_period'))

        df = moex.get_candles(ticker, from_date, to_date, time_period)
        df = df.rename(columns={
            'open': 'Open',
            'close': 'Close',
            'high': 'High',
            'low': 'Low',
            'value': 'Value',
            'volume': 'Volume',
            'begin': 'Begin',
            'end': 'End'
        })

        selected_indicators = indicators_data.get('selected_indicators')

        for indicator_data in selected_indicators:
            indicator = indicator_data.get("indicator")
            indicator_params = indicator_data.get("params")

            # CycleIndicators

            if indicator == "HT_DCPERIOD":
                df = ci.HT_DCPERIOD(df=df)

            elif indicator == "HT_DCPHASE":
                df = ci.HT_DCPHASE(df=df)

            elif indicator == "HT_PHASOR":
                df = ci.HT_PHASOR(df=df)

            elif indicator == "HT_SINE":
                df = ci.HT_SINE(df=df)

            # MathTransform

            elif indicator == "ACOS":
                df = mt.ACOS(df=df)

            elif indicator == "ASIN":
                df = mt.ASIN(df=df)

            elif indicator == "ATAN":
                df = mt.ATAN(df=df)

            elif indicator == "CEIL":
                df = mt.CEIL(df=df)

            elif indicator == "COS":
                df = mt.COS(df=df)

            elif indicator == "COSH":
                df = mt.COSH(df=df)

            elif indicator == "EXP":
                df = mt.EXP(df=df)

            elif indicator == "FLOOR":
                df = mt.FLOOR(df=df)

            elif indicator == "LN":
                df = mt.LN(df=df)

            elif indicator == "LOG10":
                df = mt.LOG10(df=df)

            elif indicator == "SIN":
                df = mt.SIN(df=df)

            elif indicator == "SINH":
                df = mt.SINH(df=df)

            elif indicator == "SQRT":
                df = mt.SQRT(df=df)

            elif indicator == "TAN":
                df = mt.TAN(df=df)

            elif indicator == "TANH":
                df = mt.TANH(df=df)

            # MathOperators

            elif indicator == "ADD":
                df = mo.ADD(df=df)

            elif indicator == "DIV":
                df = mo.DIV(df=df)

            elif indicator == "MAX":
                df = mo.MAX(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "MAXINDEX":
                df = mo.MAXINDEX(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "MIN":
                df = mo.MIN(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "MININDEX":
                df = mo.MININDEX(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "MINMAX":
                df = mo.MINMAX(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "MINMAXINDEX":
                df = mo.MINMAXINDEX(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "MULT":
                df = mo.MULT(df=df)

            elif indicator == "SUB":
                df = mo.SUB(df=df)

            elif indicator == "SUM":
                df = mo.SUM(df=df, timeperiod=indicator_params.get("timeperiod"))


            # MomentumIndicators

            elif indicator == "ADX":
                df = mi.ADX(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "ADXR":
                df = mi.ADXR(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "APO":
                df = mi.APO(df=df, fastperiod=indicator_params.get("fastperiod"),
                            slowperiod=indicator_params.get("slowperiod"),
                            matype=indicator_params.get("matype")
                            )

            elif indicator == "AROON":
                df = mi.AROON(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "AROONOSC":
                df = mi.AROONOSC(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "BOP":
                df = mi.BOP(df=df)

            elif indicator == "CCI":
                df = mi.CCI(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "CMO":
                df = mi.CMO(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "DX":
                df = mi.DX(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "MACD":
                mi.MACD(df=df,
                        fastperiod=indicator_params.get("fastperiod"),
                        slowperiod=indicator_params.get("slowperiod"),
                        signalperiod=indicator_params.get("signalperiod")
                        )

            elif indicator == "MACDEXT":
                mi.MACDEXT(df=df,
                           fastperiod=indicator_params.get("fastperiod"),
                           fastmatype=indicator_params.get("fastmatype"),
                           slowperiod=indicator_params.get("slowperiod"),
                           slowmatype=indicator_params.get("slowmatype"),
                           signalperiod=indicator_params.get("signalperiod"),
                           signalmatype=indicator_params.get("signalmatype")
                           )

            elif indicator == "MACDFIX":
                df = mi.MACDFIX(df=df, signalperiod=indicator_params.get("signalperiod"))

            elif indicator == "MFI":
                df = mi.MFI(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "MINUS_DI":
                df = mi.MINUS_DI(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "MINUS_DM":
                df = mi.MINUS_DM(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "MOM":
                df = mi.MOM(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "PLUS_DI":
                df = mi.PLUS_DI(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "PLUS_DM":
                df = mi.PLUS_DM(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "PPO":
                df = mi.PPO(df=df,
                            fastperiod=indicator_params.get("fastperiod"),
                            slowperiod=indicator_params.get("slowperiod"),
                            matype=indicator_params.get("matype")
                            )

            elif indicator == "ROC":
                df = mi.ROC(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "ROCR":
                df = mi.ROCR(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "ROCR100":
                df = mi.ROCR100(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "RSI":
                df = mi.RSI(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "STOCH":
                df = mi.STOCH(df=df,
                              fastk_period=indicator_params.get("fastk_period"),
                              slowk_period=indicator_params.get("slowk_period"),
                              slowk_matype=indicator_params.get("slowk_matype"),
                              slowd_period=indicator_params.get("slowd_period"),
                              slowd_matype=indicator_params.get("slowd_matype")
                              )

            elif indicator == "STOCHF":
                df = mi.STOCHF(df=df,
                               fastk_period=indicator_params.get("fastk_period"),
                               fastd_period=indicator_params.get("fastd_period"),
                               fastd_matype=indicator_params.get("fastd_matype"),
                               )

            elif indicator == "STOCHRSI":
                df = mi.STOCHRSI(df=df,
                                 timeperiod=indicator_params.get("timeperiod"),
                                 fastk_period=indicator_params.get("fastk_period"),
                                 fastd_period=indicator_params.get("fastd_period"),
                                 fastd_matype=indicator_params.get("fastd_matype")
                                 )

            elif indicator == "TRIX":
                df = mi.TRIX(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "ULTOSC":
                df = mi.ULTOSC(df=df,
                               timeperiod1=indicator_params.get("timeperiod1"),
                               timeperiod2=indicator_params.get("timeperiod2"),
                               timeperiod3=indicator_params.get("timeperiod3"),
                               )

            elif indicator == "WILLR":
                df = mi.WILLR(df=df, timeperiod=indicator_params.get("timeperiod"))

            # OverlapStudies

            elif indicator == "BBANDS":
                df = os.BBANDS(df=df,
                               timeperiod=indicator_params.get("timeperiod"),
                               nbdevup=indicator_params.get("nbdevup"),
                               nbdevdn=indicator_params.get("nbdevdn"),
                               matype=indicator_params.get("matype")
                               )

            elif indicator == "DEMA":
                df = os.DEMA(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "EMA":
                df = os.EMA(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "HT_TRENDLINE":
                df = os.HT_TRENDLINE(df=df)

            elif indicator == "KAMA":
                df = os.KAMA(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "MA":
                df = os.MA(df=df,
                           timeperiod=indicator_params.get("timeperiod"),
                           matype=indicator_params.get("matype")
                           )

            elif indicator == "MAMA":
                df = os.MAMA(
                    df=df,
                    fastlimit=indicator_params.get("fastlimit"),
                    slowlimit=indicator_params.get("slowlimit")
                )

            elif indicator == "MIDPOINT":
                df = os.MIDPOINT(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "MIDPRICE":
                df = os.MIDPRICE(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "SAR":
                df = os.SAR(df=df,
                            acceleration=indicator_params.get("acceleration"),
                            maximum=indicator_params.get("maximum")
                            )

            elif indicator == "SAREXT":
                df = os.SAREXT(df=df,
                               startvalue=indicator_params.get("startvalue"),
                               offsetonreverse=indicator_params.get("offsetonreverse"),
                               accelerationinitlong=indicator_params.get("accelerationinitlong"),
                               accelerationlong=indicator_params.get("accelerationlong"),
                               accelerationmaxlong=indicator_params.get("accelerationmaxlong"),
                               accelerationinitshort=indicator_params.get("accelerationinitshort"),
                               accelerationshort=indicator_params.get("accelerationshort"),
                               accelerationmaxshort=indicator_params.get("accelerationmaxshort")
                               )

            elif indicator == "SMA":
                df = os.SMA(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "T3":
                df = os.T3(df=df,
                           timeperiod=indicator_params.get("timeperiod"),
                           vfactor=indicator_params.get("vfactor")
                           )

            elif indicator == "TEMA":
                df = os.TEMA(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "TRIMA":
                df = os.TRIMA(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "WMA":
                df = os.WMA(df=df, timeperiod=indicator_params.get("timeperiod"))

            # PriceTransform

            elif indicator == "AVGPRICE":
                df = pt.AVGPRICE(df=df)

            elif indicator == "MEDPRICE":
                df = pt.MEDPRICE(df=df)

            elif indicator == "TYPPRICE":
                df = pt.TYPPRICE(df=df)

            elif indicator == "WCLPRICE":
                df = pt.WCLPRICE(df=df)

            # VolatilityIndicators
            elif indicator == "ATR":
                df = volat_ind.ATR(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "NATR":
                df = volat_ind.NATR(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "TRANGE":
                df = volat_ind.TRANGE(df=df)

            # VolumeIndicators
            elif indicator == "AD":
                df = volume_ind.AD(df=df)

            elif indicator == "OBV":
                df = volume_ind.OBV(df=df)

            elif indicator == "ADOSC":
                df = volume_ind.ADOSC(df=df,
                                      fastperiod=indicator_params.get("fastperiod"),
                                      slowperiod=indicator_params.get("slowperiod")
                                      )

            # StatisticFunctions
            elif indicator == "BETA":
                df = sf.BETA(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "CORREL":
                df = sf.BETA(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "LINEARREG":
                df = sf.LINEARREG(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "LINEARREG_ANGLE":
                df = sf.LINEARREG_ANGLE(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "LINEARREG_INTERCEPT":
                df = sf.LINEARREG_INTERCEPT(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "LINEARREG_SLOPE":
                df = sf.LINEARREG_SLOPE(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "TSF":
                df = sf.TSF(df=df, timeperiod=indicator_params.get("timeperiod"))

            elif indicator == "STDDEV":
                df = sf.STDDEV(df=df,
                               timeperiod=indicator_params.get("timeperiod"),
                               nbdev=indicator_params.get("nbdev")
                               )
            elif indicator == "VAR":
                df = sf.VAR(df=df,
                            timeperiod=indicator_params.get("timeperiod"),
                            nbdev=indicator_params.get("nbdev")
                            )

            # PatternRecognition

            elif indicator == "CDL2CROWS":
                df = pr.CDL2CROWS(df=df)

            elif indicator == "CDL3BLACKCROWS":
                df = pr.CDL3BLACKCROWS(df=df)

            elif indicator == "CDL3INSIDE":
                df = pr.CDL3INSIDE(df=df)

            elif indicator == "CDL3LINESTRIKE":
                df = pr.CDL3LINESTRIKE(df=df)

            elif indicator == "CDL3OUTSIDE":
                df = pr.CDL3OUTSIDE(df=df)

            elif indicator == "CDL3STARSINSOUTH":
                df = pr.CDL3STARSINSOUTH(df=df)

            elif indicator == "CDL3WHITESOLDIERS":
                df = pr.CDL3WHITESOLDIERS(df=df)

            elif indicator == "CDLABANDONEDBABY":
                df = pr.CDLABANDONEDBABY(df=df, penetration=indicator_params.get("penetration"))

            elif indicator == "CDLADVANCEBLOCK":
                df = pr.CDLADVANCEBLOCK(df=df)

            elif indicator == "CDLBELTHOLD":
                df = pr.CDLBELTHOLD(df=df)

            elif indicator == "CDLBREAKAWAY":
                df = pr.CDLBREAKAWAY(df=df)

            elif indicator == "CDLCLOSINGMARUBOZU":
                df = pr.CDLCLOSINGMARUBOZU(df=df)

            elif indicator == "CDLCONCEALBABYSWALL":
                df = pr.CDLCONCEALBABYSWALL(df=df)

            elif indicator == "CDLCOUNTERATTACK":
                df = pr.CDLCOUNTERATTACK(df=df)

            elif indicator == "CDLDARKCLOUDCOVER":
                df = pr.CDLDARKCLOUDCOVER(df=df, penetration=indicator_params.get("penetration"))

            elif indicator == "CDLDOJI":
                df = pr.CDLDOJI(df=df)

            elif indicator == "CDLDOJISTAR":
                df = pr.CDLDOJISTAR(df=df)

            elif indicator == "CDLDRAGONFLYDOJI":
                df = pr.CDLDRAGONFLYDOJI(df=df)

            elif indicator == "CDLENGULFING":
                df = pr.CDLENGULFING(df=df)

            elif indicator == "CDLEVENINGDOJISTAR":
                df = pr.CDLEVENINGDOJISTAR(df=df, penetration=indicator_params.get("penetration"))

            elif indicator == "CDLEVENINGSTAR":
                df = pr.CDLEVENINGSTAR(df=df, penetration=indicator_params.get("penetration"))

            elif indicator == "CDLGAPSIDESIDEWHITE":
                df = pr.CDLGAPSIDESIDEWHITE(df=df)

            elif indicator == "CDLGRAVESTONEDOJI":
                df = pr.CDLGRAVESTONEDOJI(df=df)

            elif indicator == "CDLHAMMER":
                df = pr.CDLHAMMER(df=df)

            elif indicator == "CDLHANGINGMAN":
                df = pr.CDLHANGINGMAN(df=df)

            elif indicator == "CDLHARAMI":
                df = pr.CDLHARAMI(df=df)

            elif indicator == "CDLHARAMICROSS":
                df = pr.CDLHARAMICROSS(df=df)

            elif indicator == "CDLHIGHWAVE":
                df = pr.CDLHIGHWAVE(df=df)

            elif indicator == "CDLHIKKAKE":
                df = pr.CDLHIKKAKE(df=df)

            elif indicator == "CDLHIKKAKEMOD":
                df = pr.CDLHIKKAKEMOD(df=df)

            elif indicator == "CDLHOMINGPIGEON":
                df = pr.CDLHOMINGPIGEON(df=df)

            elif indicator == "CDLIDENTICAL3CROWS":
                df = pr.CDLIDENTICAL3CROWS(df=df)

            elif indicator == "CDLINNECK":
                df = pr.CDLINNECK(df=df)

            elif indicator == "CDLINVERTEDHAMMER":
                df = pr.CDLINVERTEDHAMMER(df=df)

            elif indicator == "CDLKICKING":
                df = pr.CDLKICKING(df=df)

            elif indicator == "CDLKICKINGBYLENGTH":
                df = pr.CDLKICKINGBYLENGTH(df=df)

            elif indicator == "CDLLADDERBOTTOM":
                df = pr.CDLLADDERBOTTOM(df=df)

            elif indicator == "CDLLONGLEGGEDDOJI":
                df = pr.CDLLONGLEGGEDDOJI(df=df)

            elif indicator == "CDLLONGLINE":
                df = pr.CDLLONGLINE(df=df)

            elif indicator == "CDLMARUBOZU":
                df = pr.CDLMARUBOZU(df=df)

            elif indicator == "CDLMATCHINGLOW":
                df = pr.CDLMATCHINGLOW(df=df)

            elif indicator == "CDLMATHOLD":
                df = pr.CDLMATHOLD(df=df, penetration=indicator_params.get("penetration"))

            elif indicator == "CDLMORNINGDOJISTAR":
                df = pr.CDLMORNINGDOJISTAR(df=df, penetration=indicator_params.get("penetration"))

            elif indicator == "CDLMORNINGSTAR":
                df = pr.CDLMORNINGSTAR(df=df, penetration=indicator_params.get("penetration"))

            elif indicator == "CDLONNECK":
                df = pr.CDLONNECK(df=df)

            elif indicator == "CDLPIERCING":
                df = pr.CDLPIERCING(df=df)

            elif indicator == "CDLRICKSHAWMAN":
                df = pr.CDLRICKSHAWMAN(df=df)

            elif indicator == "CDLRISEFALL3METHODS":
                df = pr.CDLRISEFALL3METHODS(df=df)

            elif indicator == "CDLSEPARATINGLINES":
                df = pr.CDLSEPARATINGLINES(df=df)

            elif indicator == "CDLSHOOTINGSTAR":
                df = pr.CDLSHOOTINGSTAR(df=df)

            elif indicator == "CDLSHORTLINE":
                df = pr.CDLSHORTLINE(df=df)

            elif indicator == "CDLSPINNINGTOP":
                df = pr.CDLSPINNINGTOP(df=df)

            elif indicator == "CDLSTALLEDPATTERN":
                df = pr.CDLSTALLEDPATTERN(df=df)

            elif indicator == "CDLSTICKSANDWICH":
                df = pr.CDLSTICKSANDWICH(df=df)

            elif indicator == "CDLTAKURI":
                df = pr.CDLTAKURI(df=df)

            elif indicator == "CDLTASUKIGAP":
                df = pr.CDLTASUKIGAP(df=df)

            elif indicator == "CDLTHRUSTING":
                df = pr.CDLTHRUSTING(df=df)

            elif indicator == "CDLTRISTAR":
                df = pr.CDLTRISTAR(df=df)

            elif indicator == "CDLUNIQUE3RIVER":
                df = pr.CDLUNIQUE3RIVER(df=df)

            elif indicator == "CDLUPSIDEGAP2CROWS":
                df = pr.CDLUPSIDEGAP2CROWS(df=df)

            elif indicator == "CDLXSIDEGAP3METHODS":
                df = pr.CDLXSIDEGAP3METHODS(df=df)

        df = df.where(pd.notnull(df), "Null")

        candles_data = df.to_dict(orient="records")
        response_data = {
            "candles": candles_data
        }

        return response_data

    except Exception as e:
        logger.error(f"Error adding indicators: {e}")
        raise HTTPException(status_code=500, detail=f"Error adding indicators: {e}")


@ticker_router.post("/get_candles")
async def get_candles(ticker_data: dict):
    try:
        ticker = ticker_data.get('ticker')
        from_date = ticker_data.get('from_date')
        to_date = ticker_data.get('to_date')
        time_period = MOEXTimePeriods(ticker_data.get('time_period'))

        time_period = MOEXTimePeriods(time_period)

        df = moex.get_candles(ticker, from_date, to_date, time_period)
        df = df.rename(columns={'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'value': 'Value',
                                'volume': 'Volume', 'begin': 'Begin', 'end': 'End'})

        candles_data = df.to_dict(orient="records")

        response_data = {
            "candles": candles_data
        }

        return response_data

    except Exception as e:
        logger.error(f"Error fetching candles data: {e}")
        raise HTTPException(status_code=500, detail="Error fetching candles data")


@ticker_router.get("/ticker_list")
async def get_candles():
    try:
        ticker_list = moex.get_tickers()
        response_data = {
            "tickers": ticker_list
        }
        return response_data

    except Exception as e:
        logger.error(f"Error fetching candles data: {e}")
        raise HTTPException(status_code=500, detail="Error fetching candles data")
