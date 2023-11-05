import aiohttp
import emoji
from core.helpers.constant import BACK_TO

weather_icons = {
    'Sunny': '☀️',
    'Clear': '🌙',
    'Partly cloudy': '⛅',
    'Cloudy': '☁️',
    "Patchy rain possible": "🌦️",
    'Overcast': '☁️️',
    'Mist': '🌫️',
    'Patchy snow possible': '🌨️',
    "Light rain": '🌧'}


async def get_weather(strana):
    url_get = f"https://api.weatherapi.com/v1/forecast.json?key=db82493ba5634651bb6111737230910&q={strana}&days=10&aqi=no&alerts=no"
    async with aiohttp.ClientSession() as session:
        async with session.get(url_get) as response:
            try:
                json_weather = await response.json()

                location = json_weather.get('location')
                current = json_weather.get('current')
                forecast = json_weather.get('forecast')['forecastday'][0]
                current_hour = forecast['hour']
                region = location['region']
                country = location['country']
                local_time_now = location['localtime']
                last_updated = current['last_updated']
                time_weather = local_time_now[-5:-3]
                temp_c = current['temp_c']
                condition = current['condition']['text']
                feels_like = current['feelslike_c']
                humidity = current['humidity']
                wind = current['wind_kph']
                wind_dir = current['wind_dir']
                visability = current['vis_km']
                max_tm = forecast['day']['maxtemp_c']
                min_tm = forecast['day']['mintemp_c']
                will_it_rain = forecast['day']['daily_will_it_rain']
                chance_of_rain = forecast['day']['daily_chance_of_rain']
                will_it_snow = forecast['day']['daily_will_it_snow']
                chance_of_snow = forecast['day']['daily_chance_of_snow']
                sunrise = forecast['astro']['sunrise']
                sunset = forecast['astro']['sunset']
                wd = weather_icons.get(condition, )
                will_it_rain_if = 'Да' if will_it_rain else 'Нет'
                will_it_snow_if = 'Да' if will_it_snow else 'Нет'
                tomorw_weath = await tomorrow_weather(json_weather)
                lists_hour = ""
                for i, x in enumerate(current_hour):
                    if int(time_weather) < i:
                        list_hour = f"{x['time'][-5:]} {weather_icons.get(x['condition']['text'], '🤔')} {x['temp_c']}°C \n"
                        lists_hour += list_hour

                return (
                    f'''Погода в {region} {emoji.emojize(f':{country}:')}
Локальная время: {local_time_now}\n
Информация обновлена: {last_updated}
<strong>ТЕКУЩАЯ ПОГОДА</strong> 🌡
{wd} {temp_c}°C
Ощущение как: {feels_like}°C
Максимальная температура: {max_tm}°C
Минимальная температура: {min_tm}°C
Влажность: {humidity}%
Ветер: {wind_dir} {wind} km/h
Видимость: {visability} km
Будет ли дождь: {will_it_rain_if}
Будет ли снег: {will_it_snow_if}
Восход: {sunrise} 🌇  Закат: {sunset} 🌆
{lists_hour}''', tomorw_weath)
            except Exception as err:
                print(f'{err}')
                return ('Не можем найти город который вы написали,\n'
                        f'Чтобы заново ввести,Нажмите кнопку <strong>{BACK_TO}</strong>.\n'
                        'Пожалуйста внимательно свой город без ошибок напишите')


#
async def tomorrow_weather(json_weath):
    ful_forecast = json_weath.get('forecast')['forecastday']
    lists = f"{ful_forecast[0]['date']}              {ful_forecast[1]['date']}              {ful_forecast[2]['date']}\n"


    for x, y, z in zip(ful_forecast[0]['hour'], ful_forecast[1]['hour'], ful_forecast[2]['hour']):

        list_hour = f"{x['time'][-5:]}{weather_icons.get(x['condition']['text'], '🤔')} {x['temp_c']}°C"
        list_hour2 = f"{y['time'][-5:]}{weather_icons.get(y['condition']['text'], '🤔')} {y['temp_c']}°C"
        list_hour3 = f"{z['time'][-5:]}{weather_icons.get(z['condition']['text'], '🤔')} {z['temp_c']}°C"
        lists += f'{list_hour} <strong>||</strong> {list_hour2} <strong>||</strong> {list_hour3}\n'
    return lists
