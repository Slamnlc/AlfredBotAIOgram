from aiogram import types
from aiogram.dispatcher import FSMContext

from classes.User import User
from filters import IsCurrency
from keyboard.currency_markups import currencyMarkup
from keyboard.markup import settingsMarkup, locationMarkup
from loader import dp
from service.functions.text_function import getFlag, getCurrentState
from states import SettingsState
from states.states_list import FirstSettings


@dp.message_handler(content_types='text', text='Настройки')
async def openSettingsMenu(message: types.Message):
    user = User(message.from_user.id)
    await message.delete()
    await message.answer('Для изменения нажмите на кнопку с нужным параметром', reply_markup=settingsMarkup(user))
    await SettingsState.settingsMenu.set()


@dp.message_handler(content_types='text', state=SettingsState.settingsMenu,
                    regexp="сновная валюта")
async def changeMainCurrency(message: types.Message):
    await message.delete()
    await message.answer('Выберите валюту, которая будет установлена по умолчанию в конвертере',
                         reply_markup=currencyMarkup(user=User(message.from_user.id)))
    await SettingsState.setMainCurrency.set()


@dp.message_handler(IsCurrency(), content_types='text',
                    state=[SettingsState.setMainCurrency, FirstSettings.showCurrency])
async def setMainCurrencySettings(message: types.Message, state: FSMContext):
    user = User(message.from_user.id)
    currency = message.text[:3]
    await message.delete()
    user.setCurrency(currency)
    currentState = await getCurrentState(state)
    if currentState == 'showCurrency':
        await message.answer(text='Выберите до 5 валют (включительно)', reply_markup=currencyMarkup(user, True, True),
                             disable_notification=True)
        await message.answer(text=f"{currency} {getFlag(currency)} установлена как основная валюта\n"
                                  f"Теперь укажите интересующие Вас валюты (из списка выше)",
                             reply_markup=types.ReplyKeyboardRemove())
        await FirstSettings.indicateCurrencyList.set()
        await state.set_data(user.dictUserCurrency())
    else:
        await message.answer(f"{currency} {getFlag(currency)} установлена как валюта по умолчанию в конвертере",
                             reply_markup=settingsMarkup(user))
        await SettingsState.settingsMenu.set()


@dp.message_handler(content_types='text', state=SettingsState.settingsMenu, regexp="для вывода")
async def changeDayForShow(message: types.Message):
    await message.delete()
    await message.answer('Укажите сколько дней будет отображаться в выводе курса валют')
    await SettingsState.setDayForShow.set()


@dp.message_handler(content_types='text', state=[SettingsState.setDayForShow, FirstSettings.indicateDaysForShow])
async def setDayForShow(message: types.Message, state: FSMContext):
    user = User(message.from_user.id)
    await message.delete()
    if message.text.isdigit():
        if 0 < int(message.text) < 401:
            user.setDayForShow(message.text)
            currentState = await getCurrentState(state)
            if currentState == 'setDayForShow':
                await message.answer(f"Окей. Буду выводить курс за {message.text} дней",
                                     reply_markup=settingsMarkup(user))
                await SettingsState.settingsMenu.set()
            else:
                await message.answer(f"Окей. Буду выводить курс за {message.text} дней\n"
                                     f"Установим населенный пункт для погоды по умолчанию?",
                                     reply_markup=locationMarkup())
                await FirstSettings.indicateMainCity.set()
        else:
            await message.answer("Пожалуйста, укажите целое число от 1 до 400")
    else:
        await message.answer("Пожалуйста, укажите целое число")


@dp.message_handler(content_types='text', state=SettingsState.settingsMenu, regexp='Список валют в')
async def changeCurrencyList(message: types.Message, state: FSMContext):
    user = User(message.from_user.id)
    await message.delete()
    await message.answer('Пожалуйста, выберите интересующие Вас валюты', reply_markup=currencyMarkup(user, True, True),
                         disable_notification=True)
    await message.answer('Выберите до 5 валют')
    await SettingsState.setCurrencyList.set()
    await state.set_data(user.dictUserCurrency())


@dp.message_handler(content_types='text', state=SettingsState.settingsMenu, regexp='пункт для погоды')
async def changeMainCity(message: types.Message):
    await message.delete()
    await message.answer('Напишите название города или отправте местоположение', reply_markup=locationMarkup())
    await SettingsState.searchMainCity.set()
