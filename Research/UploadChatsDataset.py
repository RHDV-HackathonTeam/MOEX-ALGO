import json
from Database.DAL.ChatsDAL import ChatsDAL
from Database.DAL.WebResourcesDAL import WebResourcesDAL
from Database.session import async_session
import asyncio


async def main():
    async with async_session() as session:
        chats_dal = ChatsDAL(session)
        web_dal = WebResourcesDAL(session)

        chats = await chats_dal.select_all()
        webs = await web_dal.select_all_web_resources()

        for chat in chats:
            chat['date'] = chat['date'].isoformat() if chat['date'] else None
            chat['rating'] = ''

        for web in webs:
            web['date'] = web['date'].isoformat() if web['date'] else None
            web['rating'] = ''
            json_data = json.dumps(web, indent=4, ensure_ascii=False)

        json_data = json.dumps(chats, indent=4, ensure_ascii=False)
        web_data = json.dumps(webs, indent=4, ensure_ascii=False)

        with open('chats_with_rating.json', 'w', encoding='utf-8') as file:
            file.write(json_data)
            file.write(web_data)


asyncio.run(main())
