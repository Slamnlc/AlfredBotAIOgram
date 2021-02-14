from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from classes.Card import Card
from keyboard.inline.callback_data import ph_callback
from service.functions.text_function import replaceNumberToEmoji


def changePhotoMarkup(quantity=0):
    markup = InlineKeyboardMarkup(row_width=6)

    button1 = InlineKeyboardButton(text='⬅️', callback_data=ph_callback.new(do='back'))
    button2 = InlineKeyboardButton(text="➡️", callback_data=ph_callback.new(do='go'))

    markup.add(button1, button2)

    if quantity == 0:
        markup.add(InlineKeyboardButton(text='Добавить в корзину 🛒', callback_data=ph_callback.new(do='addToCart')))
    else:
        markup.add(InlineKeyboardButton(text=f'Добавлено {replaceNumberToEmoji(quantity)}',
                                        callback_data=ph_callback.new(do='None')))
        markup.add(InlineKeyboardButton(text='➖ кол-во', callback_data=ph_callback.new(do='minus')))
        markup.insert(InlineKeyboardButton(text='➕ кол-во', callback_data=ph_callback.new(do='addQuantity')))

    markup.add(InlineKeyboardButton(text='Список блюд', callback_data=ph_callback.new(do='showAll')))
    markup.insert(InlineKeyboardButton(text='К категориям ⬅', callback_data=ph_callback.new(do='menuBack')))

    return markup


def mainYapMarkup():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    markup.add(KeyboardButton('Назад ⬅'))
    markup.add(KeyboardButton('Корзина 🛒'))
    markup.add(KeyboardButton('Суши🍣'))
    markup.add(KeyboardButton('Пицца🍕'))
    markup.add(KeyboardButton('Боулы и поке🥣'))
    markup.add(KeyboardButton('От Шефа🧑‍🍳'))
    markup.add(KeyboardButton('Супы🍲'))

    return markup


def sushiMenu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    markup.add(KeyboardButton('Назад ⬅'))
    markup.add(KeyboardButton('Сеты🍱'))
    markup.add(KeyboardButton('Роллы🍣'))
    markup.add(KeyboardButton('Суши 🍣'))
    markup.add(KeyboardButton('Royal👑'))
    markup.add(KeyboardButton('Спринг-ролы🍣'))

    return markup


def pizzaMenu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    markup.add(KeyboardButton('Назад ⬅'))
    markup.add(KeyboardButton('Круглая🟠'))
    markup.add(KeyboardButton('Party пицца🎉'))

    return markup


def allItemsMenu(itemsList: list, quantity: str):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    markup.add(KeyboardButton('Назад ⬅'))
    markup.add(KeyboardButton('Сортировать по'))
    markup.add(KeyboardButton('🔤'))
    markup.insert(KeyboardButton('💲'))
    markup.insert(KeyboardButton('⚖️'))

    if quantity != '':
        markup.insert(KeyboardButton('🍣🔢'))

    for item in itemsList:
        if quantity != '':
            text = f"{(item[0].title())} | {item[1]} | {item[4]} шт. | {item[2]} грн."
        else:
            text = f"{item[0].title()} | {item[1]} | {item[2]} грн."
        markup.add(KeyboardButton(text=text))
    return markup


def showCardMarkup(card: Card):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=4)
    markup.add(KeyboardButton('Назад ⬅'))
    markup.add(KeyboardButton(f"Сумма: {card.totalPrice} грн"))
    markup.insert(f"Блюд: {card.number}")
    for item in card.items:
        markup.add(f"{card.items[item].name.title()} | Кол-во: {card.items[item].quantity}")
    return markup
