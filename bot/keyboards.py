import os

import aiohttp
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup)
from dotenv import load_dotenv

load_dotenv()

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)


async def get_keyboard_base(url):
    """Формирование инлайн-кнопок."""
    result = dict()
    result['title'] = 'Выберите'
    inline_keyboard = InlineKeyboardMarkup(resize_keyboard=True)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json = await response.json()
            for i in range(len(json)):
                title = json[i].get('title')
                button_id = json[i].get('pk')
                link = json[i].get('link')
                random_text = json[i].get('random_text')
                parent_title = json[i].get('parent_title')
                if parent_title:
                    result['title'] = parent_title
                inline_button = InlineKeyboardButton(
                    text=title,
                    url=link,
                    callback_data=f'button_{button_id}_{random_text}',
                )
                inline_keyboard.add(inline_button)
        result['inline_keyboard_markup'] = inline_keyboard
        return result


async def get_keyboard(tg_id, button_id):
    """Получение дочерних инлайн-кнопок для инлайн-кнопки с button_id.
    Отправка данных в ButtonLog о нажатии на кнопку с button_id.
    """
    url = (
            os.getenv('URL_CONTENT') +
            'button/' +
            (f'{button_id}/' if button_id else '') +
            'telegram/' +
            f'{tg_id}/'
    )
    async with aiohttp.ClientSession() as session:
        await session.post(url, data={'tg_id': tg_id, 'button_id': button_id})
    return await get_keyboard_base(url)
