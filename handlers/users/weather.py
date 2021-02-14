from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboard.markup import locationMarkup, weatherMarkup, settingsMarkup, futureWeatherInlineMarkup, mainMarkup
from loader import dp
from classes.User import User
from service.functions.text_function import getCurrentState, sendKeanu, deleteMessages
from service.functions.wheather_function import getWeather, getLocation, searchCities
from states import WeatherState, SettingsState
from states.states_list import FirstSettings


@dp.message_handler(content_types='text', text='Погода')
async def weatherMenu(message: types.Message, state: FSMContext):
    user = User(message.from_user.id)
    await message.delete()
    if user.location is None:
        pass
    else:
        await message.answer(await getWeather(user.getSearchQuery(), state), reply_markup=futureWeatherInlineMarkup(),
                             disable_notification=True)
    await message.answer('Отправте сообщение с названием населенного пункта',
                         reply_markup=locationMarkup(), disable_notification=True)
    await WeatherState.weatherMenu.set()


@dp.message_handler(content_types='location', state=[
    WeatherState.weatherMenu, SettingsState.setMainCity, FirstSettings.indicateMainCity
])
async def weatherByLocation(message: types.Message, state: FSMContext):
    await message.delete()
    cityList = getLocation(message.location)
    currentState = await getCurrentState(state)
    if cityList.__len__() == 1:
        if currentState in ['setMainCity', 'indicateMainCity']:
            await message.answer(await getWeather(cityList[0]))
            user = User(message.from_user.id)
            user.setMainCity(cityList[0][1])
            if currentState == 'setMainCity':
                await message.answer(f"{cityList[0][0]} установлен как город по умолчанию",
                                     reply_markup=settingsMarkup(user))
                await SettingsState.settingsMenu.set()
            else:
                await deleteMessages(message.message_id, message.chat.id, state)
                await message.answer(f"{cityList[0][0]} установлен как город по умолчанию\n"
                                     f"Настройка закончена, спасибо 🤗",
                                     reply_markup=mainMarkup())
                await sendKeanu(message.chat.id)
                await state.reset_state()
        else:
            await message.answer(await getWeather(cityList[0]), reply_markup=futureWeatherInlineMarkup())
    elif cityList.__len__() > 1:
        await message.answer('К сожалению, не удалось точно определить населенный пункт. Но вот, что я нашел 🙄',
                             reply_markup=weatherMarkup(cityList, addSearch=False))
        await state.set_state(cityList)
        if currentState == 'searchState':
            await WeatherState.searchState.set()
    else:
        await message.answer('Вообще ничего не нашел 🥺')


@dp.message_handler(content_types='text', state=[
    WeatherState.weatherMenu, SettingsState.searchMainCity, FirstSettings.indicateMainCity
])
async def weatherBySearch(message: types.Message, state: FSMContext):
    weatherSearch = searchCities(message.text)
    currentState = await getCurrentState(state)
    if weatherSearch.__len__() == 0:
        await message.answer('К сожалению, населенного пункта с таким названием не найдено 😥')
        if currentState == 'indicateMainCity':
            return
    elif weatherSearch.__len__() == 1:
        if currentState == 'indicateMainCity':
            await message.answer(await getWeather(weatherSearch[0]))
            user = User(message.from_user.id)
            user.setMainCity(weatherSearch[0])
            await deleteMessages(message.message_id, message.chat.id, state)
            await message.answer(f"{weatherSearch[0][0]} установлен как город по умолчанию\n"
                                 f"Настройка закончена, спасибо 🤗",
                                 reply_markup=mainMarkup())
            await sendKeanu(message.chat.id)
            await state.reset_state()
            return

        await message.answer(await getWeather(weatherSearch[0]), reply_markup=futureWeatherInlineMarkup())
        return
    else:
        await message.answer('Укажите населенный пункт 🏙️',
                             reply_markup=weatherMarkup(weatherSearch, addSearch=currentState == 'weatherMenu'),
                             disable_notification=True)
    await state.set_data(weatherSearch)
    if currentState == 'searchMainCity':
        await SettingsState.setMainCity.set()
    elif currentState == 'indicateMainCity':
        await FirstSettings.selectMainCity.set()
    else:
        await WeatherState.searchState.set()


@dp.message_handler(content_types='text', state=[
    WeatherState.searchState, SettingsState.setMainCity, FirstSettings.selectMainCity
])
async def selectCity(message: types.Message, state: FSMContext):
    await message.delete()
    if message.text.split('.')[0].isdigit():
        elemNumber = int(message.text.split('.')[0]) - 1
        weatherSearch = await state.get_data()
        await message.answer(await getWeather(weatherSearch[elemNumber]), disable_notification=True)
        currentState = await getCurrentState(state)
        if currentState in ['setMainCity', 'selectMainCity']:
            user = User(message.from_user.id)
            user.setMainCity(weatherSearch[elemNumber][1])
            if currentState == 'selectMainCity':
                await deleteMessages(message.message_id, message.chat.id, state)
                await message.answer(f"{weatherSearch[elemNumber][0]} установлен как город по умолчанию\n"
                                     f"Настройка закончена, спасибо 🤗",
                                     reply_markup=mainMarkup())
                await sendKeanu(message.chat.id)
                await state.reset_state()
                return
            else:
                await message.answer(f"{weatherSearch[elemNumber][0]} установлен как город по умолчанию",
                                     reply_markup=settingsMarkup(user))
                await SettingsState.settingsMenu.set()
    elif message.text == 'Искать еще 🔍':
        await message.delete()

        await message.answer('Укажите населенный пункт 🏙️', reply_markup=locationMarkup(),
                             disable_notification=True)
        await WeatherState.weatherMenu.set()
