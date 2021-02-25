from aiogram import types
from aiogram.types import CallbackQuery

from classes.User import User
from filters import IsBack
from keyboard.markup import settingsMarkup
from loader import dp
from states import SettingsState


@dp.callback_query_handler(IsBack(), state=SettingsState.setNotifyTime)
async def backFromSetNotify(call: CallbackQuery):
    await call.message.delete()
    await SettingsState.settingsMenu.set()
    user = User(call.from_user.id)
    msg = await call.message.answer('Закрываю настройку времени уведомлений', reply_markup=types.ReplyKeyboardRemove())
    await msg.delete()

    await call.message.answer('Перехожу в настройки', reply_markup=settingsMarkup(user))
