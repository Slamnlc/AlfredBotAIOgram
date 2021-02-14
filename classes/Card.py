

class Card:

    def __init__(self):
        self.number: int = 0
        self.totalPrice: int = 0
        self.items: dict = {}

    def addItem(self, itemId, sqlId, name, weight, price, productType):
        self.items[itemId] = CardItem(itemId, sqlId, name, weight, price, productType)
        self.totalPrice += price
        self.number += 1

    def delete(self, itemId):
        self.items.pop(itemId)

    def isInCard(self, item):
        if type(item) == int:
            return item in self.items
        else:
            numb = -1
            for elem in self.items:
                if self.items[elem].name == item:
                    numb = elem
                    break
            return numb

    def addQuantity(self, itemId):
        self.items[itemId].quantity += 1
        self.number += 1
        self.totalPrice += self.items[itemId].price

    def delQuantity(self, itemId):
        self.items[itemId].quantity -= 1
        self.number -= 1
        self.totalPrice -= self.items[itemId].price


class CardItem:

    def __init__(self, itemId, sqlId, name, weight, price, productType, quantity=1):
        self.itemId: int = itemId
        self.sqlId: int = sqlId
        self.name: str = name
        self.weight = weight
        self.price: int = price
        self.productType = productType
        self.quantity = quantity
