from aiogram import types

from classes import User
from data.config import ADMINS
from keyboard.inline.callback_data import weather_callback, book_search
from loader import db
from service.functions.currency_function import getUsersMarkup


def startMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton(text='Приступить к настройке'))
    markup.add(types.KeyboardButton(text='Пропустить и задать настройки по умолчанию'))
    return markup


def mainMarkup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(types.KeyboardButton('Курс валют'))
    markup.add(types.KeyboardButton('Погода'))
    markup.add(types.KeyboardButton('Поиск книг'))
    markup.add(types.KeyboardButton('Настройки'))
    markup.add(types.KeyboardButton('Test'))

    return markup


def settingsMarkup(user: User):
    data = db.getCurrencyList()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    backButton = types.KeyboardButton('Назад ⬅')
    if user.location is None:
        mainCity = types.KeyboardButton(f'Указать основной населенный пункт для погоды')
    else:
        mainCity = types.KeyboardButton(f'Населенный пункт для погоды - {user.getMainCity()}')
    mainCurrency = types.KeyboardButton(f"Основная валюта - {user.currency} {data[user.currency]['Emoji']}")
    dayForShow = types.KeyboardButton(f'Количество дней для вывода курса: {user.dayForShow}')
    currencyList = types.KeyboardButton(f'Список валют в главном меню: {user.getUsedCurrency()}')

    markup.add(backButton)
    markup.add(mainCurrency)
    markup.add(mainCity)
    markup.add(dayForShow)
    markup.add(currencyList)
    if user.id in ADMINS:
        markup.add(types.KeyboardButton(f'Количетсво уникальных пользователей - '
                                        f'{getUsersMarkup(db, returnNumber=True)}'))

    return markup


def locationMarkup(backToMenu=False):
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    if backToMenu:
        markup.add(types.KeyboardButton('Перейти в главное меню'))
    else:
        markup.add(types.KeyboardButton('Назад ⬅'))
    markup.add(types.KeyboardButton(text='Отправить местоположение', request_location=True))
    return markup


def weatherMarkup(cityList, oneTime=False, addSearch=True):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=oneTime)
    markup.add(types.KeyboardButton('Назад ⬅'))
    if addSearch:
        markup.add(types.KeyboardButton('Искать еще 🔍'))
    i = 1
    for elem in cityList:
        markup.add(types.KeyboardButton(f"{i}. {elem[0]}"))
        i += 1
    return markup


def futureWeatherInlineMarkup():
    markup = types.InlineKeyboardMarkup()

    days_1 = types.InlineKeyboardButton(text='На завтра', callback_data=weather_callback.new(days=1))
    days_3 = types.InlineKeyboardButton(text='3 дня', callback_data=weather_callback.new(days=3))
    days_7 = types.InlineKeyboardButton(text='7 дней', callback_data=weather_callback.new(days=6))

    markup.add(days_1, days_3, days_7)

    return markup


def bookMainMenu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Назад ⬅'))
    return markup


def bookMarkup(data: list):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Назад ⬅'))
    for elem in data:
        markup.add(types.KeyboardButton(f"{elem[1].title()} | {elem[2].title()} | "
                                        f"{elem[4]} | Файлов: {elem[6][0].__len__()}"))
    return markup


def bookItemMarkup(data: list):
    markup = types.InlineKeyboardMarkup(row_width=6)
    for item in data:
        txt = item.split('/')[-1]
        markup.insert(types.InlineKeyboardButton(text=txt, callback_data=book_search.new(link=item)))
    return markup
