from aiogram import types
from aiogram.dispatcher import FSMContext

from classes.User import User
from keyboard.currency_markups import currencyMarkup
from keyboard.markup import mainMarkup
from loader import dp
from service.functions.text_function import getFlag
from states.states_list import FirstSettings
from loader import db


@dp.message_handler(text='Приступить к настройке', state=FirstSettings.mainStart)
async def start_showMainCurrency(message: types.Message):
    user = User(message.from_user.id)
    await message.delete()
    await message.answer(text='Для начала, укажите валюту, которая будет использована как основная в конверторе валют?',
                         reply_markup=currencyMarkup(user))
    await FirstSettings.showCurrency.set()


@dp.message_handler(regexp='настройки по умолчанию', state=FirstSettings.mainStart)
async def letsStart(message: types.Message, state: FSMContext):
    if db.isExist('id', 'users', message.from_user.id):
        db.deleteUser(message.from_user.id)
    db.addUser(message.from_user.id)
    await message.delete()
    await message.answer(text='Настрокий по умолчанию:\n'
                              f'Основная валюта - UAH {getFlag("UAH")}\n'
                              f'Валюты в главном меню валют - USD {getFlag("USD")}, EUR {getFlag("EUR")}\n'
                              f'Количество дней для вывода курса валют - 10\n',
                         reply_markup=mainMarkup())
    await state.finish()
