from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified
from keyboard.currency_markups import mainCurrencyMarkup, currencyMarkup
from keyboard.inline.callback_data import numeric_callback
from loader import dp
from classes.User import User
from service.functions.currency_function import getTodayRate
from service.functions.text_function import is_Digit
from states import CurrencyState


def calculateCurrency(markup, currentResult):
    currencyFrom = markup.inline_keyboard[1][0].text.split(' - ')[1]
    currencyTo = markup.inline_keyboard[1][1].text.split(' - ')[1]
    if currencyFrom != currencyTo:
        if currencyFrom == 'UAH':
            rateForCurrency = float(getTodayRate(currencyTo) * float(currentResult))
        elif 'UAH' != currencyFrom and currencyTo != 'UAH':
            rateForCurrency = (float(getTodayRate(currencyFrom) * float(currentResult))) \
                              / float(getTodayRate(currencyTo))
        else:
            rateForCurrency = float(getTodayRate(currencyFrom)) * float(currentResult)
    else:
        rateForCurrency = currentResult
    return f'{currentResult} {currencyFrom} = {round(float(rateForCurrency), 2)}'


@dp.callback_query_handler(numeric_callback.filter(item_name=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']),
                           state=CurrencyState.selectCurrencyFrom)
async def setValue(call: CallbackQuery, callback_data: dict):
    currentResult = call.message.reply_markup.inline_keyboard[2][0].text
    whatAdd = callback_data['item_name']
    if currentResult == 'Результат':
        if whatAdd == '0':
            currentResult = ''
        else:
            currentResult = ''
    else:
        currentResult = currentResult.split(' ')[0]
    currentResult = f"{currentResult}{whatAdd}"
    if is_Digit(currentResult):
        returnVal = calculateCurrency(call.message.reply_markup, currentResult)
        try:
            call.message.reply_markup.inline_keyboard[2][0].text = returnVal
            await call.message.edit_text(text=call.message.text, reply_markup=call.message.reply_markup)
        except MessageNotModified:
            pass


@dp.callback_query_handler(numeric_callback.filter(item_name='back'), state=CurrencyState.selectCurrencyFrom)
async def exitFromInline(call: CallbackQuery):
    user = User(call.from_user.id)
    currentResult = call.message.reply_markup.inline_keyboard[2][0].text
    await call.message.delete()
    if currentResult == 'Результат':
        txt = 'Открываю меню курса валют'
    else:
        txt = f"{currentResult} {call.message.reply_markup.inline_keyboard[1][1].text.split(' - ')[1]}"
    await call.message.answer(txt, reply_markup=mainCurrencyMarkup(user))
    await CurrencyState.mainMenu.set()


@dp.callback_query_handler(numeric_callback.filter(item_name='del'), state=CurrencyState.selectCurrencyFrom)
async def deleteSymbolInline(call: CallbackQuery):
    currentResult = call.message.reply_markup.inline_keyboard[2][0].text
    if currentResult != 'Результат':
        currentResult = currentResult.split(' ')[0]
        currentResult = currentResult[:-1]
        if currentResult == '' or currentResult == '0':
            currentResult = 'Результат'
        else:
            currentResult = calculateCurrency(call.message.reply_markup, currentResult)
        call.message.reply_markup.inline_keyboard[2][0].text = currentResult
        await call.message.edit_text(text=call.message.text, reply_markup=call.message.reply_markup)


@dp.callback_query_handler(numeric_callback.filter(item_name='clear'), state=CurrencyState.selectCurrencyFrom)
async def clearSymbolsInline(call: CallbackQuery):
    call.message.reply_markup.inline_keyboard[2][0].text = 'Результат'
    try:
        await call.message.edit_text(text=call.message.text, reply_markup=call.message.reply_markup)
    except MessageNotModified:
        pass


@dp.callback_query_handler(numeric_callback.filter(item_name='.'), state=CurrencyState.selectCurrencyFrom)
async def addDotInline(call: CallbackQuery):
    currentResult = call.message.reply_markup.inline_keyboard[2][0].text.split(' ')[0]
    if currentResult != 'Результат':
        if '.' in currentResult:
            return
        sp = call.message.reply_markup.inline_keyboard[2][0].text.split(' ')
        sp[0] = f"{currentResult}."
        call.message.reply_markup.inline_keyboard[2][0].text = ' '.join(sp)
        await call.message.edit_text(text=call.message.text, reply_markup=call.message.reply_markup)


@dp.callback_query_handler(numeric_callback.filter(item_name='chFrom'), state=CurrencyState.selectCurrencyFrom)
async def changeCurrencyFrom(call: CallbackQuery, state: FSMContext):
    user = User(call.from_user.id)
    await call.message.delete()
    await state.set_data(
        {
            'from': call.message.reply_markup.inline_keyboard[1][0].text.split(' - ')[1],
            'to': call.message.reply_markup.inline_keyboard[1][1].text.split(' - ')[1]
        }
    )
    await call.message.answer('Из какой валюты конвертировать?', reply_markup=currencyMarkup(user))
    await CurrencyState.changeCurrencyFrom.set()


@dp.callback_query_handler(numeric_callback.filter(item_name='chTo'), state=CurrencyState.selectCurrencyFrom)
async def changeCurrencyTo(call: CallbackQuery, state: FSMContext):
    user = User(call.from_user.id)
    await call.message.delete()
    await call.message.answer('В какую валюту конвертировать?', reply_markup=currencyMarkup(user))
    await state.set_data(
        {
            'from': call.message.reply_markup.inline_keyboard[1][0].text.split(' - ')[1],
            'to': call.message.reply_markup.inline_keyboard[1][1].text.split(' - ')[1]
        }
    )
    await CurrencyState.changeCurrencyTo.set()

#     buttonDel = InlineKeyboardButton(text="Del.", callback_data=numeric_callback.new(item_name='del'))
#     buttonClear = InlineKeyboardButton(text="Clear", callback_data=numeric_callback.new(item_name='clear'))
#     buttonDot = InlineKeyboardButton(text=".", callback_data=numeric_callback.new(item_name='.'))


#     buttonFrom = InlineKeyboardButton(text=f"Из {data[fromCurrency]['Emoji']} - {fromCurrency}",
#                                       callback_data=numeric_callback.new(item_name='chFrom'))
#     buttonTo = InlineKeyboardButton(text=f"в {data[toCurrency]['Emoji']} - {toCurrency}",
#                                     callback_data=numeric_callback.new(item_name='chTo'))
