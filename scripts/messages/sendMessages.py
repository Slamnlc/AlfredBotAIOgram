import aioschedule as schedule
import asyncio
import time

# import data.config
from loader import dp


async def job():
    # for admin in data.config.ADMINS:
    await dp.bot.send_message(185200431, 'Ну шо? Я настроил')


if __name__ == '__main__':
    schedule.every(10).seconds.do(job)
    loop = asyncio.get_event_loop()
    while 1:
        loop.run_until_complete(schedule.run_pending())
        time.sleep(1)
