import configparser as ConfigParser


def getInt(section, name, default=0):
    global config
    try: return int(config.get(section, name))
    except: return default
    
config    = ConfigParser.ConfigParser()

config.read("config.ini")
baud = getInt("Connection", "baud")
zozo = getInt("Zozo","zaza")
print(baud,type(baud))
print (zozo,type(zozo))