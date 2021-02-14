from aiogram.dispatcher import FSMContext

from classes.Card import Card
from handlers.users.inline_handlers.yaposhka_inline import sendNewPhoto
from keyboard.yaposka_markup import mainYapMarkup, sushiMenu, pizzaMenu, allItemsMenu, showCardMarkup
from loader import dp, yap_db
from aiogram import types

from service.functions.text_function import getTableName, deleteMessages
from states import Yap


@dp.message_handler(content_types='text', text='Test')
async def openSettingsMenu(message: types.Message, state: FSMContext):
    await message.delete()
    await message.answer("Выберите категорию", reply_markup=mainYapMarkup(), disable_notification=True)
    await Yap.yapMainMenu.set()
    data = {
            'current': 1,
            'table': '',
            'card': Card(),
            'productType': message.text,
            'order': 'asc',
            'startId': message.message_id
        }
    await state.set_data(data)


@dp.message_handler(content_types='text', text=['Суши 🍣', 'Роллы🍣', 'Сеты🍱', 'Royal👑', 'Спринг-ролы🍣', 'Круглая🟠',
                                                'Party пицца🎉', 'Боулы и поке🥣', 'От Шефа🧑‍🍳', 'Супы🍲'],
                    state=[Yap.yapMainMenu, Yap.subMenu, Yap.showPhotos])
async def showProductsPhoto(message: types.Message, state: FSMContext):
    tableName = await getTableName(message.text)
    await Yap.showPhotos.set()
    data = await state.get_data()
    data['current'] = 1,
    data['table'] = tableName
    data['productType'] = message.text
    await state.set_data(data)
    await sendNewPhoto(message, state, 1, True)


@dp.message_handler(content_types='text', text='Суши🍣', state=Yap.yapMainMenu)
async def showSushiMenu(message: types.Message):
    await message.answer('Выберите подкатегорию', reply_markup=sushiMenu(), disable_notification=True)
    await message.delete()
    await Yap.subMenu.set()


@dp.message_handler(content_types='text', text='Пицца🍕', state=Yap.yapMainMenu)
async def showSushiMenu(message: types.Message):
    await message.answer('Выберите подкатегорию', reply_markup=pizzaMenu(), disable_notification=True)
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
    await message.answer(f'Отсортировано по {txt}', reply_markup=allItemsMenu(query, quantity),
                         disable_notification=True)


@dp.message_handler(content_types='text', text='Корзина 🛒', state=Yap)
async def showCard(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if data.__len__() == 0:
        data['card'] = Card()
    await message.answer('Ваша корзина:', reply_markup=showCardMarkup(data['card']), disable_notification=True)
    await Yap.card.set()


@dp.message_handler(content_types='text', state=Yap.showPhotos)
async def showItem(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    if 'Назад' in message.text:
        await deleteMessages(message.message_id, message.chat.id, state)
        await message.answer('Выберите категорию', reply_markup=mainYapMarkup(), disable_notification=True)
        await Yap.yapMainMenu.set()
        return
    txt = message.text.split('|')[0].lower().strip()
    if data['table'] in ['rolly', 'royal', 'sety']:
        quantity = ', quantity'
    else:
        quantity = ''

    result = yap_db.getFromDB(data['table'], f'name, weight, price, position{quantity}',
                              where=f"name = '{txt}'", orderBy='ORDER BY POSITION')
    if result.__len__() == 0:
        result = yap_db.getFromDB(data['table'], f'name, weight, price, position{quantity}',
                                  where=f"name like '%{txt}%'", orderBy='ORDER BY POSITION')
    if result.__len__() == 0:
        await message.answer('Не могу найти блюдо с таким названием 😔')
    elif result.__len__() == 1:
        await sendNewPhoto(message, state, result[0][3], True)
    else:
        await dp.bot.delete_message(message.chat.id, message.message_id - 1)
        await message.answer('Выберите блюдо', reply_markup=allItemsMenu(result, quantity), disable_notification=True)
