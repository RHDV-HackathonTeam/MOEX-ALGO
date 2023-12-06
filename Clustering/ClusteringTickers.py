import pandas as pd
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from moexalgo import Market
from datetime import datetime, timedelta
import json


class DataClusterization:
    def __init__(self):
        self.imputer = SimpleImputer(strategy='mean')
        self.model = None

    def clusterize(self, data_frame, cluster_metrics, clusters_number):
        df_with_features = data_frame[cluster_metrics]
        df_imputed = pd.DataFrame(self.imputer.fit_transform(df_with_features), columns=df_with_features.columns)
        self.model = KMeans(n_clusters=clusters_number, n_init=50, random_state=42)
        self.model.fit(df_imputed)
        data_frame['cluster'] = self.model.labels_
        return data_frame

    def get_tickers_for_specific_type(self, clusterised_data, number_investor_type):
        ticker_pos = 0
        tickers = pd.DataFrame(clusterised_data.iloc[ticker_pos:ticker_pos + 1, :])
        ticker_pos += 1
        for i in clusterised_data['cluster'][1:]:
            if i == number_investor_type:
                tickers.loc[ticker_pos] = clusterised_data.iloc[ticker_pos:ticker_pos + 1, :].values[0]
            ticker_pos += 1
        return tickers[1:]


class ExtendedDataClusterization(DataClusterization):
    def calculate(self, market_obj, investor_types, long_term, mid_term, short_term):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1 * 1)
        date_range = pd.date_range(start=start_date, end=end_date, freq='1D').strftime('%Y-%m-%d')

        print("123")

        combined_data = pd.DataFrame()
        for date in date_range:
            df = pd.DataFrame(market_obj.obstats(date=date))
            print("iter")
            combined_data = pd.concat([combined_data, df], ignore_index=True)

        print("combined")

        clusterised_df = self.clusterize(combined_data, ['spread_lv10', 'spread_1mio', 'spread_lv10'], investor_types)

        print("clustered")

        long_term_tickers = self.get_tickers_for_specific_type(clusterised_df, long_term)
        mid_term_tickers = self.get_tickers_for_specific_type(clusterised_df, mid_term)
        short_term_tickers = self.get_tickers_for_specific_type(clusterised_df, short_term)

        return long_term_tickers, mid_term_tickers, short_term_tickers

    def cache_clusterization(self):
        investor_types = 3
        long_term = 0
        mid_term = 1
        short_term = 2

        market = Market('stocks')

        long_term_tickers, mid_term_tickers, short_term_tickers = self.calculate(market, investor_types,
                                                                                 long_term,
                                                                                 mid_term, short_term)

        result_dict = {
            "long_term": long_term_tickers[0].values.tolist(),
            "mid_term": mid_term_tickers[0].values.tolist(),
            "short_term": short_term_tickers[0].values.tolist()
        }

        with open('investment_tickers.json', 'w') as json_file:
            json.dump(result_dict, json_file, indent=4)

if __name__ == "__main__":
    # c = ExtendedDataClusterization()
    # c.cache_clusterization()
    pass