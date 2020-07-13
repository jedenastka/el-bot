async def c_ping(bot, message):
    await message.channel.send('Pong!')

events = [
    {
        'type': 'command',
        'name': 'ping',
        'alias': ['test'],
        'callable': c_ping
    }
]