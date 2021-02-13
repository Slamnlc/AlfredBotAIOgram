import json
import operator
from service.functions.text_function import convertToUser, convertToAdd
from loader import db


class User:

    def __init__(self, userID):
        if db.isExist('id', 'users', userID):
            data = convertToUser(db.getFromDB('users', '*', f"id={userID}"))
        else:
            data = db.addUser(userID)

        self.id = userID
        self.location = data['location']
        self.currency = data['currency']
        self.currencyPriority = data['currencyPriority']
        self.userCurrency = data['mainCurrency']
        self.dayForShow = data['dayForShow']

    def getUsedCurrency(self):
        data = db.getCurrencyList()
        listOfCurrency = None
        for curr in self.userCurrency:
            if listOfCurrency is None:
                listOfCurrency = f"{curr} {data[curr]['Emoji']}"
            else:
                listOfCurrency = f"{listOfCurrency}, {curr} {data[curr]['Emoji']}"
        return listOfCurrency

    def setCurrency(self, currency):
        self.currency = currency
        db.update('users', 'currency', f"'{currency}'", f"id={self.id}")

    def addCurrencyUse(self, currency):
        self.currencyPriority[currency] += 1
        self.currencyPriority = dict(sorted(self.currencyPriority.items(), key=operator.itemgetter(1), reverse=True))
        li = json.dumps(self.currencyPriority)
        db.update('users', 'currencypriority', f"'{li}'::json", f"id={self.id}")

    def setDayForShow(self, numberForShow):
        self.dayForShow = numberForShow
        db.update('users', 'dayforshow', numberForShow, f"id={self.id}")

    def setUserCurrency(self, userCurrency):
        self.userCurrency = userCurrency
        db.update('users', 'maincurrency', f"ARRAY[{userCurrency}]", f"id={self.id}")

    def getMainCity(self):
        result = db.getFromDB('users', 'citylist.*', f'users.id={self.id}',
                              'JOIN citylist ON citylist.id = users.location')
        return result[0][1].title()

    def getSearchQuery(self):
        data = db.getFromDB('citylist', '*', f"id={self.location}")[0]
        return convertToAdd(data)

    def setMainCity(self, cityLink):
        idCity = db.getFromDB('citylist', 'id', f"link='{cityLink}'")[0][0]
        self.location = idCity
        db.update('users', 'location', idCity, f'id={self.id}')

    def dictUserCurrency(self):
        data = {}
        for currency in self.userCurrency:
            data[currency] = 2
        return data
