async def log(bot, message):
    print(message.content)

events = [
    {
        'type': 'onMessage',
        'callable': log
    }
]