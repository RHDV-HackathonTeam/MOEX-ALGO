import asyncio

from SentimentClassifier.SentimentClassifier import NewsSentimentClassifier
from Scrapping.Parsers.RBCInvest import RBCParser
from Scrapping.Parsers.TelegramUserAgent import UserAgentCore
from Database.DAL.ChatsDAL import ChatsDAL
from Database.DAL.WebResourcesDAL import WebResourcesDAL
from Database.session import async_session
from datetime import datetime
from selenium.common.exceptions import StaleElementReferenceException


class MainLayer(object):

    _telegram_chats = [
        "markettwits", #265000
        # "+qKeau08SQjs2M2My" #245063
        "World_Sanctions" #25497
    ]

    @classmethod
    async def ParseIterate(cls):

        try:
            tg = UserAgentCore(session_name="session")
            rbc = RBCParser()
            classifier = NewsSentimentClassifier()

            async with async_session() as session:
                chats_dal = ChatsDAL(session)
                web_dal = WebResourcesDAL(session)

                for chat in cls._telegram_chats:
                    last_message_id = await chats_dal.get_last_post_id_for_channel(chat)
                    await tg.parse_chat(chat_id=chat, last_msg_id=last_message_id)


                last_rbc_href = await web_dal.get_last_added_link(resource="rbc")

                rbc_hrefs = await rbc.parse_hrefs(target_news_url=last_rbc_href)


                try:
                    for href in reversed(rbc_hrefs):
                        output = await rbc.parse_news(url=href)
                        await web_dal.add_web_resource("rbc", href, datetime.now(), tags=output[1], text=output[0])
                        print("added page")

                        rating = classifier.predict_sentiment(output[0])
                        await web_dal.add_rating(href, rating)

                except StaleElementReferenceException:
                    output = ["No data available", []]
                    await web_dal.add_web_resource("rbc", href, datetime.now(), tags=output[1], text=output[0])
                    print("handled stale reference error, added default data")

        except Exception as e:
            return e

        finally:
            await rbc.close_parser()


asyncio.run(MainLayer.ParseIterate())