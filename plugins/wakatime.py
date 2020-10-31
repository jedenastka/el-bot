from botutils import getServerDoc
import datetime

dbPath = ['plugins', 'wakatime']

async def c_wakatime(ctx, user=None):
    if user is None:
        user = ctx.message.author.name
    
    profile = getServerDoc(ctx.message.guild.id, dbPath + ['profiles', str(user)], addOverlay=True)
    if profile == {}:
        return
    
    await ctx.send(f"https://wakatime.com/share/@{profile['id']}/{profile['chart']}?{int(datetime.datetime.timestamp(datetime.datetime.now()))}")

events = [
    {
        'type': 'command',
        'name': 'wakatime',
        'aliases': ['waka'],
        'callable': c_wakatime
    }
]