from datetime import datetime
from Exchanges.MOEX.AlgoPack import MOEX
from Exchanges.ExchangesInterface import MOEXTimePeriods


class StrategyTester:

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


