from logging import getLogger
from settings import basedir
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
        data_cluster = DataClusterization()
        data = data_cluster.read_tickers_from_json(file_path=f"{basedir}/Clustering/cached_clustering_tickers.json")

        return data

    except Exception as e:
        logger.error(f"Error fetching candles data: {e}")
        raise HTTPException(status_code=500, detail="Error while clustering data")