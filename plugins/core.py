async def readyMessage(ctx):
    print("Ready!")

events = [
    {
        'type': 'onReady',
        'callable': readyMessage
    }
]