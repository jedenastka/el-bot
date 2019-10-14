import discord
from discord.ext import commands
import pymongo
import json, os
import secrets

# make cache directory
os.makedirs('cache', exist_ok=True)

def notIfNotNone(statement):
    return not statement and statement is not None

def empty(obj):
    return tuple(obj) == ()

def getServerData(serverId):
    # get server data from default
    serverData = bot.data["default"]
    # update it with database
    serverDataDb = bot.db.servers.find_one({"id": serverId})
    if serverDataDb is not None:
        serverData.update(serverDataDb)
    # and then with global
    serverData.update(bot.data["global"])
    return serverData

# help embed generator
def generateHelp(commandsArray):
    helpText = '**Commands:**\n\n'
    for command in commandsArray:
        helpText += f'''{command} {command.signature}{' ...' if isinstance(command, commands.Group) else ''}\n'''
    return discord.Embed(title = 'Help', description = helpText)

# callable prefix
def prefix(bot, message):
    prefixes = bot.data['prefixes']
    if message.guild != None:
        if str(message.guild.id) in bot.data['servers']:
            guildPrefixes = bot.data['servers'][str(message.guild.id)]['prefixes']
            if guildPrefixes != []:
                prefixes = guildPrefixes
    return prefixes

bot = commands.Bot(command_prefix = "el!")

with open('data.json') as file:
    bot.data = json.load(file)

dbClient = pymongo.MongoClient()
bot.db = dbClient['el']

# when ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} (ID: {bot.user.id})')

# delete default help
bot.remove_command('help')

# custom help command
@bot.command(name='help')
async def _help(ctx, command = None):
    if command == None:
        helpEmbed = generateHelp(bot.commands)
    else:
        for botCommand in bot.commands:
            if str(botCommand) == command or command in botCommand.aliases:
                if isinstance(botCommand, commands.Group):
                    helpEmbed = generateHelp(botCommand.commands)
                    break
                else:
                    pass
            else:
                pass
    await ctx.send(embed = helpEmbed)

@bot.group(name='permissions', aliases=['p'])
async def _permissions(ctx):
    server = ctx.guild
    document = {"id": server.id}
    bot.db.servers.insert_one(document)

@_permissions.command(name='command', aliases=['c'])
async def _command(ctx, commandName, operation=None, *args):
    if operation is None:
        serverData = getServerData(ctx.guild.id)
        permisions = multiget(serverData, "commands", commandName, "permisions")
        defaultPermisions = multiget(serverData, "commandDefault", "permisions")
        if permisions is not None:
            permisions.update(defaultPermisions)
        else:
            permisions = defaultPermisions
        await ctx.send(str(permisions))

def multiget(dictionary, *path):
    temp = dictionary
    for i in path:
        temp = temp.get(i)
        if temp is None:
            break
    return temp

# check
@bot.check
async def globalCheck(ctx):
    commandName = ctx.command.qualified_name
    user = ctx.message.author.id
    serverData = getServerData(ctx.guild.id)
    # check if command is specified
    if commandName in serverData["commands"]:
        commandData = serverData["commands"][commandName]
    else:
        # fallback to default if not
        commandData = serverData["commandDefault"]
    commandPermisions = commandData.get("permisions")
    # do not run when disabled
    if notIfNotNone(multiget(commandData, "enabled")):
        return False
    # do group check
    commandGroups = commandPermisions.get("groups")
    groupCheck = None
    if commandGroups is not None and not empty(commandGroups):
        groups = serverData["groups"]
        # for every group
        userGroups = []
        for group in groups.items():
            if user in group[1]:
                userGroups.append(group[0])
        for group in commandGroups:
            if group["name"] in userGroups:
                groupCheck = group["allow"]
                break
    # when user is not allowed
    userCheck = multiget(commandPermisions, "users", str(user))
    if userCheck is not None:
        if not userCheck:
            return False
        elif notIfNotNone(commandPermisions.get("default")):
            # fallback
            return False
    elif notIfNotNone(groupCheck):
        # and when group is not allowed
        return False
    return True

# load plugins
for plugin in bot.data["plugins"]:
    bot.load_extension(bot.data["pluginPath"] + plugin)

bot.run(secrets.token, bot=True, reconnect=True)