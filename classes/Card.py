

class Card:

    def __init__(self):
        self.number: int = 0
        self.totalPrice: int = 0
        self.items: dict = {}

    def addItem(self, itemId, name, weight, price):
        self.items[itemId] = CardItem(itemId, name, weight, price)
        self.totalPrice += price
        self.number += 1

    def delete(self, itemId):
        self.items.pop(itemId)

    def isInCard(self, itemId):
        return itemId in self.items


class CardItem:

    def __init__(self, itemId, name, weight, price, quantity=1):
        self.itemId: int = itemId
        self.name: str = name
        self.weight = weight
        self.price: int = price
        self.quantity = quantity
