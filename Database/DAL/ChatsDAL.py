from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from Database.Models.Model import Chats


class ChatsDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_chat(self, id_post, id_channel, date, text, link):
        try:
            chat = Chats(id_post=id_post, id_channel=id_channel, date=date, text=text, link=link)
            self.session.add(chat)
            await self.session.flush()
            return chat
        except IntegrityError:
            await self.session.rollback()
            return None

    async def get_last_message_id_for_channel(self, id_channel):
        result = await self.session.execute(
            select(Chats.id).filter(Chats.id_channel == id_channel).order_by(Chats.id.desc()).limit(1)
        )
        last_id = result.scalar_one_or_none()
        return last_id

    async def get_chat_texts_for_channel(self, id_channel):
        result = await self.session.execute(
            select(Chats.text).filter(Chats.id_channel == id_channel)
        )
        texts = [row[0] for row in result]
        return texts

    async def get_post_text_for_channel(self, id_post, id_channel):
        result = await self.session.execute(
            select(Chats.text).filter(Chats.id_post == id_post, Chats.id_channel == id_channel).limit(1)
        )
        post_text = result.scalar_one_or_none()
        return post_text
