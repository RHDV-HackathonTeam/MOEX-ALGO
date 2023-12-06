import pandas as pd
from sklearn.cluster import KMeans
from moexalgo import *
from sklearn.impute import SimpleImputer


def data_clusterization(data_frame, cluster_metrics, clusters_number):
    imputer = SimpleImputer(strategy='mean') 
    df = pd.DataFrame(data_frame)
    df_with_features = df[cluster_metrics]
    df_imputed = pd.DataFrame(imputer.fit_transform(df_with_features), columns=df_with_features.columns)
    model = KMeans(n_clusters=clusters_number, n_init=50, random_state=42)
    model.fit(df_imputed)
    df['cluster'] = model.labels_
    return df


def get_tickers_for_specific_type(clusterised_data, number_investor_type):
    ticker_pos = 0
    tickers = pd.DataFrame(clusterised_data.iloc[ticker_pos:ticker_pos + 1, :])
    ticker_pos += 1
    for i in clusterised_data['cluster'][1:]:
        if (i == number_investor_type):
            tickers.loc[ticker_pos] = clusterised_data.iloc[ticker_pos:ticker_pos + 1, :].values[0]
        ticker_pos += 1
    return tickers[1:]