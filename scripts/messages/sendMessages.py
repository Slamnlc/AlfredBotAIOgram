import aioschedule as schedule
import asyncio
from loader import dp
from data.config import ADMINS
from service.functions.currency_function import addCurrencyInfo


async def job():
    for admin in ADMINS:
        await dp.bot.send_message(admin, 'Ну шо? Я настроил')


async def startSchedule():
    # schedule.every(30).seconds.do(job)
    schedule.every().day.at("18:00").do(addCurrencyInfo, 5)
    schedule.every().day.at("22:00").do(addCurrencyInfo, 5)
    schedule.every().day.at("06:00").do(addCurrencyInfo, 5)
    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)
