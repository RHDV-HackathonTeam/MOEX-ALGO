from fastapi import APIRouter
from logging import getLogger
from fastapi import HTTPException
from Exchanges.MOEX.AlgoPack import *
from Exchanges.ExchangesInterface import *
from BackTester.Backtester import StrategyTester

logger = getLogger(__name__)

backtest_router = APIRouter()


@backtest_router.post("/dualsma")
async def dualsma(ticker_data: dict):
    try:
        ticker = ticker_data.get('ticker')
        from_date = ticker_data.get('from_date')
        to_date = ticker_data.get('to_date')
        time_period = MOEXTimePeriods(ticker_data.get('time_period'))
        fast_period = ticker_data.get('fast_period')
        long_period = ticker_data.get('long_period')
        risk = ticker_data.get('risk')
        reward_ratio = ticker_data.get('reward_ratio')
        stop_loss_ratio = ticker_data.get('stop_loss_ratio')
        take_profit_ratio = ticker_data.get('take_profit_ratio')
        start_balance = ticker_data.get('start_balance')

        s = StrategyTester(
            balance=start_balance,
            ticker=ticker,
            start_time=from_date,
            end_time=to_date,
            bar_interval=time_period
        )

        s.DualSMAStrategy(fast_period, long_period)
        max_day_loss, max_day_profitability, \
            final_balance, overall_profit, \
            total_trades, profitable_trades \
            = s.backtest_with_news(
            risk=risk,
            reward_ratio=reward_ratio,
            stop_loss_ratio=stop_loss_ratio,
            take_profit_ratio=take_profit_ratio
        )

        df = s.df

        df = df.rename(columns={'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'value': 'Value',
                                'volume': 'Volume', 'begin': 'Begin', 'end': 'End'})
        df = df.where(pd.notnull(df), "Null")
        candles_data = df.to_dict(orient="records")

        response_data = {
            "strategy_name": "DualSMA",
            "max_day_loss": max_day_loss,
            "max_day_profitability": max_day_profitability,
            "final_balance": final_balance,
            "start_balance": start_balance,
            "overall_profit": overall_profit,
            "total_trades": total_trades,
            "profitable_trades": profitable_trades,
            "candles": candles_data
        }

        return response_data

    except Exception as e:
        logger.error(f"Error fetching candles data: {e}")
        raise HTTPException(status_code=500, detail="Error fetching candles data")


@backtest_router.post("/macd")
async def macd(ticker_data: dict):
    try:
        ticker = ticker_data.get('ticker')
        from_date = ticker_data.get('from_date')
        to_date = ticker_data.get('to_date')
        time_period = MOEXTimePeriods(ticker_data.get('time_period'))
        fast_period = ticker_data.get('fast_period')
        slow_period = ticker_data.get('slow_period')
        signal_period = ticker_data.get('signal_period')
        risk = ticker_data.get('risk')
        reward_ratio = ticker_data.get('reward_ratio')
        stop_loss_ratio = ticker_data.get('stop_loss_ratio')
        take_profit_ratio = ticker_data.get('take_profit_ratio')
        start_balance = ticker_data.get('start_balance')

        s = StrategyTester(
            balance=start_balance,
            ticker=ticker,
            start_time=from_date,
            end_time=to_date,
            bar_interval=time_period
        )

        s.MACDStrategy(fastperiod=fast_period, slowperiod=slow_period, signalperiod=signal_period)
        max_day_loss, max_day_profitability, \
            final_balance, overall_profit, \
            total_trades, profitable_trades \
            = s.backtest_with_news(
            risk=risk,
            reward_ratio=reward_ratio,
            stop_loss_ratio=stop_loss_ratio,
            take_profit_ratio=take_profit_ratio
        )

        df = s.df

        df = df.rename(columns={'open': 'Open', 'close': 'Close', 'high': 'High', 'low': 'Low', 'value': 'Value',
                                'volume': 'Volume', 'begin': 'Begin', 'end': 'End'})
        df = df.where(pd.notnull(df), "Null")
        candles_data = df.to_dict(orient="records")

        response_data = {
            "strategy_name": "MACD signal",
            "max_day_loss": max_day_loss,
            "max_day_profitability": max_day_profitability,
            "final_balance": final_balance,
            "start_balance": start_balance,
            "overall_profit": overall_profit,
            "total_trades": total_trades,
            "profitable_trades": profitable_trades,
            "candles": candles_data
        }

        return response_data

    except Exception as e:
        logger.error(f"Error fetching candles data: {e}")
        raise HTTPException(status_code=500, detail="Error fetching candles data")
