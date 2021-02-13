from aiogram import Dispatcher
from filters.general import IsNumber, IsFood
from filters.currency_flags import IsCurrency


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsNumber)
    dp.filters_factory.bind(IsCurrency)
    dp.filters_factory.bind(IsFood)