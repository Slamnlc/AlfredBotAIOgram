from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.users.yaposhka_test import deleteMessages
from keyboard.markup import mainMarkup
from keyboard.currency_markups import mainCurrencyMarkup
from keyboard.yaposka_markup import mainYapMarkup
from loader import dp
from classes.User import User
from service.functions.text_function import sendKeanu
from states import CurrencyState, Yap
from states.states_list import FirstSettings


@dp.message_handler(Text(contains='Назад'), content_types='text', state='*')
async def goBack(message: types.Message, state: FSMContext):
    user = User(message.from_user.id)
    currentState = await state.get_state()
    if currentState is None:
        await message.answer('Перехожу в главное меню', reply_markup=mainMarkup(), disable_notification=True)
        return
    currentState = currentState.split(':')[1]
    await message.delete()
    if currentState in [
        'otherCurrency',
        'changeCurrencyFrom',
        'changeCurrencyFrom',
        'selectCurrencyFrom'
    ]:
        await message.answer('Выберите валюту', reply_markup=mainCurrencyMarkup(user), disable_notification=True)
        await CurrencyState.mainMenu.set()
    elif currentState in [
        'mainMenu',
        'settingsMenu',
        'searchState',
        'weatherMenu',
        'yapMainMenu',
        'bookMenu'
    ]:
        await message.answer('Окей. Перехожу в главное меню', reply_markup=mainMarkup(), disable_notification=True)
        await state.finish()

    elif currentState in ['subMenu', 'showPhotos', 'card']:
        await deleteMessages(message.message_id, message.chat.id, state)
        await message.answer('Выберите категорию', reply_markup=mainYapMarkup(), disable_notification=True)
        await Yap.yapMainMenu.set()

@dp.message_handler(text='Перейти в главное меню', content_types='text', state=FirstSettings.indicateMainCity)
async def openMainMenu(message: types.Message, state: FSMContext):
    await message.answer('Открываю главное меню\nНастройка закончена, спасибо 🤗', reply_markup=mainMarkup())
    await sendKeanu(message.chat.id)
    await state.finish()

