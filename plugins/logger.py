async def log(ctx):
    print(ctx.message.content)

events = [
    {
        'type': 'onMessage',
        'callable': log
    }
]