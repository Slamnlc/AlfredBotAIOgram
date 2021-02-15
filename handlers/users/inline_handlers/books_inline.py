from aiogram.types import CallbackQuery

from data import IMAGE_PATH
from filters.general import IsFlib

from loader import dp
from states.states_list import BookSearch
import requests
import os


@dp.callback_query_handler(IsFlib(), state=BookSearch.bookMenu)
async def sendBook(call: CallbackQuery):
    link = f"http:{call.data.split(':')[1]}"
    form = link.split('/')[-1]
    if form == 'read':
        await call.message.answer(link)
    else:
        await call.message.answer('Сейчас все вышлю')
        path = f"{IMAGE_PATH}{call.from_user.id}.{form}"
        with open(path, 'wb') as out_stream:
            req = requests.get(link, stream=True)
            for chunk in req.iter_content(1024):
                out_stream.write(chunk)
        await dp.bot.send_document(call.message.chat.id, document=open(path, 'rb'))
        os.remove(path)
