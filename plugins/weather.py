import requests

import discord

async def c_weather(ctx, city):
    r = requests.get('https://api.openweathermap.org/data/2.5/weather', params={'q': city, 'appid': ctx.secrets['openweathermap'], 'units': 'metric'})
    weather = r.json()

    if weather['cod'] == 404:
        await ctx.send(f"There is no city `{city}`.")
        return
    elif weather['cod'] != 200:
        await ctx.send(f"Unknown error (error code: `{weather['cod']}`).")
    
    embed = discord.Embed(
        title=f"Weather for {weather['name']}",
        description=f"""**{weather['weather'][0]['main']}**
        *{weather['weather'][0]['description']}*
        
        **Temperature:** {weather['main']['temp']}\u00b0C
        *Feels like {weather['main']['feels_like']}\u00b0C*
        **Pressure:** {weather['main']['pressure']} hPa
        **Humidity:** {weather['main']['humidity']}%
        **Wind speed:** {weather['wind']['speed']} m/s
        **Cloudiness:** {weather['clouds']['all']}%
        **Rain:** {weather['rain']['1h']} mm (last 1h)
        **Snow:** {weather['snow']['1h']} mm (last 1h)"""
    )
    embed.set_thumbnail(url = f"https://openweathermap.org/img/wn/{weather['weather'][0]['icon']}@2x.png")
    await ctx.send(r.text, embed=embed)

events = [
    {
        'type': 'command',
        'name': 'weather',
        'aliases': [],
        'callable': c_weather
    }
]