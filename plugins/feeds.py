import asyncio

import requests

from botutils import getSettingsDoc, getServerDoc

async def checkForUpdates(ctx):
    while True:
        for server in ctx.bot.guilds:
            for source in getServerDoc(server.id, ['plugins', 'feeds', 'sources']):
                if source['type'] == 'rss':
                    r = requests.get(source['typeSettings']['source'])
                    r = None
        await asyncio.sleep(getSettingsDoc(['plugins', 'feeds', 'refreshTime']))

events = [
    {
        'type': 'onReady',
        'callable': checkForUpdates
    }
]