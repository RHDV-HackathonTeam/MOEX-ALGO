from Database.DAL.ChatsDAL import ChatsDAL
from Database.session import async_session
import asyncio


async def test():
    async with async_session() as session:
        chats_dal = ChatsDAL(session)
        chat = await chats_dal.add_chat(
            id_post=1203102301230,
            id_channel="123",
            date="123",
            text=None,
            link="123"
        )

        print("Added chat:", chat)

asyncio.run(test())