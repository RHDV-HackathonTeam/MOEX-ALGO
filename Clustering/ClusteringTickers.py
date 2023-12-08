import pandas as pd
import json
from sklearn.cluster import KMeans
from sklearn.impute import SimpleImputer
from moexalgo import Market
from datetime import datetime, timedelta


class DataClusterization:
    def __init__(self):
        self.imputer = SimpleImputer(strategy='mean')
        self.model = None

    def data_clusterization(self, data_frame, cluster_metrics, clusters_number):
        df = pd.DataFrame(data_frame)
        df_with_features = df[cluster_metrics]
        df_imputed = pd.DataFrame(self.imputer.fit_transform(df_with_features), columns=df_with_features.columns)
        self.model = KMeans(n_clusters=clusters_number, n_init=50, random_state=42)
        self.model.fit(df_imputed)
        df['cluster'] = self.model.labels_
        return df

    def get_tickers_for_specific_type(self, clusterised_data, number_investor_type):
        ticker_pos = 0
        tickers = pd.DataFrame(clusterised_data.iloc[ticker_pos:ticker_pos + 1, :])
        ticker_pos += 1
        for i in clusterised_data['cluster'][1:]:
            if i == number_investor_type:
                tickers.loc[ticker_pos] = clusterised_data.iloc[ticker_pos:ticker_pos + 1, :].values[0]
            ticker_pos += 1
        return tickers[1:]

    def calculate(self):
        investor_types = 3
        long_term = 0
        mid_term = 1
        short_term = 2

        end_date = datetime.now()
        start_date = end_date - timedelta(days=720)

        date_range = pd.date_range(start=start_date, end=end_date, freq='1D').strftime('%Y-%m-%d')

        combined_data = pd.DataFrame()
        for date in date_range:
            df = pd.DataFrame(Market('stocks').obstats(date=date))
            combined_data = pd.concat([combined_data, df], ignore_index=True)

        clusterised_df = self.data_clusterization(
            combined_data,
            ['spread_lv10', 'spread_1mio', 'spread_lv10'],
            investor_types
        )

        long_term_tickers = self.get_tickers_for_specific_type(clusterised_df, long_term)
        mid_term_tickers = self.get_tickers_for_specific_type(clusterised_df, mid_term)
        short_term_tickers = self.get_tickers_for_specific_type(clusterised_df, short_term)

        unique_long_term = long_term_tickers['secid'].unique().tolist()
        unique_mid_term = mid_term_tickers['secid'].unique().tolist()
        unique_short_term = short_term_tickers['secid'].unique().tolist()

        result_dict = {
            "long_term": unique_long_term,
            "mid_term": unique_mid_term,
            "short_term": unique_short_term
        }

        with open('cached_clustering_tickers.json', 'w') as json_file:
            json.dump(result_dict, json_file, indent=4)

    def read_tickers_from_json(self, file_path):
        try:
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)

            return data

        except FileNotFoundError:
            print("Файл не найден.")
            return None


if __name__ == "__main__":
    data_cluster = DataClusterization()
    data_cluster.calculate()
    data = data_cluster.read_tickers_from_json("cached_clustering_tickers.json")
    print(data)
