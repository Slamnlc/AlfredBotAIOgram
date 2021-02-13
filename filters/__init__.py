from aiogram import Dispatcher
from filters.general import IsNumber
from filters.currency_flags import IsCurrency


def setup(dp: Dispatcher):
    dp.filters_factory.bind(IsNumber)
    dp.filters_factory.bind(IsCurrency)
