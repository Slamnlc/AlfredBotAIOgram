import json
import locale
from datetime import date, datetime
from time import strptime

from aiogram.dispatcher import FSMContext
from googletrans import Translator
import requests
from lxml import html
from loader import db
from service.functions.text_function import convertToAdd, replaceNumberToEmoji, convertCityName, \
    addWeatherEmoji


def searchCities(city):
    city = ' '.join(city.replace('ё', 'е').replace('-', ' ').lower().split())
    data = db.getFromDB('citylist', '*', f"lower(name) LIKE '{city}%'", orderBy='ORDER BY maincity DESC')

    if data.__len__() == 0:
        data = db.getFromDB('citylist', '*', f"lower(name) LIKE '{city.replace('и', 'ы')}%'",
                            orderBy='ORDER BY maincity DESC')

    returnList = []

    for elem in data:
        returnList.append(convertToAdd(elem))

    return returnList


def translate(st):
    sp = st.split(' ')
    translator = Translator()
    for i in range(sp.__len__()):
        sp[i] = translator.translate(sp[i], dest='ru').text
    return ' '.join(sp)


def getLocation(location):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&uselang=ru_RU&" \
          f"lat={location.latitude}&lon={location.longitude}"
    res = requests.get(url)
    respJson = json.loads(res.text)

    distinct = ''
    if 'address' in respJson:
        if 'city' in respJson['address']:
            cityName = translate(respJson['address']['city']).lower().replace('-', ' ')
        elif 'town' in respJson['address']:
            cityName = translate(respJson['address']['town']).lower().replace('-', ' ')
        elif 'village' in respJson['address']:
            cityName = translate(respJson['address']['village']).lower().replace('-', ' ')
        else:
            cityName = ''
            distinct = translate(respJson['address']['county']).lower().replace('-', ' ')
        region = translate(respJson['address']['state']).lower().replace('-', ' ')

    else:
        cityName = translate(respJson['city']).lower().replace('-', ' ')
        region = ''

    if cityName == '':
        cityList = [db.getFromDB('citylist', '*', f"dist like'%{distinct}%'")[0]]
        if cityList[0][5]:
            cityList = [cityList[0]]
    else:
        cityName = convertCityName(cityName)
        cityList = db.getFromDB('citylist', '*', f"name='{cityName}'")

    if cityList.__len__() > 1:
        cityList = db.getFromDB('citylist', '*', f"name='{cityName}' AND REGION like '%{region}%'")
        if cityList.__len__() > 1:
            distinct = translate(respJson['address']['county']).lower().replace('-', ' ')
            cityList = db.getFromDB('citylist', '*', f"name = '{cityName}' AND REGION = '{region}' "
                                                     f"AND DIST = '{distinct}'")
    elif cityList.__len__() == 0:
        cityList = db.getFromDB('citylist', '*', f"name LIKE'%{cityName}%' AND REGION = '{region}'")

    returnList = []
    for elem in cityList:
        returnList.append(convertToAdd(elem))

    return returnList


async def getWeather(cityElem, state: FSMContext = None):
    locale.setlocale(locale.LC_TIME, "ru_RU")
    res = requests.get(cityElem[1])
    parsed_body = html.fromstring(res.text)
    minTemp = parsed_body.xpath('//div[contains(@class,"min")]/span/text()')
    maxTemp = parsed_body.xpath('//div[contains(@class,"max")]/span/text()')
    weatherType = parsed_body.xpath('//div[contains(@class,"weatherIco")]/@title')
    timeTr = parsed_body.xpath('//tr[contains(@class, "gray time")]/td/text()')
    weatherTime = parsed_body.xpath('//tr[contains(@class, "img weatherIcoS")]//div/@title')
    tempNow = parsed_body.xpath('//tr[contains(@class, "temperature")]/td/text()')
    feelLike = parsed_body.xpath('//tr[contains(@class, "temperatureSens")]/td/text()')
    dayLight = parsed_body.xpath('//div[contains(@class, "infoDaylight")]/span/text()')

    i = 0
    for i in range(timeTr.__len__()):
        if datetime.now().hour < strptime(timeTr[i].split(' ')[0], '%H').tm_hour:
            break

    tempAtNow = replaceNumberToEmoji(tempNow[i])
    feel = replaceNumberToEmoji(feelLike[i])
    weatherAtNow = replaceNumberToEmoji(weatherTime[i])

    minTemp[0] = replaceNumberToEmoji(minTemp[0])
    maxTemp[0] = replaceNumberToEmoji(maxTemp[0])

    whatReturn = f"Погода в {cityElem[0]}🏙️\n{date.today().strftime('%d %B')}\n" \
                 f"Мин.: {minTemp[0]} Макс.: {maxTemp[0]}\n" \
                 f"{weatherType[0]} \n" \
                 f"Восход 🌅: {dayLight[0]}. Заход 🌇: {dayLight[1]}\n\n" \
                 f"Сейчас: {tempAtNow}. {weatherAtNow}. Чувствуется как {feel}"

    if not state is None:
        await state.set_data(
            {
                'min': minTemp[1:],
                'max': maxTemp[1:],
                'type': weatherType[1:]
            }
        )

    return addWeatherEmoji(whatReturn)
