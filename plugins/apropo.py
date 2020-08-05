import math

async def c_apropo(ctx, topic):
    entry = ctx.bot.db['apropo'].find_one({'topic': topic})
    if entry is None:
        await ctx.message.channel.send(f"There is no `{topic}` apropo.")
        return
    
    await ctx.message.channel.send(entry['content'])

async def c_apropo_add(ctx, topic, *content):
    content = ' '.join(content)
    if ctx.bot.db['apropo'].find_one({'topic': topic}) is not None:
        await ctx.message.channel.send(f"There already is an `{topic}` apropo.")
        return

    ctx.bot.db['apropo'].insert_one({'topic': topic, 'content': content, 'files': ctx.message.attachments})

async def c_apropo_list(ctx, page=1):
    page = int(page)
    perPage = 50
    count = ctx.bot.db['apropo'].count_documents({})
    pages = math.ceil(count / perPage)

    if page > pages or page <= 0:
        await ctx.message.channel.send(f"There is no page {page}.")
        return

    entries = ctx.bot.db['apropo'].find()
    topics = []
    maxLenght = 0
    for apropoEntry in entries[(page - 1) * perPage:page * perPage]:
        topic = apropoEntry['topic']
        topics.append(topic)
        if len(topic) > maxLenght:
            maxLenght = len(topic)
    
    for i in range(len(topics)):
        topics[i] = f"{topics[i]: <{maxLenght}}"

    await ctx.message.channel.send(f"```\n{' '.join(topics).strip()}\n```\n**Page:** {page}/{pages}\n**Total apropo count:** {count}")

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