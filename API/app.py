import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from API.Handlers.TickerHandler import ticker_router
from API.Handlers.ClusterHandler import cluster_router


app = FastAPI(title="StatTron Master Node")

main_api_router = APIRouter()

main_api_router.include_router(
    ticker_router, prefix="/api/ticker", tags=["ticker"]
)

main_api_router.include_router(
    cluster_router, prefix="/api/clustering", tags=["clustering"]
)

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9878)