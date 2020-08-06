import datetime

import requests

import discord

async def c_weather(ctx, city):
    r = requests.get('https://api.openweathermap.org/data/2.5/weather', params={'q': city, 'appid': ctx.secrets['openweathermap'], 'units': 'metric'})
    response = r.json()

    if response['cod'] == 404:
        await ctx.send(f"There is no city `{city}`.")
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
    
    city = response['name']
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
        title=f"Weather for {city}",
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
    }
]