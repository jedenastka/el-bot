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

dbClient = pymongo.MongoClient(secrets.mongoUri if secrets.mongoUri else None)
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

# Code related to permissions got a little messy. Requires cleanup.
def getServerData(serverID: int):
    # get server data from default
    serverData = bot.data["default"].copy()
    # update it with database
    serverDataDb = bot.db.servers.find_one({"id": serverID})
    if serverDataDb is not None:
        serverData.update(serverDataDb)
    # and then with global
    serverData.update(bot.data["global"])
    return serverData

def getCommandData(serverData, commandName: str):
    commandData = multiget(serverData, "commandDefault").copy()
    commandDataUpdate = multiget(serverData, "commands", commandName)
    if commandDataUpdate is not None:
        commandData.update(commandDataUpdate)
    return commandData

def updateServersDb(serverID: int, query: dict):
    bot.db.servers.update_one({'id': serverID}, query, upsert=True)

def updatePermissions(serverID: int, where: str, how: str):
    if how == 'enable':
        updateServersDb(serverID, {"$set": {where: 1}})
    elif how == 'disable':
        updateServersDb(serverID, {"$set": {where: 0}})
    elif how == 'default':
        updateServersDb(serverID, {"$unset": {where: ''}})

@bot.group(name='permissions', aliases=['p'])
async def _permissions(ctx):
    server = ctx.guild
    document = {"id": server.id}
    if not bot.db.servers.find_one(document):
        bot.db.servers.insert_one(document)

@_permissions.command(name='command', aliases=['c'])
async def _command(ctx, commandName, *args):
    if args[0] is None:
        serverData = getServerData(ctx.guild.id)
        permissions = getCommandData(serverData, commandName).get("permissions")
        await ctx.send(str(permissions))
    elif args[0] == 'user':
        updatePermissions(ctx.guild.id, f'commands.{commandName}.permissions.users.{args[1]}', args[2])
    elif args[0] == 'group':
        updatePermissions(ctx.guild.id, f'commands.{commandName}.permissions.groups.{args[1]}', args[2])
    else:
        updatePermissions(ctx.guild.id, f'commands.{commandName}.permissions.users.{args[0]}', args[1])

@_permissions.command(name='group', aliases=['g'])
async def _group(ctx, group = None, *args):
    serverData = getServerData(ctx.guild.id)
    if group is None:
        await ctx.send(serverData.get("groups"))
    elif empty(args):
        await ctx.send(multiget(serverData, "groups", group))
    elif args[0] == 'create':
        updateServersDb(ctx.guild.id, {"$set": {f'groups.{group}': []}})
    elif args[0] == 'remove':
        updateServersDb(ctx.guild.id, {"$unset": {f'groups.{group}': ''}})
    elif args[0] == 'add':
        updateServersDb(ctx.guild.id, {"$addToSet": {f'groups.{group}': int(args[1])}})
    elif args[0] == 'kick':
        pass

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
    commandData = getCommandData(serverData, commandName)
    commandPermissions = commandData.get("permissions")
    # do not run when disabled
    if notIfNotNone(commandData.get("enabled")):
        return False
    # do group check
    commandGroups = commandPermissions.get("groups")
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
    userCheck = multiget(commandPermissions, "users", str(user))
    if userCheck is not None:
        if not userCheck:
            return False
        elif notIfNotNone(commandPermissions.get("default")):
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
