import datetime
import os.path

import requests

import discord

import cairosvg

async def c_weather(ctx, place):
    r = requests.get('https://api.openweathermap.org/data/2.5/weather', params={'q': place, 'appid': ctx.secrets['openweathermap'], 'units': 'metric'})
    response = r.json()

    if response['cod'] == 404:
        await ctx.send(f"There is no city `{place}`.")
        return
    elif response['cod'] != 200:
        await ctx.send(f"Unknown error (error code: `{response['cod']}`).")
        return
    
    emojiIcons = {
        '01': ':sunny:',
        '02': ':white_sun_cloud:',
        '03': ':cloud:',
        '04': ':cloud:',
        '09': ':cloud_rain:',
        '10': ':white_sun_rain_cloud:',
        '11': ':thunder_cloud_rain:',
        '13': ':snowflake:',
        '50': ':fog:'
    }
    
    place = response['name']
    icon = response['weather'][0]['icon']
    name = response['weather'][0]['main']
    description = response['weather'][0]['description']
    temperature = response['main']['temp']
    temperatureFeel = response['main']['feels_like']
    pressure = response['main']['pressure']
    humidity = response['main']['humidity']

    try:
        wind = response['wind']['speed']
    except:
        wind = 0
    
    try:
        clouds = response['clouds']['all']
    except:
        clouds = 0
    
    try:
        rain = response['rain']['1h']
    except:
        rain = 0
    
    try:
        snow = response['snow']['1h']
    except:
        snow = 0
    
    embed = discord.Embed(
        title=f"Weather for {place}",
        description=f"""{emojiIcons[icon[:-1]]} **{name}**
        *{description}*
        
        **Temperature:** {temperature}\u00b0C
        *Feels like {temperatureFeel}\u00b0C*
        **Pressure:** {pressure} hPa
        **Humidity:** {humidity}%
        **Wind speed:** {wind} m/s
        **Cloudiness:** {clouds}%
        **Rain:** {rain} mm (last 1h)
        **Snow:** {snow} mm (last 1h)"""
    )
    embed.set_thumbnail(url = f"https://openweathermap.org/img/wn/{icon}@2x.png")
    await ctx.send(embed=embed)

async def c_aweather(ctx, place):
    r = requests.get('http://dataservice.accuweather.com/locations/v1/search', params={'apikey': ctx.secrets['accuweather'], 'q': place})
    response = r.json()[0]

    locationKey = response['Key']
    place = response['EnglishName']

    r = requests.get(f"http://dataservice.accuweather.com/currentconditions/v1/{locationKey}", params={'apikey': ctx.secrets['accuweather'], 'details': 'true'})
    response = r.json()[0]

    emojiIcons = {
        1: ':sunny:',
        2: ':white_sun_small_cloud:',
        3: ':partly_sunny:',
        4: ':partly_sunny:',
        5: ':white_sun_cloud:',
        6: ':white_sun_cloud:',
        7: ':cloud:',
        8: ':cloud:',
        11: ':fog:',
        12: ':cloud_rain:',
        13: ':white_sun_rain_cloud:',
        14: ':white_sun_rain_cloud:',
        15: ':thunder_cloud_rain:',
        16: ':white_sun_rain_cloud:',
        17: ':white_sun_rain_cloud:',
        18: ':cloud_rain:',
        19: ':cloud:',
        20: ':cloud_snow:',
        22: ':cloud_snow:',
        23: ':cloud_snow:',
        24: ':ice_cube:',
        25: ':cloud_rain:',
        26: ':cloud_rain:',
        29: ':cloud_rain:',
        30: ':hotsprings:',
        31: ':snowflake:',
        32: ':flag_white:',
        33: ':new_moon:',
        34: ':white_sun_small_cloud:',
        35: ':partly_sunny:',
        36: ':partly_sunny:',
        37: ':white_sun_cloud:',
        38: ':white_sun_cloud:',
        39: ':white_sun_rain_cloud:',
        40: ':white_sun_rain_cloud:',
        41: ':thunder_cloud_rain:',
        42: ':thunder_cloud_rain:',
        43: ':cloud_snow:',
        44: ':cloud_snow:'
    }

    name = response['WeatherText']
    icon = response['WeatherIcon']
    temperature = response['Temperature']['Metric']['Value']
    realfeel = response['RealFeelTemperature']['Metric']['Value']
    realfeelshade = response['RealFeelTemperatureShade']['Metric']['Value']
    humidity = response['RelativeHumidity']
    humidityIndoors = response['IndoorRelativeHumidity']
    dewPoint = response['DewPoint']['Metric']['Value']
    windDirectionDegrees = response['Wind']['Direction']['Degrees']
    windDirection = response['Wind']['Direction']['English']
    windSpeed = response['Wind']['Speed']['Metric']['Value']
    windGust = response['WindGust']['Speed']['Metric']['Value']
    uvIndex = response['UVIndexText']
    uvIndexValue = response['UVIndex']
    visibility = response['Visibility']['Metric']['Value']
    pressure = response['Pressure']['Metric']['Value']
    rain = response['Precip1hr']['Metric']['Value']

    embed = discord.Embed(
        title=f"Weather for {place}",
        description=f"""{emojiIcons.get(icon, ':interrobang:')} **{name}**
        
        **Temperature:** {temperature}\u00b0C
        **RealFeel\u00ae:** {realfeel}\u00b0C
        *RealFeel Shade\u2122:** {realfeelshade}\u00b0C

        **Pressure:** {pressure} mbar
        **Humidity:** {humidity}% ({humidityIndoors}% indoors)
        **Dew point:** {dewPoint}\u00b0C
        **Wind:** {windDirection} ({windDirectionDegrees}), {windSpeed} km/h (gust {windGust} km/h)
        **Precipitation:** {rain} mm (last 1h)"""
    )

    embed.set_thumbnail(url = f"https://grzesiek11.stary.pc.pl/el/accuweather/{icon}.png")

    await ctx.send(embed=embed)

async def c_thunder(ctx, code='pl'):
    await ctx.send(f"http://images.blitzortung.org/Images/image_b_{code}.png?mapId={int(datetime.datetime.now().timestamp() * 1000)}")

events = [
    {
        'type': 'command',
        'name': 'weather',
        'aliases': [],
        'callable': c_weather
    },
    {
        'type': 'command',
        'name': 'thunder',
        'aliases': [],
        'callable': c_thunder
    },
    {
        'type': 'command',
        'name': 'aweather',
        'aliases': [],
        'callable': c_aweather
    }
]