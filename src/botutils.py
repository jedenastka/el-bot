from instances import db

def getPrefix(message, all=False):
    prefixes = db['system'].find_one({'special': 'default'})['bot']['prefixes']
    if all:
        return prefixes
    for prefix in prefixes:
        if message.content.startswith(prefix):
            return prefix
    return None