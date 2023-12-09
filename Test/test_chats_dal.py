import asyncio
from Database.DAL.ChatsDAL import ChatsDAL
from Database.session import async_session
from SentimentClassifier.SentimentClassifier import NewsSentimentClassifier


async def test_chats_dal():
    async with async_session() as session:
        chats_dal = ChatsDAL(session)

        # chat = await chats_dal.add_chat(id_post=1, id_channel="channel1", date="2023-12-01", text="Test message", link="example.com")
        # print("Added chat:", chat)
        #
        # # Получение последнего ID сообщения для канала
        # last_message_id = await chats_dal.get_last_post_id_for_channel("channel1")
        # print("Last message ID for channel 'channel1':", last_message_id)

        news = await chats_dal.select_all()

        classifier = NewsSentimentClassifier()

        for new in news:
            if new['text'] is not None:
                rating = classifier.predict_sentiment(new['text'])
                await chats_dal.add_rating(new['id_post'], new['id_channel'], rating)

            else:
                pass

asyncio.run(test_chats_dal())
