from aiogram.dispatcher import FSMContext

from keyboard.markup import bookMarkup, bookItemMarkup
from loader import dp, db
from aiogram import types
from states.states_list import BookSearch


def isNameInSearch(name: str, data: dict):
    ret = -1
    for i in range(data.__len__()):
        if data[i][1] == name:
            ret = i
            break
    return ret


@dp.message_handler(content_types='text', text='Поиск книг')
async def openBookSearchMenu(message: types.Message):
    await message.answer('Введите назвние книги')
    await BookSearch.bookMenu.set()


@dp.message_handler(content_types='text', state=BookSearch.bookMenu)
async def searchBook(message: types.Message, state: FSMContext):
    if '|' in message.text:
        show = message.text.lower().split(' |')[0]
        data = await state.get_data()
        ret = isNameInSearch(show, data)
        if ret == -1:
            await message.answer('Выберите книгу из списка результатов')
        else:
            txt = f"Книга: <b>{data[ret][1].title()}</b>\n" \
                  f"Автор: <b>{data[ret][2].title()}</b>\n\n" \
                  f"Аннотация: {data[ret][3]}"
            await message.answer(text=txt, reply_markup=bookItemMarkup(data[ret][6][0]))
    else:
        whatSearch = ' '.join(message.text.lower().split())
        data = db.getFromDB('books', '*', where=f"name like '%{whatSearch}%'",
                            orderBy='order by array_length(links,2) desc')
        if data.__len__() == 0:
            await message.answer('Ничего не нашел😥')
        else:
            await message.answer('Вот, что я нашел 📚', reply_markup=bookMarkup(data))
            await state.set_data(data)
