import emoji

import aiohttp
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from core.keyboards.reply_markyp import *
from core.helpers.constant import *
from core.filters.states import *

from core.helpers.constant import WEATHER
from core.db.config import db_connect
from core.db.database_ import ConnectPostgres

from core.helpers.information_weather import *
from core.helpers.information_book import *

router = Router()
dbc = ConnectPostgres(db_connect)


@router.message(CommandStart())
async def country_handler(msg: Message, state: FSMContext, ):
    if not await dbc.check_user(msg.from_user.id):
        await dbc.add_user(msg.from_user.id, msg.from_user.first_name, msg.from_user.username)

    await state.clear()
    await msg.answer(
        text=f"Здравствуйте <strong>{msg.from_user.full_name}</strong>🤗\nУ бота есть разные функции Желаю приятно провести время😊",
        reply_markup=main_meny())
    await state.set_state(CountryStats.chosen)
    await msg.delete()


@router.message(CountryStats.chosen, F.text == WEATHER)
async def country_state(msg: Message, state: FSMContext):
    await state.set_state(CountryStats.chosen)
    if await dbc.check_country(msg.from_user.id):
        await city_state(msg, state)
    else:
        await msg.answer(WRITE_TOWN_NAME, reply_markup=ReplyKeyboardRemove())


@router.message(CountryStats.chosen)
async def city_state(msg: Message, state: FSMContext):
    await state.update_data(city=msg.text)
    await state.set_state(CountryStats.weather)
    data_get = await state.get_data()
    if not await dbc.check_country(msg.from_user.id):
        await dbc.get_country(msg.from_user.id, data_get['city'])
    await msg.answer(text=CHOSE_OPTION, reply_markup=weather())


@router.message(CountryStats.weather, F.text == BACK_TO)
async def back_to_weather(msg: Message, state: FSMContext):
    await dbc.execute_query('DELETE FROM user_get_inform WHERE users_id = $1', msg.from_user.id)
    await state.clear()
    await country_state(msg, state)


@router.message(CountryStats.weather, F.text == CURRENT_WEATHER)
async def get_current(msg: Message, state: FSMContext):
    await state.set_state(CountryStats.weather)
    data = await state.get_data()
    info_weath = data.get('info_weather')
    if info_weath is not None:
        await msg.answer(text=info_weath[0])
    else:
        data_get = await dbc.fetchrow_query('SELECT get_country from user_get_inform where users_id = $1',
                                            msg.from_user.id)
        data_weather = await get_weather(data_get)
        await state.update_data(info_weather=data_weather)
        await msg.answer(text=data_weather[0])


@router.message(CountryStats.weather, F.text == TOMORROW_WEATHER)
async def get_tomorrow_weather(msg: Message, state: FSMContext):
    data = await state.get_data()
    info_weath = data.get('info_weather')
    if info_weath is not None:
        await msg.answer(text=info_weath[1])
    else:
        data_get = await dbc.fetchrow_query('SELECT get_country from user_get_inform where users_id = $1',
                                            msg.from_user.id)
        data_weather = await get_weather(data_get)
        await state.update_data(info_weather=data_weather)
        await msg.answer(text=data_weather[1])


@router.message(CountryStats.weather, F.text == WEATHER_ALARM)
async def get_alarm_weather(msg: Message, state: FSMContext):
    await state.set_state(CountryStats.weather)
    await msg.answer(text="Выберите тип отправляемых уведомление", reply_markup=weather_alarm())



@router.message(CountryStats.weather, F.text.in_({WEATHER_TODAY, WEATHER_THREE_DAY}))
async def get_set_alarm(msg: Message, state: FSMContext):
    await state.update_data(pick_alarm=msg.text)
    await state.set_state(CountryStats.weather)
    take = await state.get_data()
    await dbc.execute_query('INSERT INTO user_get_inform (pick_when_alarm) VALUES ($1)', take.get('pick_alarm'))
    await msg.answer('Выберете время отправки уведомлений', reply_markup=weather_ring())



@router.message(CountryStats.weather, F.text == WEATHER_BY_DAY)
async def weather_day(msg: Message, state: FSMContext):
    await state.set_state(CountryStats.pick_alarm)
    await msg.answer(text='Выберите какой в день надо отправить вам уведомление', reply_markup=weather_by_day())


@router.message(CountryStats.pick_alarm)
async def every_by_alarm(msg: Message, state: FSMContext):
    await every_alarm(msg,state)


@router.message(CountryStats.weather, F.text == WEATHER_EVERY_ALARM)
async def every_alarm(msg: Message, state: FSMContext):
    await msg.answer('Выберите в какое время надо отправить вам уведомление', reply_markup=weather_date())


# @router.message(CountryStats.chosen, F.text == WEB_APP)
# async def get_web_app(msg:Message):
#     set_state'
#
# @router.message(CountryStats.chosen, F.text == BOOK)
# async def get_book(msg: Message, state: FSMContext):
#     await state.set_state(CountryStats.book)
#     await msg.answer(text=CHOSE_OPTION, reply_markup=book())
@router.message(CountryStats.chosen, F.text == BOOK)
async def get_start(msg: Message, state: FSMContext) -> None:
    await state.set_state(CountryStats.book)
    await msg.answer(
        text=f'Привет <strong>{msg.from_user.first_name}</strong> ,я могу найти информацию об автора книги 😉'
             f'\n\nНапишите имя автора ', reply_markup=ReplyKeyboardRemove())


@router.message(CountryStats.book, F.text)
async def book_of_search(msg: Message, state: FSMContext):
    await state.update_data(book=msg.text)
    data_get = await state.get_data()
    await msg.answer(f'{request_main(data_get["book"][0])}')
    print(request_main(msg.text)[1])
    await msg.answer_photo(photo=f'{request_main(data_get["book"])[1]}')

    #

    # async def weather_date_by_city(data):
    #     url_geo = f'https://geocoding-api.open-meteo.com/v1/search?name={data["city"]}&count=1&language=en&format=json'
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(url_geo) as response:
    #             json_ = await response.json()
    #             latitude = json_['results'][0]['latitude']
    #             longitude = json_['results'][0]['longitude']
    #             url_weather = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,rain,snowfall,snow_depth,visibility&current_weather=true&timezone=auto'
    #             async with session.get(url_weather) as response1:
    #                 json_ = await response1.json()
    #                 result = json_.get('current_weather', 'не пришел ничего')
    #                 return result

    # async def get_info_book(data1):
    #     url_get = f"https://openlibrary.org/search/authors.json?q={quote(data1)}"
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(url_get) as response:
    #             json_ = await response.json()
    #
    #             get_url = json_.get(url_get).json()
    #             key_author = get_url.get('docs')[0]
    #             url_author = f'https://covers.openlibrary.org/a/olid/{key_author["key"]}-L.jpg'
    #             return (key_author['name'], url_author)
    #

    # async def get_api_weather(data1):
    #     url_get = f"http://api.weatherapi.com/v1/current.json?key=db82493ba5634651bb6111737230910&q={data1}&aqi=no"
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(url_get) as response:
    #             try:
    #                 json_weather = await response.json()
    #                 # json_formatted = json.dumps(json_, indent=2)
    #                 # print(json_formatted)
    #                 region = json_weather.get('location')['region']
    #                 country = json_weather.get('location')['country']
    #                 local_time_now = json_weather.get('location')['localtime']
    #
    #                 print(f"Weather in {region} {emoji.emojize(f':{country}:')}\n"
    #                       f"Time : {local_time_now}\n\n"
    #                       f"<strong>Current weather</strong>\n"
    #                       f"{json_weather.get('current')['condition']['icon']}")


@router.message(CountryStats.chosen)
async def get_text(msg: Message):
    await msg.answer(
        '<Strong>Извините я не принимаю ответы написанным пользователям!!!</strong> \nПожалуйста обращайтесь'
        ' ко мне только через кнопки', reply_markup=main_meny())
