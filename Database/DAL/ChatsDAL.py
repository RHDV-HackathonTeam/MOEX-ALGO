from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from Database.Models.Chats import Chats
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import cast
from sqlalchemy import String


class ChatsDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_chat(self, id_post, id_channel, date, text, link):
        existing_chat = await self.get_post_text_for_channel(id_post, id_channel)

        if existing_chat:
            return None

        try:
            chat = Chats(id_post=id_post, id_channel=id_channel, date=date, text=text, link=link)
            self.session.add(chat)
            await self.session.flush()
            return chat
        except IntegrityError:
            await self.session.rollback()
            return None

    async def get_last_post_id_for_channel(self, id_channel):
        result = await self.session.execute(
            select(Chats.id_post)
            .filter(Chats.id_channel == id_channel)
            .order_by(Chats.date.desc(), Chats.id.desc())
            .limit(1)
        )
        last_post_id = result.scalar_one_or_none()
        return last_post_id

    async def get_chat_texts_for_channel(self, id_channel):
        result = await self.session.execute(
            select(Chats.text).filter(Chats.id_channel == id_channel)
        )
        texts = [row[0] for row in result]
        return texts

    async def select_all(self):
        result = await self.session.execute(
            select(Chats)
        )
        chats = []
        for row in result.scalars():
            chat_dict = {
                'id': row.id,
                'id_post': row.id_post,
                'id_channel': row.id_channel,
                'date': row.date,
                'link': row.link,
                'text': row.text,
                'rating': row.rating
            }
            chats.append(chat_dict)
        return chats

    async def get_post_text_for_channel(self, id_post, id_channel):
        result = await self.session.execute(
            select(Chats.text).filter(Chats.id_post == id_post, Chats.id_channel == id_channel).limit(1)
        )
        post_text = result.scalar_one_or_none()
        return post_text

    async def add_rating(self, id_post, id_channel, rating):
        result = await self.session.execute(
            select(Chats).filter(Chats.id_post == id_post, Chats.id_channel == id_channel).limit(1)
        )
        existing_chat = result.scalar_one_or_none()

        if not existing_chat:
            return None

        try:
            existing_chat.rating = rating
            await self.session.flush()
            return existing_chat
        except IntegrityError:
            await self.session.rollback()
            return None

    async def add_tags(self, id_post, id_channel, tags):
        existing_chat = await self.get_post_text_for_channel(id_post, id_channel)

        if not existing_chat:
            return None

        try:
            existing_chat.tags = tags
            await self.session.flush()
            return existing_chat
        except IntegrityError:
            await self.session.rollback()
            return None

    async def get_chats_by_ticker_tag(self, ticker):
        result = await self.session.execute(
            select(Chats)
            .filter(cast(Chats.tags, ARRAY(String)).contains([ticker]))
        )
        resources = [row for row in result.scalars()]
        return resources