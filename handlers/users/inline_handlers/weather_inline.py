import locale
from datetime import date, timedelta

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboard.inline.callback_data import weather_callback
from loader import dp
from service.functions.text_function import addWeatherEmoji, replaceNumberToEmoji
from states import WeatherState


@dp.callback_query_handler(weather_callback.filter(days=['1', '3', '6']),
                           state=[WeatherState.weatherMenu, WeatherState.searchState])
async def showFutureWeather(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    st = ''
    today = date.today()
    locale.setlocale(locale.LC_TIME, "ru_RU")
    for i in range(int(callback_data['days'])):
        today += timedelta(days=1)
        minVal = replaceNumberToEmoji(data['min'][i])
        maxVal = replaceNumberToEmoji(data['max'][i])
        st += f"<b>{today.strftime('%d.%m.%y (%a)')}</b>\t-\tмин.\t{minVal}\t макс.\t{maxVal}\t{data['type'][i]} \n\n"

    await call.message.answer(addWeatherEmoji(st), parse_mode='html')
