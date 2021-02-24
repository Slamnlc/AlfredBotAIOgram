import os

from aiogram import types
from aiogram.dispatcher import FSMContext
from filters import IsCurrency
from keyboard.currency_markups import mainCurrencyMarkup
from keyboard.currency_markups import currencyMarkup, numericMarkup
from loader import dp
from classes.User import User
from service.functions.currency_function import getReturnRate
from service.functions.draw_object import drawDiagram, drawHistogramm
from service.functions.text_function import getCurrentState
from states.states_list import CurrencyState


@dp.message_handler(text="Курс валют", content_types="text")
async def openMainCurrencyMenu(message: types.Message):
    user = User(message.from_user.id)
    await message.delete()
    await message.answer('Выберите валюту', reply_markup=mainCurrencyMarkup(user))
    await CurrencyState.mainMenu.set()


@dp.message_handler(IsCurrency(), content_types='text', state=[CurrencyState.mainMenu, CurrencyState.otherCurrency])
async def showRate(message: types.Message, state: FSMContext):
    user = User(message.from_user.id)
    await message.delete()
    currency = message.text[:3].upper()
    user.addCurrencyUse(currency)
    currState = await getCurrentState(state)
    if currState == 'otherCurrency':
        markup = currencyMarkup(user)
    else:
        markup = mainCurrencyMarkup(user)
    if currency == 'UAH':
        await message.answer("Это легко, 1 гривна как стоила 1 гривну, так и стоит 1 гривну 🙃",
                             disable_notification=True)
    elif 20 < user.dayForShow < 63:
        file = drawDiagram(user.dayForShow, currency, user.id)
        await dp.bot.send_photo(message.chat.id, photo=open(file, 'rb'),
                                caption=f'Курс {currency} за {user.dayForShow} дней',
                                reply_markup=markup)
        os.remove(file)
    elif user.dayForShow > 62:
        file = drawHistogramm(user.dayForShow, currency, user.id)
        await dp.bot.send_photo(message.chat.id, open(file, 'rb'),
                                f'Курс {currency} за {user.dayForShow} дней',
                                reply_markup=markup)
        os.remove(file)
    else:
        await message.answer(getReturnRate(currency, user.dayForShow -1), reply_markup=markup,
                             disable_notification=True)


@dp.message_handler(content_types='text', text='Другие валюты $ € ¥ ₤ £', state=CurrencyState.mainMenu)
async def showOtherCurrency(message: types.Message):
    user = User(message.from_user.id)
    await message.delete()
    await message.answer('Выберите валюту', reply_markup=currencyMarkup(user))
    await CurrencyState.otherCurrency.set()


@dp.message_handler(content_types='text', text="Конвертер валют", state=CurrencyState.mainMenu)
async def setFromCurrency(message: types.Message):
    user = User(message.from_user.id)
    await message.delete()
    await message.answer('Из какой валюты будем конвертировать?',
                         reply_markup=currencyMarkup(user, oneTimeKeyboard=True))
    await CurrencyState.selectCurrencyFrom.set()


@dp.message_handler(IsCurrency(), content_types='text', state=CurrencyState.selectCurrencyFrom)
async def currencyExchange(message: types.Message):
    user = User(message.from_user.id)
    currencyFrom = message.text[:3]
    await message.delete()
    await message.answer('Какую сумму конверитровать?', reply_markup=numericMarkup(currencyFrom, user.currency))
    await CurrencyState.selectCurrencyFrom.set()


@dp.message_handler(IsCurrency(), content_types='text', state=CurrencyState.changeCurrencyTo)
async def changeCurrencyToInline(message: types.Message, state: FSMContext):
    currencyTo = message.text[:3]
    data = await state.get_data()
    await message.delete()
    await message.answer('Какую сумму конверитровать?', reply_markup=numericMarkup(data['from'], currencyTo))
    await CurrencyState.selectCurrencyFrom.set()


@dp.message_handler(IsCurrency(), content_types='text', state=CurrencyState.changeCurrencyFrom)
async def changeCurrencyToInline(message: types.Message, state: FSMContext):
    currencyFrom = message.text[:3]
    data = await state.get_data()
    await message.delete()
    await message.answer('Какую сумму конверитровать?', reply_markup=numericMarkup(currencyFrom, data['to']))
    await CurrencyState.selectCurrencyFrom.set()
