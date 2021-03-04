from datetime import datetime, date

import aioschedule as schedule
import asyncio
from loader import dp, db
from service.functions.currency_function import addCurrencyInfo, getTodayRate
from service.functions.wheather_function import getWeather


async def sendMainInfo():
    now = datetime.now()
    checkTime = f"{now.hour}:{now.minute}"
    users = db.getFromDB('users', 'id, location, maincurrency', f"notify = '{checkTime}'")
    if users.__len__() != 0:
        for user in users:
            if not user[1] is None:
                city = db.getFromDB('citylist', 'name, link', f"id={user[1]}")
                whether = await getWeather(city[0])
            else:
                whether = ''
            rate: str = 'Курс валют:\n'
            if not user[2] is None:
                data = db.getCurrencyList()
                for currency in user[2][0]:
                    if db.getFromDB(currency, 'rate', f"date='{date.today()}'").__len__() == 0:
                        await addCurrencyInfo(100)
                    rate += f"{data[currency]['FullName']} {data[currency]['Emoji']}: {getTodayRate(currency)}\n"
            else:
                rate = ''
            if rate == '' and whether == '':
                pass
            else:
                if whether == '':
                    txt = rate
                else:
                    if 'дождь' in whether.lower():
                        whether += '\nНе забудьте взять зонтик☂️'
                    txt = f"{whether}\n\n{rate}"
                if now.hour < 6:
                    hiMessage = 'Доброй ночи🌃\n\n'
                elif 6 <= now.hour < 9:
                    hiMessage = 'Доброе утро🌅\n\n'
                elif 9 <= now.hour <= 19:
                    hiMessage = 'Добрый день☀️\n\n'
                else:
                    hiMessage = 'Добрый вечер🌆️\n\n'

                await dp.bot.send_message(user[0], hiMessage + txt)


async def startSchedule():
    schedule.every(1).minute.do(sendMainInfo)
    schedule.every().day.at("18:00").do(addCurrencyInfo, 10)
    schedule.every().day.at("22:00").do(addCurrencyInfo, 10)
    schedule.every().day.at("06:00").do(addCurrencyInfo, 50)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)
