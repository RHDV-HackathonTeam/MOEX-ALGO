import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from API.Handlers.TickerHandler import ticker_router
from API.Handlers.ClusterHandler import cluster_router
from API.Handlers.BacktestHandler import backtest_router
from API.Handlers.NewsHandler import news_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="MOEX Algopack")

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

main_api_router = APIRouter()

main_api_router.include_router(
    ticker_router, prefix="/api/ticker", tags=["ticker"]
)

main_api_router.include_router(
    cluster_router, prefix="/api/clustering", tags=["clustering"]
)

main_api_router.include_router(
    news_router, prefix="/api/news", tags=["news"]
)

main_api_router.include_router(
    backtest_router, prefix="/api/backtest", tags=["backtest"]
)

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9878)