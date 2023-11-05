import aiohttp
import asyncio
import json
import emoji

access_key = 'p381l3N4fa7KHVV1kspAXv6IjsDBuHiYEO6HbmM1ZQg'


async def get_random_image_from_unsplash(access_key):
    url = 'https://api.unsplash.com/photos/random'
    async with aiohttp.ClientSession() as session:
        headers = {'Authorization': f'Client-ID {access_key}'}
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                print(data)
                return data['urls']['full']  # Возвращаем URL случайной фотографии
            else:
                print(f'Ошибка {response.status}: {await response.text()}')
                return None


# Ваш ключ доступа к Unsplash API

async def get_image(acces_key, word):
    url = 'https://api.unsplash.com/search/photos'
    query_parametrs = {'client_id': acces_key, 'query': word, 'page': "10"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=query_parametrs) as response:
            if response.status == 200:
                print(response)
                data = await response.json()
                if data['results']:
                    print(data)
                    image_url = data['results'][0]['urls']['full']
                    return image_url
                else:
                    "Извините по запросу не найдено изображений"
            else:
                print(f"Ошибка {response.status}:{await response.text()}")


# async def main():
#     random_image_url = await get_random_image_from_unsplash(access_key)
#     if random_image_url:
#         print('URL случайной фотографии:', random_image_url)


async def get_api_weather(data1):
    url_get = f"http://api.weatherapi.com/v1/forecast.json?key=db82493ba5634651bb6111737230910&q={data1}&days=10&aqi=no&alerts=no"
    async with aiohttp.ClientSession() as session:
        async with session.get(url_get) as response:
            try:
                weather_icons = {
                    'Sunny': ' ☀️',
                    'Clear': ' 🌙',
                    'Partly cloudy': ' ⛅ ',
                    'Cloudy': ' ☁️',
                    "Patchy rain possible": "🌦️",
                    'Overcast': '☁️️',
                    'Mist': '🌫️',
                    'Patchy rain possible': '🌦️',
                    'Patchy snow possible': ' 🌨️ ',

                }

                json_weather = await response.json()
                json_formatted = json.dumps(json_weather, indent=2)
                print(json_formatted)
                region = json_weather.get('location')['region']
                country = json_weather.get('location')['country']
                local_time_now = json_weather.get('location')['localtime']
                temp_c = json_weather.get('current')['temp_c']
                condition = json_weather.get('current')['condition']['text']
                feels_like = json_weather.get('current')['feelslike_c']
                humidity = json_weather.get('current')['humidity']
                wind = json_weather.get('current')['wind_kph']
                wind_dir = json_weather.get('current')['wind_dir']
                visability = json_weather.get('current')['vis_km']
                max_tm = json_weather.get('forecast')['forecastday'][0]['day']['maxtemp_c']
                will_it_rain = json_weather.get('forecast')['forecastday'][0]['day']['daily_will_it_rain']
                chance_of_rain = json_weather.get('forecast')['forecastday'][0]['day']['daily_chance_of_rain']
                will_it_snow =json_weather.get('forecast')['forecastday'][0]['day']['daily_will_it_snow']
                chance_of_snow = json_weather.get('forecast')['forecastday'][0]['day']['daily_chance_of_snow']

                if condition in weather_icons:
                    wd = weather_icons[condition]
                else:
                    wd = '🤔'

                if will_it_rain == 0:
                    will_it_rain = 'No'
                else:
                    will_it_rain = 'Yes'

                if will_it_snow == 0:
                    will_it_snow = 'No'
                else:
                    will_it_snow = 'Yes'



                print(f"weather in {region} {emoji.emojize(f':{country}:')}\n"
                      f"time : {local_time_now}\n\n"
                      f"<strong>current weather</strong>\n"
                      f"{wd} {temp_c}°C\n"
                      f"Feels like: {feels_like}°C\n"
                      f"Maximum temperature on the day: {max_tm}\n"
                      f"Humidity: {humidity}%\n"
                      f"Wind: {wind_dir} {wind} km/h\n"
                      f"Visability: {visability} km\n"
                      f"Will it rain: {will_it_rain}. Chance of rain: {chance_of_rain}%\n"
                      f"Will in snow: {will_it_snow}. Chance of snow: {chance_of_snow}%")








            except Exception as err:
                print(f'{err}')

    #


# async def main_search():
#     search_keyword = 'Uzbekistan'
#     image_url = await get_image(access_key, search_keyword)
#     if image_url:
#         print('Url найденной фотографии', image_url)
token_aqi = "54d2c3f7b8f9cabfa0dce6d0b2e5ad7ad62eb483"
async def check_aqi(country):
    url = 'https://aqicn.org/json-api/doc/feed/:city/?token=:token'
    async with aiohttp.ClientSession() as session:
        async with session.get()

if __name__ == '__main__':
    asyncio.run(get_api_weather('Tashkent'))
