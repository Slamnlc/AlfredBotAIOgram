import json
import locale
import logging
import operator
from datetime import date, timedelta

from aiogram import types

import loader
import requests


def getRate(currency, howMany):
    locale.setlocale(locale.LC_TIME, "ru_RU")
    today = date.today() - timedelta(days=howMany)
    data = loader.db.getFromDB(currency, 'rate', f"date >= '{today}'", orderBy='ORDER BY DATE DESC')
    returnList = []
    for i in range(data.__len__()):
        today = date.today() - timedelta(days=i)
        # if not loader.db.isExist('date', currency, f"'{today}'"):
        #     addCurrencyInfo(i + 5)

        if "{:.2f}".format(data[i][0]) == '0.00':
            returnList.append(today.strftime('%d.%m.%y (%a)') + ": " + "{:.4f}".format(data[i][0]))
        else:
            returnList.append(today.strftime('%d.%m.%y (%a)') + ": " + "{:.2f}".format(data[i][0]))

    return returnList


def getTodayRate(currency):
    rate = loader.db.getFromDB(currency, 'rate', f"date='{date.today()}'")
    return float(rate[0][0])


def getReturnRate(currency, howMany):
    st = ''
    rateList = getRate(currency, howMany)
    flag = loader.db.getFromDB('currency', 'emoji', f"name='{currency}'")[0][0]
    for x in rateList:
        st = f'{st}{x}\n'
    return f"Курс {currency} {flag} {getMeasure(currency)} за последние " \
           f"{rateList.__len__()} дней\n{st}"


async def addCurrencyInfo(howMany, currency=None):
    logging.info('Start updating currency rate')
    if currency is None:
        url = f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?date='
    else:
        url = f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={currency}&date='
    today = date.today() + timedelta(days=2)
    locale.setlocale(locale.LC_TIME, "ru_RU")
    newTables = ''
    for i in range(howMany):
        today = today - timedelta(days=1)
        res = requests.get(f"{url}{today.strftime('%Y%m%d')}&json")
        if res.text.find('rate') != -1:
            respJson = json.loads(res.text)
            for curr in respJson:
                if not loader.db.isTableExist(curr['cc']):
                    loader.db.createTable(curr['cc'], 'DATE DATE PRIMARY KEY, RATE DECIMAL')
                    newTables += f'\n{curr["cc"]}'
                if loader.db.isExist('date', curr['cc'], f"'{today}'"):
                    loader.db.update(curr['cc'], 'rate', curr['rate'], f"date='{today}'")
                else:
                    loader.db.insert(curr['cc'], f"'{today}', {curr['rate']}")
    logging.info('Currency rate are updated')
    if newTables != '':
        logging.info(f"List of created tables:{newTables}")


def getIndicatedCurrency():
    data = loader.db.getCurrencyList(onlyName=True)
    returnDict = {}
    mainCurrencyList = ('USD', 'EUR', 'RUB')
    for curr in data:
        if curr in mainCurrencyList:
            if curr == 'RUB':
                returnDict[curr] = 4
            else:
                returnDict[curr] = 5
        else:
            returnDict[curr] = 1
    return dict(sorted(returnDict.items(), key=operator.itemgetter(1), reverse=True))


def getMeasure(currency):
    if currency in ['XAU', 'XAG', 'XPT', 'XPD']:
        measure = '(тройская унция)'
    else:
        measure = '(единиц)'
    return measure


def getUsersMarkup(db, returnNumber=False):
    usersList = db.getFromDB('users', 'id', '1=1')
    if returnNumber:
        return usersList.__len__()
    else:
        markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        markup.add(types.KeyboardButton('Назад ⬅'))
        for elem in usersList:
            markup.add(types.KeyboardButton(elem[0]))
        return markup
