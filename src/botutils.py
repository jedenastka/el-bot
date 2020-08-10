from instances import db

def getPrefix(message, all=False):
    prefixes = db['system'].find_one({'special': 'default'})['bot']['prefixes']
    if all:
        return prefixes
    for prefix in prefixes:
        if message.content.startswith(prefix):
            return prefix
    return None

def getOverlayDoc(path=[]):
    doc = db['system'].find_one({'special': 'global'})
    
    for element in path:
        doc = doc.get(element, {})
        if doc == {}:
            break
    
    return doc

def getServerDoc(serverId: int, path=[], addOverlay=False):
    doc = db['servers'].find_one({'id': serverId})
    if addOverlay:
        doc = {**doc, **getOverlayDoc()}
    
    for element in path:
        doc = doc.get(element, {})
        if doc == {}:
            break
    
    return doc

def updateServerDoc(serverId: int, doc: dict, path=[]):
    path.reverse()
    for element in path:
        doc = {element: doc}

    db['servers'].update_one({'id': serverId}, {'$set': doc})