from aiogram.dispatcher import FSMContext, Dispatcher


from loader import db


def convertToUser(st):
    st = st[0]
    if st[4] is None:
        mainCurrency = None
    else:
        mainCurrency = st[4][0]
    user = {
        'id': st[0],
        'location': st[1],
        'currency': st[2],
        'currencyPriority': st[3],
        'mainCurrency': mainCurrency,
        'dayForShow': st[5],
    }
    return user


def convertToAdd(elem):
    if elem[5]:
        return [elem[1].title(), elem[4], elem[5]]
    else:
        if elem[3] is None:
            return [f"{elem[1].title()}, {elem[2].title()}", elem[4], elem[5]]
        else:
            return [f"{elem[1].title()}, {elem[2].title()}, {elem[3].title()}", elem[4], elem[5]]


def replaceList(strToReplace, oldText, newText):
    for i in range(oldText.__len__()):
        strToReplace = strToReplace.replace(oldText[i], newText[i])
    return strToReplace


def replaceNumberToEmoji(txt):
    oldText = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    newText = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣']
    return replaceList(txt, oldText, newText)


def addSymbolToString(st, word, symbols):
    sp = st.strip().split(' ')
    for i in range(sp.__len__()):
        if word.lower() in sp[i].lower():
            sp[i] += symbols
    return ' '.join(sp)


def addWeatherEmoji(st: str):
    weatherFrom = ['облачно', 'снег', 'дождь', 'ясно', 'гроза']
    weatherTo = ['☁️', '❄️️', '🌧️', '☀️', '⚡']
    for i in range(weatherFrom.__len__()):
        st = addSymbolToString(st, weatherFrom[i], weatherTo[i])
    return st


def addYapEmoji(st: list):
    what = ['моцарелла', 'томат', 'помидор', 'яйцо', 'куриц', 'креветк', 'перец', 'лук', 'колба', 'оливк', 'мидии',
            'рис', 'нори', 'краб', 'сыр', 'телятина', 'огурец', 'капуста', 'микрогрин', 'лосос', 'манго', 'салат',
            'икра', 'семян', 'соус', 'авокадо', 'миндал', 'филадельфия', 'каракатиц', 'угорь', 'кунжут', 'чука',
            'айсберг', 'гуакамоле', 'кукуруз', 'кинза', 'курин', 'ветчина', 'рыба', 'васаби', 'масаго', 'майонез',
            'тобико', 'яблоко', 'морковь', 'груша', 'такуан', 'горбуша', 'харусаме', 'сурими', 'кальмар', 'масляная',
            'тесто', 'говядин', 'корнишон', 'камамбер', 'балык', 'салями', 'фасоль', 'маслины', 'ананас', 'бекон',
            'пармезан', 'шпинат', 'пепперони', 'чеснок', 'орегано', 'орех', 'масло', 'крем', 'свинин', 'миди', 'лимон',
            'зелень', 'чеддер', 'дор-блю', 'тунца', 'бобы', 'кешью', 'начос', 'малина', 'буль', 'лапша', 'утка',
            'шиитаке', 'лайм', 'мята', 'ростк', 'кокосовое молоко', 'вакаме', 'имбир', 'паста', 'горох', 'тофу',
            'водоросли', 'шисо', 'фета', 'сливки', 'петрушка',
            'опята', 'шампиньон', 'гриб']
    how = ['🧀', '🍅', '🍅', '🥚', '🍗', '🦐', '🌶️', '🧅', '🥓', '🫒', '🦪',
           '🍚', '🍘', '🦀', '🧀', '🐄', '🥒', '🥬', '🌱', '🍣', '🥭', '🥬',
           '- ', '- ', '- ', '🥑', '🥜', '🧀', '🦑', '🐟', '- ', '🥬',
           '🥬', '🥑', '🌽', '🌱', '🍗', '🐖', '🐟', '🫑', '- ', '- ',
           '- ', '🍏', '🥕', '🍐', '- ', '🐟', '- ', '- ', '🦑', '🐟',
           '🥟', '🐄', '🥒', '🧀', '🐖', '🥓', '- ', '🫒', '🍍', '🐖',
           '🧀', '🌱', '🌶🥓️', '🧄', '🌱', '🥜', '- ', '- ', '🐖', '🦪', '🍋',
           '🌱', '🧀', '🧀', '🐟', '- ', '🥜', '- ', '- ', '🍲', '🍜', '🦆',
           '- ', '- ', '🌱', '🌱', '🥥🥛', '🌱', '- ', '🍝', '- ', '🧀',
           '🌱', '🌱', '🧀', '- ', '🌱',
           '- ',  '- ',  '- ']
    if st.__len__() == 1:
        return ''
    else:
        for i in range(st.__len__()):
            for ii in range(what.__len__()):
                if what[ii] in st[i].lower():
                    st[i] = how[ii] + st[i]
                    break
            st[i] = st[i].title()
        return st


def is_Digit(val):
    if val.isdigit():
        return True
    else:
        try:
            float(val)
            return True
        except ValueError:
            return False


def multiReplace(strToReplace, valuesForReplace):
    for y in valuesForReplace:
        strToReplace = strToReplace.replace(y, '')
    return strToReplace


async def getCurrentState(state: FSMContext):
    st = await state.get_state()
    return st.split(':')[1]


def convertCityName(cityName):
    bad = ['змеев', 'борова']
    ok = ['змиев', ',боровая']
    for i in range(bad.__len__()):
        cityName = cityName.replace(bad[i], ok[i])
    return cityName


def getFlag(currency):
    data = db.getFromDB('currency', 'emoji', f"name='{currency}'")
    return data[0][0]


async def sendKeanu(dp: Dispatcher, chatId):
    await dp.bot.send_animation(chatId, 'https://media.giphy.com/media/hv4TC2Ide8rDoXy0iK/giphy-downsized.gif')


async def getTableName(itemName: str):
    if itemName == 'Суши 🍣':
        return 'sushi'
    elif itemName == 'Роллы🍣':
        return 'rolly'
    elif itemName == 'Сеты🍱':
        return 'sety'
    elif itemName == 'Royal👑':
        return 'royal'
    elif itemName == 'Спринг-ролы🍣':
        return 'spring_rolly'
    elif itemName == 'Круглая🟠':
        return 'kruglaja'
    elif itemName == 'Party пицца🎉':
        return 'metrovaja'
    elif itemName == 'Боулы и поке🥣':
        return 'bouly'
    elif itemName == 'От Шефа🧑‍🍳':
        return 'osoboe'
    elif itemName == 'Супы🍲':
        return 'supy'
