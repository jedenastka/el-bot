import discord
from discord.ext import commands
import pymongo
import json, os
import secrets

# make cache directory
os.makedirs('cache', exist_ok=True)

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

@bot.command(name='config')
async def _config(ctx):
    server = ctx.guild
    document = {"id": server.id}
    bot.db.servers.insert_one(document)

def dictReturnIfUsable(dictionary, *path):
    try:
        temp = dictionary
        for i in path:
            temp = temp[i]
        return temp
    except:
        return None

# check
@bot.check
async def globalCheck(ctx):
    commandName = ctx.command.qualified_name
    serverData = bot.data["default"]
    serverDataDb = bot.db.servers.find_one({"id": ctx.guild.id})
    if serverDataDb != None:
        serverData.update(serverDataDb)
    serverData.update(bot.data["global"])
    if commandName in serverData["commands"]:
        commandData = serverData["commands"][commandName]
    else:
        commandData = serverData["commandDefault"]
    commandPermisions = commandData.get("permisions")
    if dictReturnIfUsable(commandData, "enabled") == 0:
        return False
    if dictReturnIfUsable(commandPermisions, "users", str(ctx.message.author.id)) == 0:
        return False
    elif dictReturnIfUsable(commandPermisions, "default") == 0:
        return False
    commandGroups = commandPermisions.get("groups")
    if commandGroups != None:
        groups = serverData["groups"]
        userGroups = []
        for group in groups.items():
            if ctx.message.author.id in group[1]:
                userGroups.append(group[0])
        # this part is probably broken
        groupCheck = 0 if userGroups != [] else 1
        for group in userGroups:
            if groups[group] == 1:
                groupCheck = 1
        if not groupCheck:
            return False
    return True

# load plugins
for plugin in bot.data["plugins"]:
    bot.load_extension(bot.data["pluginPath"] + plugin)

bot.run(secrets.token, bot=True, reconnect=True)