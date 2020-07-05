from .client import client
from .CONST import SteamData
from .CONST import SearchPatterns
from .item import Item
from time import sleep
import json
import re

import pprint

class inventory:
    def __init__(self, config):
        self.config         = config
        self.userID         = config["USER_DATA"]["STEAM_ID64"]
        self.userCurrency   = config["USER_DATA"]["CURRENCY"]
        self.avoidItems     = {}
        self.games          = []
        self.userItems      = {}

        self.readGames()
        self.readIgnoredItems()

    #Adds the games into List that user wanted to track
    def readGames(self):
        for key in self.config["GAMES"]:
            if (self.config["GAMES"][key] == "True"):
                self.games.append( key )

    def readIgnoredItems(self):
        PATH = self.config["DEFAULT"]["ITEM_PROPERTIES"]
        with open(PATH, 'r') as fin:
             ignoreList = json.loads( fin.read() )

        self.avoidItems = {}

        for game, properties in ignoreList.items():
            if ( game not in self.games ):
                continue
            self.avoidItems[game] = {}

            for property, parameters in properties.items():
                ignoreArray = []

                for parameter, value in parameters.items():
                    if ( value == "False" ):
                        ignoreArray.append(parameter)

                self.avoidItems[game][property] = ignoreArray

        pp = pprint.PrettyPrinter(indent=4)
        pp.pprint(self.avoidItems)

    def outputItemList(self):
        with open("out.txt", 'w') as fout:
            for game in self.userItems.values():
                for item in game.values():
                    out = str(item)
                    fout.write(out)
                    fout.write('\n')

    def getInventoryList(self):
        for game in self.games:
            inventory = client().getItems(userID64 = self.userID, gameID = SteamData.GAME_ID[ game ])

            if ( not inventory ):
                self.userItems[game] = {}
                continue

            inventory = self.processInventory(game, inventory)

            self.userItems[game] = inventory

        #self.outputItemList()

    def processInventory(self, game, inventory):
        items = {}

        itemQuantity     = inventory["rgInventory"]
        itemDescription  = inventory["rgDescriptions"]

        if   ( game == "CSGO"):
            items = self.processCSGOItems(itemDescription)

        elif ( game == "DOTA_2"):
            items = self.processDOTA2Items(itemDescription)

        elif ( game == "RUST"):
            pass

        elif ( game == "UNTURNED"):
            pass

        elif ( game == "DST" ):
            pass

        elif ( game == "TF2" ):
            pass

        #Release WHEN all implementators are ready
        for individualItem in itemQuantity.values():
            items[ individualItem["classid"] ].quantity += int(individualItem["amount"])

        self.outputItemList()

        return items

    def processCSGOItems(self, items):
        itemList = {}

        for item in items.values():
            itemName       = item["name"]
            itemID         = item["classid"]
            itemMarketName = item["market_hash_name"]
            itemQuality    = re.search(re.compile(SearchPatterns.CSGO["QUALITY"]), item["type"]).group()
            itemType       = re.search(re.compile(SearchPatterns.CSGO["TYPE"]),    item["type"]).group()
            isTradable     = True if ( item["tradable"]   == 1 ) else False
            isMarketable   = True if ( item["marketable"] == 1 ) else False

            itemList[itemID] = Item(game        = "CSGO",
                                    item_name   = itemName,
                                    item_id     = itemID,
                                    market_name = itemMarketName,
                                    quality     = itemQuality,
                                    type        = itemType,
                                    tradable    = isTradable,
                                    marketable  = isMarketable
                                    )

        return itemList

    def processDOTA2Items(self, items):
        itemList = {}

        for item in items.values():
            itemName       = item["name"]
            itemID         = item["classid"]
            itemMarketName = item["market_hash_name"]
            itemQuality    = re.search(re.compile(SearchPatterns.DOTA_2["QUALITY"]), item["type"]).group()

            #Removes the Quality with Space(\s or ' ') and titles
            itemType       = re.sub(itemQuality + ' ', '', item["type"]).title()

            isTradable     = True if ( item["tradable"]   == 1 ) else False
            isMarketable   = True if ( item["marketable"] == 1 ) else False

            itemList[itemID] = Item(game        = "DOTA_2",
                                    item_name   = itemName,
                                    item_id     = itemID,
                                    market_name = itemMarketName,
                                    quality     = itemQuality,
                                    type        = itemType,
                                    tradable    = isTradable,
                                    marketable  = isMarketable
                                    )
            #print(itemList[itemID])

        return itemList
