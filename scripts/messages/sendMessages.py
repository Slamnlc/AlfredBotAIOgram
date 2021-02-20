import aioschedule as schedule
import asyncio
import time

from data.config import ADMINS
from loader import dp


async def job():
    for admin in ADMINS:
        await dp.bot.send_message(admin, 'Ну шо? Я настроил')


schedule.every(10).seconds.do(job)
loop = asyncio.get_event_loop()
while 1:
    loop.run_until_complete(schedule.run_pending())
    time.sleep(1)
