from aiogram import types
from aiogram.dispatcher.filters import CommandHelp, CommandStart

from keyboard.markup import startMarkup
from loader import dp
from states.states_list import FirstSettings


@dp.message_handler(CommandHelp())
async def bot_help(message: types.Message):
    await message.answer('Тут должна быть помощь')


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message):
    await message.answer(f"Добро пожаловать, {message.from_user.first_name}\n"
                         f"Я бот Альфред и вот что я умею:\n"
                         f"- Работать с курсом валют💱\n- Показывать погоду☂️\n- Скачивать книги📚\n"
                         f"Приступим к первоначальной настройке?",
                         reply_markup=startMarkup())
    await FirstSettings.mainStart.set()
