import pandas as pd
from sklearn.cluster import KMeans
from moexalgo import *

def data_clusterization(data_frame, cluster_metrics, clusters_number):
    df = pd.DataFrame(data_frame)
    df_with_features = df[cluster_metrics]
    model = KMeans(n_clusters=clusters_number, n_init=50, random_state=42)
    model.fit(df_with_features)
    df['cluster'] = model.labels_
    return df
   