from datetime import datetime
import numpy as np

from Exchanges.MOEX.AlgoPack import *
from Exchanges.ExchangesInterface import MOEXTimePeriods

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

    def DualSMAStrategy(self, fast_period, long_period, risk: float, reward_ratio: int):
        self.df = self.moex.get_candles(self.ticker, self.start_time, self.end_time, self.bar_interval)
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
        position = None

        for i in range(len(self.df)):
            if self.df["SMA 10"][i] > self.df["SMA 50"][i]:
                if position != 'long':
                    buy_signal_price.append(self.df["Close"][i])
                    sell_signal_price.append(np.nan)
                    position = 'long'
                else:
                    buy_signal_price.append(np.nan)
                    sell_signal_price.append(np.nan)

            elif self.df["SMA 10"][i] < self.df["SMA 50"][i]:
                if position != 'short':
                    sell_signal_price.append(self.df["Close"][i])
                    buy_signal_price.append(np.nan)
                    position = 'short'
                else:
                    buy_signal_price.append(np.nan)
                    sell_signal_price.append(np.nan)

            else:
                buy_signal_price.append(np.nan)
                sell_signal_price.append(np.nan)

        self.df["BUY"] = buy_signal_price
        self.df["SELL"] = sell_signal_price
        self.df["POSITION"] = np.nan

    def risk_reward_backtest(self, risk=1, reward_ratio=30):
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

            elif not np.isnan(self.df['SELL'][i]):
                if position == 'long':
                    position = None
                    sell_price = self.df['SELL'][i]
                    total_trades += 1
                    self.df.at[i, 'POSITION'] = 'closed'
                    if buy_price:
                        trade_profit = (sell_price - buy_price) / buy_price * 100
                        self.balance += position_size * sell_price
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

        print(f"Максимальный убыток за день: {max_day_loss:.2f}%")
        print(f"Максимальная прибыль за день: {max_day_profitability:.2f}%")
        print(f"Конечный баланс: {final_balance:.2f}")
        print(f"Общая прибыль/убыток (%): {overall_profit:.2f}")
        print(f"Всего сделок: {total_trades}")
        print(f"Прибыльные сделки: {profitable_trades}")


if __name__ == "__main__":
    s = StrategyTester(
        balance=10000,
        ticker="SBER",
        start_time=datetime(2023, 1, 16),
        end_time=datetime(2023, 10, 18),
        bar_interval=MOEXTimePeriods.TEN_MINUTES
    )

    s.DualSMAStrategy(10, 50, 0.01, 3)

    buy_indices = np.where(s.df["BUY"].notnull())[0]
    sell_indices = np.where(s.df["SELL"].notnull())[0]
    print("Сигнал на покупку\n", buy_indices)
    print("Сигнал на продажу\n", sell_indices)

    s.backtest()
