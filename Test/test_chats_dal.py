import asyncio
from Database.DAL.ChatsDAL import ChatsDAL
from Database.session import async_session


async def test_chats_dal():
    async with async_session() as session:
        chats_dal = ChatsDAL(session)

        # chat = await chats_dal.add_chat(id_post=1, id_channel="channel1", date="2023-12-01", text="Test message", link="example.com")
        # print("Added chat:", chat)
        #
        # # Получение последнего ID сообщения для канала
        # last_message_id = await chats_dal.get_last_post_id_for_channel("channel1")
        # print("Last message ID for channel 'channel1':", last_message_id)

        print(await chats_dal.select_all())

# Запуск тестовой функции
asyncio.run(test_chats_dal())
