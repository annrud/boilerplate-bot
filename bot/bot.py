import os
import logging

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils.executor import start_polling
from dotenv import load_dotenv
import keyboards as kb
import api

load_dotenv()


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

DEBUG = os.getenv('DEBUG')

logging.basicConfig(
    level=logging.DEBUG,
    filename='bot.log',
    format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
)

TYPE_TEXT = 0
TYPE_AUDIO = 1
TYPE_VIDEO = 2
TYPE_PHOTO = 3

BOT_METHODS = {
    TYPE_AUDIO: 'audio',
    TYPE_VIDEO: 'video',
    TYPE_PHOTO: 'photo',
}


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    """Выдача кнопок по команде "start"."""
    tg_id = message.from_user.id
    keyboard = await kb.get_keyboard(tg_id, button_id=None)
    await message.answer(
        f'{keyboard["title"]} 👇',
        reply_markup=keyboard['inline_keyboard_markup']
    )


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('button_'))
async def process_callback(callback_query: types.CallbackQuery):
    """Выдача контента инлайн-кнопки."""
    tg_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    _, button_id, random_text = callback_query.data.split('_')
    keyboard = await kb.get_keyboard(tg_id, button_id)
    content = await api.get_content(button_id)
    if content:
        for content in content:
            content_id = content.get('pk')
            material_type = content.get('material_type')
            file_url = content.get('file_url')
            file_id = content.get('file_id')
            text = content.get('text')
            if material_type == TYPE_TEXT:
                await bot.send_message(tg_id, text)
            else:
                await send_file(
                    tg_id, file_url, file_id, text, material_type, content_id
                )
    if keyboard['inline_keyboard_markup']['inline_keyboard']:
        await callback_query.message.answer(
            f'{keyboard["title"]} 👇',
            reply_markup=keyboard['inline_keyboard_markup']
        )
    if random_text == 'True':
        text = await api.get_random_text()
        await bot.send_message(tg_id, text=text)


async def send_file(tg_id, file_url, file_id, text, material_type, content_id):
    """Отправка медиа-файла."""
    method_name = BOT_METHODS[material_type]
    if file_id:
        file = file_id
    else:
        file = await api.get_file_by_url(file_url)
    if len(text) < 1024:
        res = await getattr(bot, f'send_{method_name}')(
            tg_id,
            file,
            text
        )
    else:
        res = await getattr(bot, f'send_{method_name}')(tg_id, file)
        await bot.send_message(tg_id, text)

    if method_name == 'photo':
        file_id = res[method_name][0]['file_id']
    else:
        file_id = res[method_name]['file_id']
    await api.send_file_id(content_id, file_id)
    return res


if __name__ == '__main__':
    if DEBUG:
        start_polling(dp)
