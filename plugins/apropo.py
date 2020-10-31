import math

from botutils import getServerDoc, updateServerDoc

dbPath = ['plugins', 'apropo', 'database']

async def c_apropo(ctx, topic):
    entry = getServerDoc(ctx.message.guild.id, dbPath + [topic], addOverlay=True)
    if entry is None:
        await ctx.send(f"There is no `{topic}` apropo.")
        return
    
    await ctx.send(entry['content'])

async def c_apropo_add(ctx, topic, *content):
    content = ' '.join(content)
    if getServerDoc(ctx.message.guild.id, dbPath + [topic], addOverlay=True) != {}:
        await ctx.send(f"There already is an `{topic}` apropo.")
        return

    updateServerDoc(ctx.message.guild.id, {topic: {'content': content}}, dbPath)

async def c_apropo_list(ctx, page=1):
    entries = getServerDoc(ctx.message.guild.id, dbPath, addOverlay=True)

    page = int(page)
    perPage = 50
    pages = math.ceil(len(entries) / perPage)

    if page > pages or page <= 0:
        await ctx.send(f"There is no page {page}.")
        return

    topics = list(entries.keys())
    
    for i in range(len(topics)):
        topics[i] = f"{topics[i]: <{len(max(topics))}}"

    await ctx.send(f"```\n{' '.join(topics).strip()}\n```\n**Page:** {page}/{pages}\n**Total apropo count:** {len(entries)}")

events = [
    {
        'type': 'command',
        'name': 'apropo',
        'aliases': ['apo'],
        'callable': c_apropo,
        'subcommands': [
            {
                'type': 'command',
                'name': 'add',
                'aliases': [],
                'callable': c_apropo_add
            },
            {
                'type': 'command',
                'name': 'list',
                'aliases': [],
                'callable': c_apropo_list
            }
        ]
    }
]