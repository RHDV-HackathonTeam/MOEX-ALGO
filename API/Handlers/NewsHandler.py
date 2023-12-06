from logging import getLogger
from Database.DAL.ChatsDAL import ChatsDAL
from Database.DAL.WebResourcesDAL import WebResourcesDAL
from Database.session import async_session

from fastapi import APIRouter
from fastapi import HTTPException

from Exchanges.MOEX.AlgoPack import *

moex = MOEX()

logger = getLogger(__name__)

news_router = APIRouter()


@news_router.get("/get_all_news")
async def get_all_news():
    try:
        async with async_session() as session:
            chats_dal = ChatsDAL(session)
            web_dal = WebResourcesDAL(session)

            tg_news = await chats_dal.select_all()
            web_news = await web_dal.select_all_web_resources()

            merged_news = []

            for news in web_news:
                merged_news.append({
                    'link': news['link'],
                    'text': news['text'],
                    'date': news['date'],
                    'source': news['resource'],
                    'rating': news['rating']
                })

            for news in tg_news:
                merged_news.append({
                    'link': news['link'],
                    'text': news['text'],
                    'date': news['date'],
                    'source': news['id_channel'],
                    'rating': news['rating']
                })

            sorted_news = sorted(merged_news, key=lambda x: x['date'], reverse=True)

            return sorted_news

    except Exception as e:
        logger.error(f"Error while get news from database: {e}")
        raise HTTPException(status_code=500, detail="Error while get news from database")


@news_router.post("/get_news_by_ticker")
async def get_news_by_ticker(news_data: dict):
    try:
        async with async_session() as session:
            chats_dal = ChatsDAL(session)
            web_dal = WebResourcesDAL(session)

            ticker = news_data.get('ticker')

            web_news = await web_dal.get_resources_by_ticker_tag(ticker=ticker)

            print(web_news)

            merged_news = []

            for news in web_news:
                merged_news.append({
                    'link': news.link,
                    'text': news.text,
                    'date': news.date,
                    'source': news.resource,
                    'rating': news.rating
                })

            sorted_news = sorted(merged_news, key=lambda x: x['date'], reverse=True)

            return sorted_news

    except Exception as e:
        logger.error(f"Error while get news from database: {e}")
        raise HTTPException(status_code=500, detail="Error while get news from database")