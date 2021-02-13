from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from classes.User import User
from keyboard.inline.callback_data import currency_callback
from keyboard.markup import settingsMarkup
from loader import dp
from filters.currency_flags import IsCurrency
from service.functions.text_function import getCurrentState
from states import SettingsState
from states.states_list import FirstSettings


@dp.callback_query_handler(IsCurrency(), state=[SettingsState.setCurrencyList, FirstSettings.indicateCurrencyList])
async def changeStatus(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    markup: types.InlineKeyboardMarkup = call.message.reply_markup
    for button in markup.inline_keyboard:
        if call.data in button[0].text:
            if '✅' in button[0].text:
                button[0].text = button[0].text.replace('✅', '')
                if button[0].text[:3] in data:
                    data.pop(button[0].text[:3])
            elif data.__len__() < 5:
                button[0].text += '✅'
                data[button[0].text[:3]] = 2
            else:
                await call.message.answer('Выберите до 5 валют')
    markup.inline_keyboard.sort(key=lambda butt: '✅' in butt[0].text)
    if data != await state.get_data():
        await state.set_data(data)
        await call.message.edit_reply_markup(markup)


@dp.callback_query_handler(currency_callback.filter(item_name='back'),
                           state=[SettingsState.setCurrencyList, FirstSettings.indicateCurrencyList])
async def backToSettings(call: CallbackQuery):
    user = User(call.from_user.id)
    await call.message.delete()
    await call.message.answer('Открываю меню настроек', reply_markup=settingsMarkup(user))
    await SettingsState.settingsMenu.set()


@dp.callback_query_handler(currency_callback.filter(item_name='done'),
                           state=[SettingsState.setCurrencyList, FirstSettings.indicateCurrencyList])
async def setUserCurrencyList(call: CallbackQuery, state: FSMContext):
    user = User(call.from_user.id)
    data = await state.get_data()
    if data.__len__() == 0:
        await call.message.answer('Выберите хотя бы одну валюту 🥺')
    else:
        await call.message.delete()
        data = list(data.keys())
        user.setUserCurrency(data)
        currentState = await getCurrentState(state)
        if currentState == 'setCurrencyList':
            await call.message.answer(f"{', '.join(data)} теперь будут отображатся в меню курса валют",
                                      reply_markup=settingsMarkup(user))
            await SettingsState.settingsMenu.set()
        else:
            await call.message.answer(f"{', '.join(data)} теперь будут отображатся в меню курса валют\n"
                                      f"За сколько дней отображать курс валют (напишите число от 1 до 400)?",
                                      reply_markup=types.ReplyKeyboardRemove())
            await FirstSettings.indicateDaysForShow.set()
