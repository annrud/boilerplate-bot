import os
import aiohttp
from aiohttp import client_exceptions
from dotenv import load_dotenv

load_dotenv()


async def get_content(button_id):
    """Получение json с медиа-контентом."""
    url = os.getenv('URL_CONTENT') + 'content/button/' + f'{button_id}/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json = await response.json()
            return json


async def get_file_by_url(url):
    """Получение медиа-файла по url."""
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.read()
                return None
        except (
                client_exceptions.ClientConnectorError,
                client_exceptions.InvalidURL
        ):
            return None


async def send_file_id(content_id, file_id):
    """Отправка телеграм-id файла в БД."""
    url = os.getenv('URL_CONTENT') + 'content/' + f'{content_id}/'
    async with aiohttp.ClientSession() as session:
        await session.post(url, data={'pk': content_id, 'file_id': file_id},)


async def get_random_text():
    """Получение рандомного текста."""
    url = os.getenv('URL_CONTENT') + 'random/'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json = await response.json()
            return json.get('text')
