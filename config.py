from configparser import ConfigParser

config = ConfigParser()

config.read('config.ini')
sections = config.sections()
for section in sections:
    
    options = config.options(section)
    
    for option in options:
        
        value=config.get(section,option)
        print(option,value)