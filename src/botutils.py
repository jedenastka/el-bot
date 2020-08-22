import discord

import datetime

from instances import db

def getPrefix(message, all=False):
    prefixes = db['system'].find_one({'special': 'default'})['bot']['prefixes']
    if all:
        return prefixes
    for prefix in prefixes:
        if message.content.startswith(prefix):
            return prefix
    return None

def mergeDicts(local, overlay):
    for key in overlay:
        if isinstance(local, dict) and isinstance(overlay, dict):
            if isinstance(local.get(key), dict) and isinstance(overlay.get(key), dict):
                local[key] = mergeDicts(local[key], overlay[key])
            elif isinstance(local.get(key), list) and isinstance(overlay.get(key), list):
                local[key] += overlay[key]
            else:
                local[key] = overlay[key]
        else:
            local = overlay
    
    return local

def getDefaultDoc(path=[]):
    doc = db['system'].find_one({'special': 'default'})

    doc.pop('_id')
    doc.pop('special')
    
    for element in path:
        doc = doc.get(element, {})
        if doc == {}:
            break
    
    return doc

def getSettingsDoc(path=[]):
    doc = db['system'].find_one({'special': 'settings'})

    doc.pop('_id')
    doc.pop('special')
    
    for element in path:
        doc = doc.get(element, {})
        if doc == {}:
            break
    
    return doc

def getOverlayDoc(path=[]):
    doc = db['system'].find_one({'special': 'overlay'})

    doc.pop('_id')
    doc.pop('special')
    
    for element in path:
        doc = doc.get(element, {})
        if doc == {}:
            break
    
    return doc

def getServerDoc(serverId: int, path=[], addOverlay=False):
    doc = db['servers'].find_one({'id': serverId})

    doc.pop('_id')

    if addOverlay:
        doc = mergeDicts(doc, getOverlayDoc())
    
    for element in path:
        doc = doc.get(element, {})
        if doc == {}:
            break
    
    return doc

def updateServerDoc(serverId: int, doc: dict, path=[]):
    dotPath = '.'.join(path)

    db['servers'].update_one({'id': serverId}, {'$set': {dotPath: doc}})

def createEmbed(title={'text': 'El'}, content='', color=discord.Colour(0), footer={}, image=discord.Embed.Empty, thumbnail=discord.Embed.Empty, author={}, fields=[]):
    titleText = ''
    titleUrl = None
    if isinstance(title, dict):
        if title.get('text') is not None:
            titleText = title['text']
        if title.get('url') is not None:
            titleUrl = title['url']
    
    if not isinstance(color, discord.Colour):
        color = discord.Colour(0)

    footerText = discord.Embed.Empty
    footerIcon = discord.Embed.Empty
    if isinstance(footer, dict):
        if footer.get('text') is not None:
            footerText = title['text']
        if footer.get('icon') is not None:
            footerIcon = title['icon']

    authorText = ''
    authorUrl = discord.Embed.Empty
    authorIcon = discord.Embed.Empty
    if isinstance(footer, dict):
        if author.get('text') is not None:
            authorText = author['text']
        if author.get('url') is not None:
            authorUrl = author['url']
        if author.get('icon') is not None:
            authorIcon = author['icon']

    embed = discord.Embed(title=titleText, description=content, url=titleUrl, timestamp=datetime.datetime.now(), colour=color)
    embed.set_footer(text=footerText, icon_url=footerIcon)
    embed.set_image(url=image)
    embed.set_thumbnail(url=thumbnail)
    embed.set_author(name=authorText, url=authorUrl, icon_url=authorIcon)

    if isinstance(fields, list):
        for field in fields:
            if isinstance(field, dict):
                embed.add_field(name=field.get('name'), value=field.get('value'), inline=field.get('inline'))

    return embed