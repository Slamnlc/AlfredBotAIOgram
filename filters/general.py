from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message
from loader import yap_db


class IsNumber(BoundFilter):

    async def check(self, callback_data: dict):
        return callback_data.data.split(':')[1].isdigit()


class IsFood(BoundFilter):

    async def check(self, message: Message, state: FSMContext):
        data = await state.get_data()
        if yap_db.isExist('name', data['table'], f"%{message.text}%", like=True):
            return True
        else:
            return False


class IsFlib(BoundFilter):

    async def check(self, callback_data: dict):
        if 'flibusta.is' in callback_data.data.split(':')[1]:
            return True
        else:
            return False


class IsBack(BoundFilter):
    async def check(self, callback_data: dict):
        if callback_data.data == 'backButton':
            return True
        else:
            return False
