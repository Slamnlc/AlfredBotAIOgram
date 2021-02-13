from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from classes.Card import Card
from keyboard.inline.callback_data import ph_callback
from keyboard.yaposka_markup import mainYapMarkup, allItemsMenu, changePhotoMarkup
from loader import dp, yap_db
from aiogram import types

from service.functions.text_function import addYapEmoji
from states import Yap


async def sendNewPhoto(message: types.Message, state: FSMContext, newPhoto, fromShow=False):
    data = await state.get_data()
    mainSet = yap_db.getFromDB(data['table'], '*', f'position={newPhoto}')
    data['current'] = newPhoto
    name = mainSet[0][1]
    weight = mainSet[0][2]
    price = mainSet[0][6]
    if data['table'] == 'sety':
        items = '🍣' + '\n🍣'.join(mainSet[0][3][0])
    elif type(mainSet[0][3][0]) == str:
        items = mainSet[0][3][0].title()
    else:
        items = '\n'.join(addYapEmoji(mainSet[0][3][0]))
    txt = f"{data['productType']}: <b>{name}</b>\n" \
          f"Вес: <b>{weight}</b>\n" \
          f"Цена: <b>{price} грн</b>\n\n" \
          f"{items}"
    if fromShow:
        await message.delete()
        await dp.bot.send_photo(message.chat.id, photo=mainSet[0][5], caption=txt,
                                reply_markup=changePhotoMarkup(), parse_mode='HTML')
    else:
        card: Card = data['card']
        if card.isInCard(mainSet[0][0]):
            markup = changePhotoMarkup(card.items[mainSet[0][0]].quantity)
        else:
            markup = changePhotoMarkup()
        await message.edit_media(types.input_media.InputMediaPhoto(mainSet[0][5]))
        await message.edit_caption(caption=txt, reply_markup=markup, parse_mode='HTML')
    await state.set_data(data)


@dp.callback_query_handler(ph_callback.filter(do=['back', 'go']), state=Yap.showPhotos)
async def changePhoto(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    currentPhoto = data['current']
    recordNumber = yap_db.getFromDB(data['table'], 'COUNT(id)', '1=1')[0][0]
    if callback_data['do'] == 'go':
        if currentPhoto + 1 > recordNumber:
            newPhoto = 1
        else:
            newPhoto = currentPhoto + 1
    else:
        if currentPhoto - 1 != 0:
            newPhoto = currentPhoto - 1
        else:
            newPhoto = recordNumber
    await sendNewPhoto(call.message, state, newPhoto)


@dp.callback_query_handler(ph_callback.filter(do='menuBack'), state=[Yap.showPhotos, Yap.subMenu])
async def changePhoto(call: CallbackQuery):
    await call.message.delete()
    await call.message.answer("Выберите категорию", reply_markup=mainYapMarkup())
    await Yap.yapMainMenu.set()


@dp.callback_query_handler(ph_callback.filter(do='showAll'), state=[Yap.showPhotos, Yap.subMenu])
async def changePhoto(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    if data['table'] in ['rolly', 'royal', 'sety']:
        quantity = ', quantity'
    else:
        quantity = ''
    itemsList = yap_db.getFromDB(data['table'], f'name, weight, price, position{quantity}', '1=1',
                                 orderBy='ORDER BY POSITION')
    await call.message.answer('Выберите блюдо', reply_markup=allItemsMenu(itemsList, quantity))


@dp.callback_query_handler(ph_callback.filter(do='addToCart'), state=Yap.showPhotos)
async def changePhoto(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data['table'] in ['rolly', 'royal', 'sety']:
        quantity = ', quantity'
    else:
        quantity = ''
    itemsList = yap_db.getFromDB(data['table'], f'id, name, weight, price{quantity}', f"position={data['current']}")
    card: Card = data['card']
    card.addItem(itemsList[0][0], itemsList[0][1], itemsList[0][2], itemsList[0][3])
    data['card'] = card
    await state.set_data(data)
    await call.message.edit_reply_markup(changePhotoMarkup(1))


@dp.callback_query_handler(ph_callback.filter(do=['addQuantity', 'minus']), state=Yap.showPhotos)
async def changePhoto(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    itemId = yap_db.getFromDB(data['table'], 'id', f'position={data["current"]}')[0][0]
    card: Card = data['card']

    if callback_data['do'] == 'addQuantity':
        card.items[itemId].quantity += 1
    else:
        if card.items[itemId].quantity > 1:
            card.items[itemId].quantity -= 1
        else:
            card.delete(itemId)
            itemId = -1

    if itemId == -1:
        markup = changePhotoMarkup()
    else:
        markup = changePhotoMarkup(card.items[itemId].quantity)

    await state.update_data(card=card)
    await call.message.edit_reply_markup(reply_markup=markup)
