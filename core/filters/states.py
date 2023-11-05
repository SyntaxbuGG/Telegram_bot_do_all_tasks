from aiogram.filters.state import StatesGroup, State


class CountryStats(StatesGroup):
    enter_first = State()
    chosen = State()
    weather = State()
    city = State()
    book = State()
    web_app = State()
    info_weather=State()
    pick_city = State()
    pick_alarm = State()


