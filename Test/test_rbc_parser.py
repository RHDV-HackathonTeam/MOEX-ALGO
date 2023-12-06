import asyncio
from Scrapping.Parsers.RBCInvest import RBCParser

if __name__ == "__main__":
    async def main():
        p = RBCParser()
        # await p.parse_hrefs(target_news_url="https://quote.ru/news/article/6564529c9a79473e2da384f0")
        await p.parse_news(url="https://quote.ru/news/article/6564529c9a79473e2da384f0")

    asyncio.run(main())
