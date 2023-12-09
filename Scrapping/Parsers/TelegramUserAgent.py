import asyncio
import dataclasses
from pyrogram import Client
from datetime import date
from Database.DAL.ChatsDAL import ChatsDAL
from Database.session import async_session
from SentimentClassifier.SentimentClassifier import NewsSentimentClassifier

sessions_dirPath = "sessions"


@dataclasses.dataclass
class Post:
    id_post: int
    id_channel: int | str
    date: date
    text: str
    link: str


class UserAgentCore:
    def __init__(self, session_name: str):
        self.session_name = session_name
        self.app = Client(f"{sessions_dirPath}/{session_name}")

    @staticmethod
    async def create_session(session_name: str, api_id: int, api_hash: str):
        async with Client(f"{sessions_dirPath}/{session_name}", api_id, api_hash) as app:
            await app.send_message("me", f"init session {session_name}")
            return app

    async def parse_chat(
            self,
            chat_id: int | str,
            last_msg_id: int
    ):
        posts = []

        try:

            async with self.app as app:
                iterate_status = True
                offset_id = 0

                while iterate_status:
                    async for message in app.get_chat_history(
                            chat_id=chat_id, offset_id=offset_id, limit=100
                    ):

                        if message.id <= 1 or message.id <= last_msg_id:
                            iterate_status = False
                            break

                        post = Post(
                            id_post=message.id,
                            id_channel=chat_id,
                            date=message.date,
                            text=message.text if message.text is not None else message.caption,
                            link=f"https://t.me/{chat_id}/{message.id}"
                        )

                        print(message.id)

                        posts.append(post)
                        offset_id = posts[len(posts) - 1].id_post
                        print("offset", offset_id)

        except Exception as e:
            print(e)

        async with async_session() as session:
            chats_dal = ChatsDAL(session)
            classifier = NewsSentimentClassifier()
            for post in posts:
                await chats_dal.add_chat(
                    id_post=post.id_post,
                    id_channel=post.id_channel,
                    date=post.date,
                    text=post.text,
                    link=post.link
                )

                if post.text is not None:
                    rating = classifier.predict_sentiment(post.text)
                    await chats_dal.add_rating(post.id_post, post.id_channel, rating)


