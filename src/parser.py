from botutils import getPrefix
from instances import events

def splitNoBreak(string: str):
    splittedString = []
    tmp = ''
    inQuotes = False

    for i in range(len(string)):
        ch = string[i]
        previousCh = string[i - 1] if i != 0 else ''
        nextCh = string[i + 1] if i != len(string) - 1 else ''
        chIsQuote = False
        
        if ch in ('"', '\''):
            if not inQuotes and previousCh == ' ':
                inQuotes = True
                chIsQuote = True
            elif inQuotes and nextCh in (' ', ''):
                inQuotes = False
                chIsQuote = True
        
        if (ch != ' ' or inQuotes) and not chIsQuote:
            tmp += ch
        
        if (ch == ' ' and not inQuotes) or nextCh == '':
            splittedString.append(tmp)
            tmp = ''
        
        if nextCh == '' and inQuotes:
            raise Exception('Unclosed quote')
    
    return splittedString

def findCommand(parts):
    commands = events
    
    i = 1
    
    for part in parts:
        for command in commands:
            if command['type'] == 'command' and part in command['aliases'] + [command['name']]:

                commands = command.get('subcommands', [])
                
                lastSubcommand = True
                for partLeft in parts[i:]:
                    for commandLeft in commands:
                        if partLeft in commandLeft['aliases'] + [commandLeft['name']]:
                            lastSubcommand = False
                
                if commands == [] or lastSubcommand:
                    return (command, parts[i:])
                
                break
        
        i += 1
    
    return ({}, [])

def getCommand(message):
    prefix = getPrefix(message)
    if prefix is not None:
        commandString = message.content[len(prefix):]

        try:
            parts = splitNoBreak(commandString)
        except Exception:
            return ({}, [])

        command, args = findCommand(parts)

        return command, args

    return ({}, [])