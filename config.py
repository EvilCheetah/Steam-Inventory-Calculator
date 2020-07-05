import configparser

class config:
    def __init__(self, PATH: str):
        self.userConfig = configparser.ConfigParser()

        #to make return the keys in Uppercase
        #e.g. dota_2 will be returned as DOTA_2
        self.userConfig.optionxform = str

        self.userConfig.read(PATH)
