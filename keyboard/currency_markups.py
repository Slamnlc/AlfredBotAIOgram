import operator

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

from keyboard.inline.callback_data import numeric_callback, currency_callback
from loader import db
from classes import User


def mainCurrencyMarkup(user: User):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    if user.userCurrency is None:
        currencyList = ['USD', 'RUB']
    else:
        currencyList = user.userCurrency

    data = db.getCurrencyList()

    for curr in currencyList:
        markup.insert(KeyboardButton(f"{curr} {data[curr]['Emoji']}"))
        if markup.keyboard[0].__len__() == 3:
            markup.add()

    markup.insert(KeyboardButton('Другие валюты $ € ¥ ₤ £'))
    markup.add(KeyboardButton('Конвертер валют'))
    markup.add(KeyboardButton('Назад ⬅'))
    return markup


def currencyMarkup(user, inlineMode=False, addCheckBox=False, oneTimeKeyboard=False):
    data = db.getCurrencyList()

    if inlineMode:
        markup = InlineKeyboardMarkup(row_width=6)
        markup.add(InlineKeyboardButton(text='Назад ⬅', callback_data=currency_callback.new(item_name='back')))
        newDict = dict(sorted(user.currencyPriority.items(),
                              key=operator.itemgetter(0),
                              reverse=True
                              ))
        for curr in dict(sorted(newDict.items(), key=operator.itemgetter(1), reverse=False)):
            if addCheckBox and curr in user.userCurrency:
                textToAdd = f'{curr} - {data[curr]["Emoji"]} {data[curr]["FullName"]} ✅'
            else:
                textToAdd = f'{curr} - {data[curr]["Emoji"]} {data[curr]["FullName"]}'
            markup.add(InlineKeyboardButton(text=textToAdd, callback_data=curr))
        markup.add(InlineKeyboardButton(text='Готово ✅', callback_data=currency_callback.new(item_name='done')))
        if addCheckBox:
            markup.inline_keyboard.sort(key=lambda butt: '✅' in butt[0].text)
    else:
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=oneTimeKeyboard)
        markup.add(KeyboardButton('Назад ⬅'))
        markup.add(f"UAH - {data['UAH']['Emoji']} Гривна")
        for curr in user.currencyPriority:
            if curr != 'UAH':
                markup.add(KeyboardButton(f'{curr} - {data[curr]["Emoji"]} {data[curr]["FullName"]}'))

    return markup


def numericMarkup(fromCurrency, toCurrency):

    numberMarkup = InlineKeyboardMarkup(row_width=3)
    data = db.getCurrencyList()

    button1 = InlineKeyboardButton(text='1', callback_data=numeric_callback.new(item_name='1'))
    button2 = InlineKeyboardButton(text="2", callback_data=numeric_callback.new(item_name='2'))
    button3 = InlineKeyboardButton(text="3", callback_data=numeric_callback.new(item_name='3'))
    button4 = InlineKeyboardButton(text="4", callback_data=numeric_callback.new(item_name='4'))
    button5 = InlineKeyboardButton(text="5", callback_data=numeric_callback.new(item_name='5'))
    button6 = InlineKeyboardButton(text="6", callback_data=numeric_callback.new(item_name='6'))
    button7 = InlineKeyboardButton(text="7", callback_data=numeric_callback.new(item_name='7'))
    button8 = InlineKeyboardButton(text="8", callback_data=numeric_callback.new(item_name='8'))
    button9 = InlineKeyboardButton(text="9", callback_data=numeric_callback.new(item_name='9'))
    button0 = InlineKeyboardButton(text="0", callback_data=numeric_callback.new(item_name='0'))

    buttonBack = InlineKeyboardButton(text='Назад ⬅', callback_data=numeric_callback.new(item_name='back'))
    buttonDel = InlineKeyboardButton(text="Del.", callback_data=numeric_callback.new(item_name='del'))
    buttonClear = InlineKeyboardButton(text="Clear", callback_data=numeric_callback.new(item_name='clear'))
    buttonDot = InlineKeyboardButton(text=".", callback_data=numeric_callback.new(item_name='.'))
    buttonResult = InlineKeyboardButton(text="Результат", callback_data=numeric_callback.new(item_name='result'))

    buttonFrom = InlineKeyboardButton(text=f"Из {data[fromCurrency]['Emoji']} - {fromCurrency}",
                                      callback_data=numeric_callback.new(item_name='chFrom'))
    buttonTo = InlineKeyboardButton(text=f"в {data[toCurrency]['Emoji']} - {toCurrency}",
                                    callback_data=numeric_callback.new(item_name='chTo'))

    numberMarkup.add(buttonBack, buttonClear)
    numberMarkup.add(buttonFrom, buttonTo)
    numberMarkup.add(buttonResult)
    numberMarkup.add(button1, button2, button3)
    numberMarkup.add(button4, button5, button6)
    numberMarkup.add(button7, button8, button9)
    numberMarkup.add(buttonDel, button0, buttonDot)

    return numberMarkup
