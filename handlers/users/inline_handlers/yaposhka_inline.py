from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from filters import IsNumber
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
        items = mainSet[0][3][0]
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
        await message.edit_media(types.input_media.InputMediaPhoto(mainSet[0][5]))
        await message.edit_caption(caption=txt, reply_markup=message.reply_markup, parse_mode='HTML')
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


@dp.callback_query_handler(IsNumber(), state=[Yap.showPhotos, Yap.subMenu])
async def showItem(call: CallbackQuery, state: FSMContext):
    newPhoto = int(call.data.split(':')[1])
    print(newPhoto)
    await sendNewPhoto(call.message, state, newPhoto, True)
