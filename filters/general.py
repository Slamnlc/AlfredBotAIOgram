from aiogram.dispatcher.filters import BoundFilter


class IsNumber(BoundFilter):

    async def check(self, callback_data: dict):
        return callback_data.data.split(':')[1].isdigit()