from datetime import datetime
import numpy as np

from Exchanges.MOEX.AlgoPack import *
from Exchanges.ExchangesInterface import MOEXTimePeriods

import asyncio
from Database.DAL.WebResourcesDAL import WebResourcesDAL
from Database.session import async_session

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


class StrategyTester:

    moex = MOEX()

    def __init__(
            self,
            balance: float,
            ticker: str,
            start_time: datetime,
            end_time: datetime,
            bar_interval: MOEXTimePeriods,
    ):
        self.balance = balance
        self.ticker = ticker
        self.start_time = start_time
        self.end_time = end_time
        self.bar_interval = bar_interval
        self.df = None
        self.DEFAULT_RATING = 6

    def DualSMAStrategy(self, fast_period, long_period):
        self.df = self.moex.get_candles(self.ticker, self.start_time, self.end_time, self.bar_interval)
        print(self.df)
        self.df = self.df.rename(columns={
            'open': 'Open',
            'close': 'Close',
            'high': 'High',
            'low': 'Low',
            'value': 'Value',
            'volume': 'Volume',
            'begin': 'Begin',
            'end': 'End'
        })

        self.df = os.SMA(df=self.df, timeperiod=fast_period)
        self.df = os.SMA(df=self.df, timeperiod=long_period)

        buy_signal_price = list()
        sell_signal_price = list()
        flag = 0

        for i in range(len(self.df)):
            if self.df["SMA 10"][i] > self.df["SMA 50"][i]:
                if flag != 1:
                    buy_signal_price.append(self.df["Close"][i])
                    sell_signal_price.append(np.nan)
                    flag = 1
                else:
                    buy_signal_price.append(np.nan)
                    sell_signal_price.append(np.nan)

            elif self.df["SMA 10"][i] < self.df["SMA 50"][i]:
                if flag != -1:
                    sell_signal_price.append(self.df["Close"][i])
                    buy_signal_price.append(np.nan)
                    flag = -1
                else:
                    buy_signal_price.append(np.nan)
                    sell_signal_price.append(np.nan)

            else:
                buy_signal_price.append(np.nan)
                sell_signal_price.append(np.nan)

        self.df["BUY"] = buy_signal_price
        self.df["SELL"] = sell_signal_price

    def MACDStrategy(self, fastperiod, slowperiod, signalperiod):
        self.df = self.moex.get_candles(self.ticker, self.start_time, self.end_time, self.bar_interval)
        print(self.df)
        self.df = self.df.rename(columns={
            'open': 'Open',
            'close': 'Close',
            'high': 'High',
            'low': 'Low',
            'value': 'Value',
            'volume': 'Volume',
            'begin': 'Begin',
            'end': 'End'
        })

        self.df = mi.MACD(df=self.df,
                            fastperiod=fastperiod,
                            slowperiod=slowperiod,
                            signalperiod=signalperiod
                          )

        buy_signal_price = list()
        sell_signal_price = list()
        flag = 0

        for i in range(len(self.df)):
            if self.df[f'MACD {fastperiod} {slowperiod} {signalperiod}'][i] > self.df[f"MACD signal {fastperiod} {slowperiod} {signalperiod}"][i]:
                if flag != 1:
                    buy_signal_price.append(self.df["Close"][i])
                    sell_signal_price.append(np.nan)
                    flag = 1
                else:
                    buy_signal_price.append(np.nan)
                    sell_signal_price.append(np.nan)

            elif self.df[f'MACD {fastperiod} {slowperiod} {signalperiod}'][i] < self.df[f"MACD signal {fastperiod} {slowperiod} {signalperiod}"][i]:
                if flag != -1:
                    sell_signal_price.append(self.df["Close"][i])
                    buy_signal_price.append(np.nan)
                    flag = -1
                else:
                    buy_signal_price.append(np.nan)
                    sell_signal_price.append(np.nan)

            else:
                buy_signal_price.append(np.nan)
                sell_signal_price.append(np.nan)

        self.df["BUY"] = buy_signal_price
        self.df["SELL"] = sell_signal_price

    async def get_weighted_rating(self, candle_date):

        async with async_session() as session:
            web_dal = WebResourcesDAL(session)
            news = await web_dal.get_resources_by_ticker_tag(ticker=self.ticker)

            DEFAULT_RATING = 6
            total_weighted_rating = 0
            total_weight = 0
            news_count = len(news)

            if news_count == 0:
                return DEFAULT_RATING

            for news_item in news:
                news_date = datetime.strptime(news_item.date, "%Y-%m-%d")
                if news_date <= candle_date:
                    news_date = news_item.date
                    days_difference = (candle_date - news_date).days
                    weight = 1 / (days_difference + 1)
                    total_weighted_rating += news_item.rating * weight
                    total_weight += weight

            return total_weighted_rating / total_weight if total_weight > 0 else DEFAULT_RATING

    def backtest_with_news(self, risk, reward_ratio, stop_loss_ratio, take_profit_ratio):

        initial_balance = self.balance
        max_day_profitability = 0
        max_day_loss = 0
        position = None
        buy_price = None
        total_trades = 0
        profitable_trades = 0

        for i in range(len(self.df)):
            if not np.isnan(self.df['BUY'][i]):
                if position is None:
                    # weighted_rating = self.get_weighted_rating(news, self.df['Begin'].iloc[i])
                    weighted_rating = self.DEFAULT_RATING
                    if weighted_rating > 5:
                        position = 'long'
                        buy_price = self.df['BUY'][i]
                        total_trades += 1
                        self.df.at[i, 'POSITION'] = 'long'
                        if self.balance * risk > 0:
                            trade_size = min((self.balance * risk) / buy_price, self.balance)
                            self.balance -= trade_size
                            position_size = trade_size / buy_price

                            stop_loss = buy_price * (1 - stop_loss_ratio / 100)
                            take_profit = buy_price * (1 + take_profit_ratio / 100)

            elif not np.isnan(self.df['SELL'][i]):
                if position == 'long':
                    position = None
                    sell_price = self.df['SELL'][i]
                    total_trades += 1
                    self.df.at[i, 'POSITION'] = 'closed'
                    if buy_price:
                        trade_profit = (sell_price - buy_price) / buy_price * 100
                        self.balance += position_size * sell_price

                        if sell_price <= stop_loss or sell_price >= take_profit:
                            position = None
                            buy_price = None
                            self.df.at[i, 'POSITION'] = 'closed'
                            position_size = 0

                        if trade_profit >= reward_ratio * risk:
                            position = None
                            buy_price = None
                            self.df.at[i, 'POSITION'] = 'closed'
                            position_size = 0

                        if trade_profit >= max_day_profitability:
                            max_day_profitability = trade_profit
                        elif trade_profit <= max_day_loss:
                            max_day_loss = trade_profit

                        if trade_profit > 0:
                            profitable_trades += 1

        final_balance = self.balance
        overall_profit = (final_balance - initial_balance) / initial_balance * 100

        print(f"Max Day Loss: {max_day_loss:.2f}%")
        print(f"Max Day Profitability: {max_day_profitability:.2f}%")
        print(f"Final Balance: {final_balance:.2f}")
        print(f"Overall Profit/Loss (%): {overall_profit:.2f}")
        print(f"Total Trades: {total_trades}")
        print(f"Profitable Trades: {profitable_trades}")

        return max_day_loss, max_day_profitability, final_balance, overall_profit, total_trades, profitable_trades

    def backtest(self):
        initial_balance = self.balance
        max_day_profitability = 0
        max_day_loss = 0
        position = None
        buy_price = None
        total_trades = 0
        profitable_trades = 0

        for i in range(len(self.df)):
            if not np.isnan(self.df['BUY'][i]):
                if position is None:
                    position = 'long'
                    buy_price = self.df['BUY'][i]
                    total_trades += 1
                elif position == 'short':
                    position = 'long'
                    buy_price = self.df['BUY'][i]
                    total_trades += 1

            elif not np.isnan(self.df['SELL'][i]):
                if position is None:
                    position = 'short'
                    sell_price = self.df['SELL'][i]
                    total_trades += 1
                elif position == 'long':
                    position = 'short'
                    sell_price = self.df['SELL'][i]
                    total_trades += 1

                    if buy_price:
                        trade_profit = (sell_price - buy_price) / buy_price * 100
                        self.balance *= (1 + trade_profit / 100)
                        if trade_profit > 0:
                            profitable_trades += 1

                        if trade_profit > max_day_profitability:
                            max_day_profitability = trade_profit
                        elif trade_profit < max_day_loss:
                            max_day_loss = trade_profit

        final_balance = self.balance
        overall_profit = (final_balance - initial_balance) / initial_balance * 100

        print(f"Max Day Loss: {max_day_loss:.2f}%")
        print(f"Max Day Profitability: {max_day_profitability:.2f}%")
        print(f"Final Balance: {final_balance:.2f}")
        print(f"Overall Profit/Loss (%): {overall_profit:.2f}")
        print(f"Total Trades: {total_trades}")
        print(f"Profitable Trades: {profitable_trades}")

    def risk_reward_backtest(self, risk, reward_ratio, stop_loss_ratio, take_profit_ratio):
        initial_balance = self.balance
        max_day_profitability = 0
        max_day_loss = 0
        position = None
        buy_price = None
        total_trades = 0
        profitable_trades = 0

        for i in range(len(self.df)):
            if not np.isnan(self.df['BUY'][i]):
                if position is None:
                    position = 'long'
                    buy_price = self.df['BUY'][i]
                    total_trades += 1
                    self.df.at[i, 'POSITION'] = 'long'
                    if self.balance * risk > 0:
                        trade_size = min((self.balance * risk) / buy_price, self.balance)
                        self.balance -= trade_size
                        position_size = trade_size / buy_price

                        stop_loss = buy_price * (1 - stop_loss_ratio / 100)
                        take_profit = buy_price * (1 + take_profit_ratio / 100)

            elif not np.isnan(self.df['SELL'][i]):
                if position == 'long':
                    position = None
                    sell_price = self.df['SELL'][i]
                    total_trades += 1
                    self.df.at[i, 'POSITION'] = 'closed'
                    if buy_price:
                        trade_profit = (sell_price - buy_price) / buy_price * 100
                        self.balance += position_size * sell_price

                        if sell_price <= stop_loss or sell_price >= take_profit:
                            position = None
                            buy_price = None
                            self.df.at[i, 'POSITION'] = 'closed'
                            position_size = 0

                        if trade_profit >= reward_ratio * risk:
                            position = None
                            buy_price = None
                            self.df.at[i, 'POSITION'] = 'closed'
                            position_size = 0

                        if trade_profit >= max_day_profitability:
                            max_day_profitability = trade_profit
                        elif trade_profit <= max_day_loss:
                            max_day_loss = trade_profit

                        if trade_profit > 0:
                            profitable_trades += 1

        final_balance = self.balance
        overall_profit = (final_balance - initial_balance) / initial_balance * 100

        print(f"Max Day Loss: {max_day_loss:.2f}%")
        print(f"Max Day Profitability: {max_day_profitability:.2f}%")
        print(f"Final Balance: {final_balance:.2f}")
        print(f"Overall Profit/Loss (%): {overall_profit:.2f}")
        print(f"Total Trades: {total_trades}")
        print(f"Profitable Trades: {profitable_trades}")

        return max_day_loss, max_day_profitability, final_balance, overall_profit, total_trades, profitable_trades


if __name__ == "__main__":
    s = StrategyTester(
        balance=10000,
        ticker="SBER",
        start_time=datetime(2022,10,10),
        end_time=datetime(2023,10,18),
        bar_interval=MOEXTimePeriods.TEN_MINUTES
    )

    # s.DualSMAStrategy(10, 50)
    s.MACDStrategy(fastperiod=12, slowperiod=26, signalperiod=9)
    buy_indices = np.where(s.df["BUY"].notnull())[0]
    sell_indices = np.where(s.df["SELL"].notnull())[0]
    print("Buy signal\n",buy_indices)
    print("Sell signal\n", sell_indices)

    # s.backtest()
    # s.balance = 10000
    s.risk_reward_backtest(risk=1, reward_ratio=3, stop_loss_ratio=2, take_profit_ratio=5)
