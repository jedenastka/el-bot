from classes import Context
from instances import bot, db, settings, secrets, events
from parser import getCommand
from botutils import getDefaultDoc

async def on_message(message):
    context = Context(message, bot, db, settings, secrets)

    for event in events:
        if event['type'] == 'onMessage':
            await event['callable'](context)

    command, args = getCommand(message)
    if command != {}:
        await command['callable'](context, *args)

async def on_message_delete(message):
    context = Context(message, bot, db, settings, secrets)

    for event in events:
        if event['type'] == 'onDelete':
            await event['callable'](context)

async def on_message_edit(before, after):
    context = Context(None, bot, db, settings, secrets)

    for event in events:
        if event['type'] == 'onEdit':
            await event['callable'](context, before, after)

async def on_raw_reaction_add(payload):
    context = Context((await bot.get_guild(payload.guild_id).get_channel(payload.channel_id).fetch_message(payload.message_id)), bot, db, settings, secrets)
    emoji = payload.emoji
    user = bot.get_guild(payload.guild_id).get_member(payload.user_id)

    for event in events:
        if event['type'] == 'onReaction':
            await event['callable'](context, emoji, user)

async def on_raw_reaction_remove(payload):
    context = Context((await bot.get_guild(payload.guild_id).get_channel(payload.channel_id).fetch_message(payload.message_id)), bot, db, settings, secrets)
    emoji = payload.emoji
    user = bot.get_guild(payload.guild_id).get_member(payload.user_id)

    for event in events:
        if event['type'] == 'onReactionRemove':
            await event['callable'](context, emoji, user)

async def on_guild_join(guild):
    overlay = db['system'].find_one({'special': 'default'})
    overlay.pop('_id')
    overlay.pop('special')

    if db['servers'].find_one({'id': guild.id}) is None:
        db['servers'].insert_one({'id': guild.id, **overlay})

    context = Context(None, bot, db, settings, secrets)

    for event in events:
        if event['type'] == 'onJoin':
            await event['callable'](context, guild)

async def on_ready():
    for default in settings['systemDbDefault']:
        if db['system'].find_one({'special': default['special']}) is None:
            db['system'].insert_one(default)
    
    overlay = getDefaultDoc()

    for guild in bot.guilds:
        if db['servers'].find_one({'id': guild.id}) is None:
            db['servers'].insert_one({'id': guild.id, **overlay})

    context = Context(None, bot, db, settings, secrets)

    for event in events:
        if event['type'] == 'onReady':
            await event['callable'](context)