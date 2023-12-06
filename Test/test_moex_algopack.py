from Exchanges.MOEX.AlgoPack import *

if __name__ == "__main__":
    try:
        moex = MOEX()
        candles_df = moex.get_candles('SBER', '2023-10-10', '2023-10-18', MOEXTimePeriods.TEN_MINUTES)
        print(candles_df.head())

        tradestats_df = moex.get_tradestats('SBER', '2023-10-10', '2023-10-18')
        print(tradestats_df.head())

        orderstats_df = moex.get_orderstats('SBER', '2023-10-10', '2023-10-18')
        print(orderstats_df.head())

        obstats_df = moex.get_obstats('SBER', '2023-10-10', '2023-10-18')
        print(obstats_df.head())

        print(moex.get_tickers())

        stock = Market('stocks').tickers()
        for ticker in stock:
            print(ticker)

    except MOEXAlgoPackException as e:
        print(f"MOEXAlgoPack Error: {e}")