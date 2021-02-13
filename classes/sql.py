import json
import psycopg2

from data.config import yaposhkaDbName, mainDbName, dbUserName, dbPassword
from service.functions.currency_function import getIndicatedCurrency


def crete_connection():
    return Database()


def create_yaposhka():
    return Database(yaposhkaDbName)
1==1

class Database:

    def __init__(self, dbName=mainDbName):
        self.connection = psycopg2.connect(
            database=dbName,
            user=dbUserName,
            password=dbPassword,
            host='127.0.0.1',
            port='5432')
        self.cursor = self.connection.cursor()
        print("Connected to database")

    def getFromDB(self, tableName, what, where, join='', orderBy=''):
        self.cursor.execute(
            f"SELECT {what.upper()} "
            f"FROM {tableName.upper()} "
            f"{join} "
            f"WHERE {where} "
            f"{orderBy}"
        )
        return self.cursor.fetchall()

    def getColumnsNames(self, tableName: str):
        self.cursor.execute(f"select column_name from information_schema.columns "
                            f"where table_name='{tableName.lower()}'")
        header = ''
        for elem in self.cursor.fetchall():
            header = f"{header},{elem[0]}"
        return header[1:]

    def insert(self, tableName: str, values: str):
        headers = self.getColumnsNames(tableName)
        quantity = headers.split(',').__len__()
        if values.split(',').__len__() == quantity:
            self.cursor.execute(f"INSERT INTO {tableName} ({headers}) VALUES ({values})")
            print(f"Data {values} successfully inserted to {tableName}")
        else:
            print(f"Total columns number ({quantity}) "
                  f"aren't equal to inserted values ({values.split(',').__len__()})"
                  f"Data aren't inserted")

    def update(self, tableName, what, how, condition):
        self.cursor.execute(f"UPDATE {tableName} SET {what} = {how} WHERE {condition}")
        self.connection.commit()

    def isExist(self, field, table, condition):
        self.cursor.execute(f"SELECT EXISTS(SELECT {field} FROM {table} WHERE {field} = {condition})")
        result = self.cursor.fetchall()[0]
        return result[0]

    def isTableExist(self, tableName: str):
        self.cursor.execute(f"SELECT count(table_name) FROM INFORMATION_SCHEMA.TABLES "
                            f"WHERE TABLE_NAME = '{tableName.lower()}'")
        result = self.cursor.fetchall()[0][0]
        if result > 0:
            return True
        else:
            return False

    def createTable(self, tableName:str, header: str):
        self.cursor.execute(f"CREATE TABLE {tableName} ({header})")
        self.connection.commit()
        print(f"Table {tableName} was successfully created")

    def getCurrencyList(self, onlyName=False):
        if onlyName:
            what = "name"
        else:
            what = '*'
        self.cursor.execute(f"SELECT {what} FROM CURRENCY WHERE 1=1")
        result = self.cursor.fetchall()
        if onlyName:
            data = []
        else:
            data = {}
        for i in range(result.__len__()):
            if onlyName:
                data.append(result[i][0])
            else:
                data[result[i][0]] = {
                    "FullName": result[i][1],
                    "Emoji": result[i][2]
                }
        return data

    def deleteUser(self, userID):
        self.cursor.execute(f"DELETE FROM USERS WHERE ID={userID}")
        self.connection.commit()
        print(f"User with id {userID} was deleted")

    def addUser(self, idUser, currency='UAH',
                mainCurrency=['EUR', 'USD'], location='NULL', currencyPriority=None, dayForShow=10):
        if currencyPriority is None:
            currencyPriority = getIndicatedCurrency()
        currencyPriority = json.dumps(currencyPriority)
        query = f"INSERT INTO USERS (ID, LOCATION, CURRENCY, CURRENCYPRIORITY, MAINCURRENCY, " \
                f"DAYFORSHOW) VALUES ({idUser}, {location}, '{currency}', " \
                f"'{currencyPriority}'::json, ARRAY[{mainCurrency}],{dayForShow})"
        self.cursor.execute(query)
        self.connection.commit()
        print(f"User with ID {idUser} was created")
        data = {
            'id': idUser,
            'location': location,
            'currency': currency,
            'currencyPriority': currencyPriority,
            'mainCurrency': mainCurrency,
            'dayForShow': dayForShow,
        }
        return data
