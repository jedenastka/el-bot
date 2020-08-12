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