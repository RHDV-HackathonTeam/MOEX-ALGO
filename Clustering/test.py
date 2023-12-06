from ClusteringTickers import *

investor_types = 3
long_term = 0
mid_term = 1
short_term = 2

# чем больше спред тем более краткосрочным инвестр должен быть, поэтому юзаем ['spread_lv10', 'spread_1mio', 'spread_lv10']; 
# долгосрочный - 0, среднесрочный - 1, краткосрочный - 2, потому что так отсортированы центроиды и соответственно их индексы

df = pd.DataFrame(Market('stocks').obstats(date='2023-11-01'))
clusterised_df = data_clusterization(df, ['spread_lv10', 'spread_1mio', 'spread_lv10'], investor_types)

print(get_tickers_for_specific_type(clusterised_df, long_term))

