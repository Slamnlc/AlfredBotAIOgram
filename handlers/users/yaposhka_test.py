from aiogram.dispatcher import FSMContext

from classes.Card import Card
from handlers.users.inline_handlers.yaposhka_inline import sendNewPhoto
from keyboard.yaposka_markup import mainYapMarkup, sushiMenu, pizzaMenu, allItemsMenu
from loader import dp, yap_db
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
            'card': Card(),
            'productType': message.text,
            'order': 'asc'
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


@dp.message_handler(content_types='text', text=['🔤', '💲', '⚖️', '🍣🔢', 'Сортировать по'], state=Yap)
async def sortByName(message: types.Message, state: FSMContext):
    await dp.bot.delete_message(message.chat.id, message.message_id - 1)
    await message.delete()
    data = await state.get_data()

    if data['order'] == 'asc':
        data['order'] = 'desc'
    else:
        data['order'] = 'asc'
    await state.set_data(data)

    if message.text == '🔤':
        field = 'name'
        txt = 'имени'
    elif message.text == '💲':
        field = 'price'
        txt = 'цене'
    elif message.text == '⚖️':
        field = 'weight'
        txt = 'весу'
    elif message.text == '🍣🔢':
        field = 'quantity'
        txt = 'количеству'
    else:
        field = 'position'
        txt = 'порядку'

    if data['table'] in ['rolly', 'royal', 'sety']:
        quantity = ', quantity'
    else:
        quantity = ''

    query = yap_db.getFromDB(
        data['table'], f'name, weight, price, position{quantity}', '1=1', orderBy=f'ORDER BY {field} {data["order"]}')
    await message.answer(f'Отсортировано по {txt}', reply_markup=allItemsMenu(query, quantity))


@dp.message_handler(content_types='text', state=Yap.showPhotos)
async def showItem(message: types.Message, state: FSMContext):
    data = await state.get_data()
    txt = message.text.split('|')[0].lower().strip()
    if data['table'] in ['rolly', 'royal', 'sety']:
        quantity = ', quantity'
    else:
        quantity = ''

    result = yap_db.getFromDB(data['table'], f'name, weight, price, position{quantity}',
                              where=f"name like '%{txt}%'", orderBy='ORDER BY POSITION')
    if result.__len__() == 0:
        await message.delete()
        await message.answer('Не могу найти блюдо с таким названием 😔')
    elif result.__len__() == 1:
        await sendNewPhoto(message, state, result[0][3], True)
    else:
        await dp.bot.delete_message(message.chat.id, message.message_id - 1)
        await message.delete()
        await message.answer('Выберите блюдо', reply_markup=allItemsMenu(result, quantity))
