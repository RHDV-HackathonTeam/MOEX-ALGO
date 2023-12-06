import asyncio
from Scrapping.Parsers.TelegramUserAgent import *

if __name__ == "__main__":
    # api_id = 123
    # api_hash = ""
    #
    # asyncio.run(UserAgentCore.create_session(session_name="session", api_id=api_id, api_hash=api_hash))

    u = UserAgentCore(session_name="session")
    asyncio.run(u.parse_chat(chat_id="markettwits", last_msg_id=265000))
    asyncio.run(u.parse_chat(chat_id="newssmartlab", last_msg_id=51818))
    asyncio.run(u.parse_chat(chat_id="World_Sanctions", last_msg_id=25497))