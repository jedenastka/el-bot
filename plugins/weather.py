import requests

async def c_weather(ctx, city):
    r = requests.get('https://api.openweathermap.org/data/2.5/weather', params={'q': city, 'appid': ctx.secrets['openweathermap']})
    await ctx.send(r.text)

events = [
    {
        'type': 'command',
        'name': 'weather',
        'aliases': [],
        'callable': c_weather
    }
]