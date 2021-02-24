import asyncio
import logging

from scripts.messages.sendMessages import startSchedule
from utils.set_bot_commands import set_default_commands, clear_all_commands


async def on_startup(dp):
    import filters
    filters.setup(dp)

    from utils.notify_admins import on_startup_notify
    await on_startup_notify(dp)
    await clear_all_commands(dp)
    await set_default_commands(dp)
    logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
    asyncio.create_task(startSchedule())


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
