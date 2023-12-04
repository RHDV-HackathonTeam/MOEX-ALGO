from main import *

investor_types = 3
clusterised_df = data_clusterization(list(Ticker('SBER').obstats(date='2023-12-01')), ['spread_bbo', 'spread_1mio'], investor_types)
#чем больше спред тем более краткосрочным инвестр должен быть; долгосрочный - 0, среднесрочный - 1, краткосрочный - 2,
#потому что так отсортированы центроиды и соответственно их индексы

for i in clusterised_df['cluster']:
    if (i == 0):
        print(clusterised_df[i])
        print('long-term')
    elif (i == 1):
        print(clusterised_df[i])
        print('mid-term')
    else:
        print(clusterised_df[i])
        print('short-term')
