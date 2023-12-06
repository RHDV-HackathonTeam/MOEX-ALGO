from logging import getLogger
import numpy as np
from Clustering.ClusteringTickers import *

from fastapi import APIRouter
from fastapi import HTTPException

from Exchanges.MOEX.AlgoPack import *

moex = MOEX()

logger = getLogger(__name__)

cluster_router = APIRouter()


@cluster_router.get("/cluster_tickers")
async def get_clustering_tickers():
    try:
        investor_types = 3
        long_term = 0
        mid_term = 1
        short_term = 2

        df = pd.DataFrame(Market('stocks').obstats(date='2023-11-01'))
        clusterised_df = data_clusterization(df, ['spread_lv10', 'spread_1mio', 'spread_lv10'], investor_types)
        long_term_df = get_tickers_for_specific_type(clusterised_df, long_term)
        mid_term_df = get_tickers_for_specific_type(clusterised_df, mid_term)
        short_term_df = get_tickers_for_specific_type(clusterised_df, short_term)

        response_data = {
            "long_term": long_term_df['secid'].drop_duplicates().tolist(),
            "mid_term": mid_term_df['secid'].drop_duplicates().tolist(),
            "short_term": short_term_df['secid'].drop_duplicates().tolist()
        }

        return response_data

    except Exception as e:
        logger.error(f"Error fetching candles data: {e}")
        raise HTTPException(status_code=500, detail="Error while clustering data")