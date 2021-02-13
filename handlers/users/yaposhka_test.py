from aiogram.dispatcher import FSMContext

from handlers.users.inline_handlers.yaposhka_inline import sendNewPhoto
from keyboard.yaposka_markup import mainYapMarkup, sushiMenu, pizzaMenu
from loader import dp
from aiogram import types

from service.functions.text_function import getTableName
from states import Yap


@dp.message_handler(content_types='text', text='Test')
async def openSettingsMenu(message: types.Message):
    await message.delete()
    await message.answer("Выберите категорию", reply_markup=mainYapMarkup())
    await Yap.yapMainMenu.set()


@dp.message_handler(content_types='text', text=['Суши 🍣', 'Роллы🍣', 'Сеты🍱', 'Royal👑', 'Спринг-ролы🍣', 'Круглая🟠',
                                                'Party пицца🎉', 'Боулы и поке🥣', 'От Шефа🧑‍🍳', 'Супы🍲'],
                    state=[Yap.yapMainMenu, Yap.subMenu, Yap.showPhotos])
async def showProductsPhoto(message: types.Message, state: FSMContext):
    tableName = await getTableName(message.text)
    await Yap.showPhotos.set()
    await state.set_data(
        {
            'current': 1,
            'table': tableName,
            'productType': message.text
        }
    )
    await sendNewPhoto(message, state, 1, True)


@dp.message_handler(content_types='text', text='Суши🍣', state=Yap.yapMainMenu)
async def showSushiMenu(message: types.Message):
    await message.answer('Выберите подкатегорию', reply_markup=sushiMenu())
    await message.delete()
    await Yap.subMenu.set()


@dp.message_handler(content_types='text', text='Пицца🍕', state=Yap.yapMainMenu)
async def showSushiMenu(message: types.Message):
    await message.answer('Выберите подкатегорию', reply_markup=pizzaMenu())
    await message.delete()
    await Yap.subMenu.set()
