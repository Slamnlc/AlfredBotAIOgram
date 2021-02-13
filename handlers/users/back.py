from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboard.markup import mainMarkup
from keyboard.currency_markups import mainCurrencyMarkup
from keyboard.yaposka_markup import mainYapMarkup
from loader import dp
from classes.User import User
from states import CurrencyState, Yap


@dp.message_handler(content_types=['text'], text='Назад ⬅', state='*')
async def goBack(message: types.Message, state: FSMContext):
    user = User(message.from_user.id)
    currentState = await state.get_state()
    if currentState is None:
        await message.answer('Перехожу в главное меню', reply_markup=mainMarkup())
        return
    currentState = currentState.split(':')[1]
    await message.delete()
    if currentState in [
        'otherCurrency',
        'changeCurrencyFrom',
        'changeCurrencyFrom',
        'selectCurrencyFrom'
    ]:
        await message.answer('Выберите валюту', reply_markup=mainCurrencyMarkup(user))
        await CurrencyState.mainMenu.set()
    elif currentState in [
        'mainMenu',
        'settingsMenu',
        'searchState',
        'weatherMenu',
        'yapMainMenu'
    ]:
        await message.answer('Окей. Перехожу в главное меню', reply_markup=mainMarkup())
        await state.finish()

    elif currentState in ['subMenu', 'showPhotos']:
        if currentState == 'showPhotos':
            await dp.bot.delete_message(message.chat.id, message.message_id - 1)
        await message.answer('Выберите категорию', reply_markup=mainYapMarkup())
        await Yap.yapMainMenu.set()
