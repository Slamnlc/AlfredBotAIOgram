from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from classes.sql import crete_connection, create_yaposhka
from data.config import TOKEN
1==1
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
db = crete_connection()
yap_db = create_yaposhka()
dp = Dispatcher(bot, storage=storage)
