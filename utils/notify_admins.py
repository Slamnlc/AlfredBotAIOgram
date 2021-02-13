import logging

from aiogram import Dispatcher

from data.config import ADMINS
from keyboard.markup import mainMarkup


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, 'Бот запущен и готов к работе', reply_markup=mainMarkup())
        except Exception as err:
            logging.exception(err)
