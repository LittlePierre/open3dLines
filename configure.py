import configparser as ConfigParser


def getInt(section, name, default=0):
    global config
    try: return int(config.get(section, name))
    except: return default
def getStr(section, name, default=0):
    global config
    try: return str(config.get(section, name))
    except: return default
    
config    = ConfigParser.ConfigParser()

config.read("config.ini")
