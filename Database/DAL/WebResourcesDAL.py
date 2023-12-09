from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from Database.Models.WebResources import WebResources
from sqlalchemy import desc
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import cast
from sqlalchemy import String


class WebResourcesDAL:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_web_resource(self, resource, link, date, tags=None, text=None):
        existing_link = await self.get_text_by_link(link)
        if existing_link:
            return None

        try:
            web_resource = WebResources(resource=resource, link=link, date=date, tags=tags, text=text)
            self.session.add(web_resource)
            await self.session.flush()
            return web_resource
        except IntegrityError:
            await self.session.rollback()
            return None

    async def get_last_added_link(self, resource):
        result = await self.session.execute(
            select(WebResources.link)
            .filter(WebResources.resource == resource)
            .order_by(desc(WebResources.date))
            .limit(1)
        )
        last_link = result.scalar_one_or_none()
        return last_link

    async def select_all_web_resources(self):
        result = await self.session.execute(
            select(WebResources)
        )
        resources = []
        for row in result.scalars():
            resource_dict = {
                'id': row.id,
                'resource': row.resource,
                'link': row.link,
                'date': row.date,
                'tags': row.tags,
                'text': row.text,
                'rating': row.rating
            }
            resources.append(resource_dict)
        return resources

    async def get_all_texts_by_resource(self, resource):
        result = await self.session.execute(
            select(WebResources.text)
            .filter(WebResources.resource == resource)
        )
        texts = [row[0] for row in result]
        return texts

    async def get_text_by_link(self, link):
        result = await self.session.execute(
            select(WebResources.link)
            .filter(WebResources.link == link)
            .limit(1)
        )
        text = result.scalar_one_or_none()
        return text

    async def add_rating(self, link, rating):
        existing_resource = await self.session.execute(select(WebResources).filter(WebResources.link == link).limit(1))
        existing_resource = existing_resource.scalar_one_or_none()
        print(existing_resource)

        if not existing_resource:
            return None

        try:
            existing_resource.rating = rating
            await self.session.flush()
            return existing_resource
        except IntegrityError:
            await self.session.rollback()
            return None

    async def add_tags(self, link, tags):
        existing_resource = await self.get_text_by_link(link)

        if not existing_resource:
            return None

        try:
            existing_resource.tags = tags
            await self.session.flush()
            return existing_resource
        except IntegrityError:
            await self.session.rollback()
            return None

    async def get_resources_by_ticker_tag(self, ticker):
        result = await self.session.execute(
            select(WebResources)
            .filter(cast(WebResources.tags, ARRAY(String)).contains([ticker]))
        )
        resources = [row for row in result.scalars()]
        return resources
