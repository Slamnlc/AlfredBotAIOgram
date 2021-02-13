from aiogram.types import Message
from aiogram.types.callback_query import CallbackQuery
from aiogram.dispatcher.filters import BoundFilter
from loader import db


class IsCurrency(BoundFilter):

    async def check(self, data):
        if isinstance(data, CallbackQuery):
            currency = data.data
        elif isinstance(data, Message):
            currency = data.text[:3].upper()
        return db.isExist('name', 'currency', f"'{currency}'")
