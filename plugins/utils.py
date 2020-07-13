async def c_ping(bot, message, text = 'Pong!'):
    await message.channel.send(text)

events = [
    {
        'type': 'command',
        'name': 'ping',
        'alias': ['test'],
        'callable': c_ping
    }
]