import requests
from aiogram.dispatcher import FSMContext

from classes.Book import Book
from loader import dp
from aiogram import types
from lxml import html
from states.states_list import BookSearch


@dp.message_handler(content_types='text', text='Поиск книг')
async def openBookSearchMenu(message: types.Message):
    await message.answer('Введите назвние книги')
    await BookSearch.bookMenu.set()


@dp.message_handler(content_types='text', state=BookSearch.bookMenu)
async def searchBook(message: types.Message, state: FSMContext):
    whatSearch = message.text.replace(" ", "+")
    url = f"http://flibusta.site/booksearch?ask={whatSearch}"
    res = requests.get(url)
    parsed_body = html.fromstring(res.text)
    bookResult = parsed_body.xpath("//div[@class='clear-block' and @id='main']//a[contains(@href, '/b/')]")
    bookFormats = ['read', 'fb2', 'epub', 'mobi', 'download']
    i = 0
    bookList = {}
    for elem in bookResult:
        bookId = elem.xpath('@href')[0]
        if elem.xpath('span/text()').__len__() == 0:
            name = f"{' '.join(elem.xpath('b/text()'))} {' '.join(elem.xpath('text()')).strip()}"
        else:
            name = f"{' '.join(elem.xpath('span/text()'))} {' '.join(elem.xpath('text()')).strip()}"
        bookUrl = f"http://flibusta.is{elem.xpath('@href')[0]}"
        bookRes = requests.get(bookUrl)
        author = elem.xpath('../a[2]/text()')
        book_parsed = html.fromstring(bookRes.text)
        dateAdd = book_parsed.xpath("//following-sibling::text()[contains(., 'обавлена')]")
        formats = []
        for link in bookFormats:
            if book_parsed.xpath(f'//a[contains(@href, "{bookId}/{link}")]').__len__() > 0:
                formats.append(f"http://flibusta.is{bookId}/{link}")
        bookList[i] = Book(name, author[0], dateAdd[0], bookUrl, '', formats)
        i += 1
    1==1
