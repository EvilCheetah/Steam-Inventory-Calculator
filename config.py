import configparser
import library.CONST.URL as URL
import library.CONST.SteamData as SteamData


class config:
    def __init__(self, PATH: str):
        self.userConfig = configparser.ConfigParser()

        #to make return the keys in Uppercase
        #e.g. dota_2 will be returned as DOTA_2
        self.userConfig.optionxform = str
        self.userConfig.read(PATH)

        #Reading userCurrency and Changing it in CONST.URL for the rest of the program
        URL.CURRENCY = SteamData.CURRENCY[ self.userConfig["USER_DATA"]["CURRENCY"] ]["code"]

        print(URL.CURRENCY)
