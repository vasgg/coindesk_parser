from aiohttp import ClientSession, TCPConnector
from loguru import logger

BASEURL = 'https://www.coindesk.com'
CHUNK = 10
page_number = '/pf/api/v3/content/fetch/search?query=%7B%22search_query%22%3A%22bitcoin%22%2C%22page%22%3A{}'
period_in_hours = '%2C%22filter_url%22%3A%22%26facetedkey%3DpubDate%7C%26facetedvalue%3D{}%7C%22%7D'
logger.add('debug.log', format='{time} {level} {message}', level='DEBUG', retention='30 days', enqueue=True)

session = None


async def get_session() -> ClientSession:
    global session
    if session is None:
        session = ClientSession(connector=TCPConnector(ssl=False))
    return session


async def close_session():
    global session
    if session:
        await session.close()
        session = None


class News:
    def __init__(self, title, link, pubdate):
        self.title = title
        self.link = link
        self.pubdate = pubdate
