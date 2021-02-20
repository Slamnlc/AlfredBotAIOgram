from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandHelp, CommandStart

from keyboard.markup import startMarkup
from loader import dp
from states.states_list import FirstSettings


@dp.message_handler(CommandHelp(), state="*")
async def bot_help(message: types.Message):
    await message.answer(f"Я бот Альфред и вот что я умею:\n"
                         f"- Работать с курсом валют💱\n"
                         f"- Показывать погоду☂️\n"
                         f"Если что-то пошло не так - нажми /start")


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    await message.answer(f"Добро пожаловать, {message.from_user.first_name}\n"
                         f"Я бот Альфред и вот что я умею:\n"
                         f"- Работать с курсом валют💱\n- Показывать погоду☂️\n"
                         f"Приступим к первоначальной настройке?",
                         reply_markup=startMarkup())
    await state.set_data({'startId': message.message_id})
    await FirstSettings.mainStart.set()
