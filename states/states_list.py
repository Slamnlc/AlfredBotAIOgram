from aiogram.dispatcher.filters.state import StatesGroup, State


class FirstSettings(StatesGroup):
    mainStart = State()
    showCurrency = State()
    indicateMainCurrency = State()
    indicateDaysForShow = State()
    indicateCurrencyList = State()
    indicateMainCity = State()
    selectMainCity = State()


class CurrencyState(StatesGroup):
    mainMenu = State()
    otherCurrency = State()
    selectCurrencyFrom = State()
    convertor = State()
    changeCurrencyFrom = State()
    changeCurrencyTo = State()


class SettingsState(StatesGroup):
    settingsMenu = State()
    searchMainCity = State()
    setMainCity = State()
    setMainCurrency = State()
    setDayForShow = State()
    setCurrencyList = State()


class WeatherState(StatesGroup):
    weatherMenu = State()
    searchState = State()


class BookSearch(StatesGroup):
    bookMenu = State()
    bookResult = State()


class Yap(StatesGroup):
    yapMainMenu = State()
    subMenu = State()
    showPhotos = State()
    card = State()