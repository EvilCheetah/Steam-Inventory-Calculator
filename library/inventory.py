from .client import client
from .CONST import SteamData
from .CONST import SearchPatterns
from .item import Item

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



###------------Read Config Functions------------###
###
###     These functions read the data from the
###     config files, in order to customize the
###     program for the user, as well as ingore
###     some unnecessary items.

    def readGames(self):
        for key in self.config["GAMES"]:
            if (self.config["GAMES"][key] == "True"):
                self.games.append( key )

    def readIgnoredItems(self):
        PATH = self.config["DEFAULT"]["ITEM_PROPERTIES"]

        #Read the Properties
        with open(PATH, 'r') as fin:
             ignoreList = json.loads( fin.read() )

        #Just for clarification
        self.avoidItems = {}

        #Loop over the Games
        for game, properties in ignoreList.items():
            #If game doesn't exist in class Variable
            #Don't waste time
            if ( game not in self.games ):
                continue

            #Create a game in dict
            self.avoidItems[game] = {}

            #Loop over Properties in Games
            for property, parameters in properties.items():

                #Array for Quality, Type
                ignoreArray = []

                #Dictionary for Price
                ignoreDict  = {}

                #Loop over the Elements in Properties
                for parameter, value in parameters.items():
                    #Append ignored element into the array
                    if ( value == "False" ):
                        ignoreArray.append(parameter)
                        continue

                    #Records a Lower Margin
                    elif ( parameter == "LOWER_MARGIN"):
                        #Ignore Lower Margin if
                        if ( float(value) < 0 or value == "False" or value == "None"):
                            continue

                        ignoreDict[parameter] = float(value)

                    #Records an Upper Margin
                    elif ( parameter == "UPPER_MARGIN"):
                        #Ignore Upper Margin if:
                        if ( value == "INF" or value == False ):
                            continue

                        ignoreDict[parameter] = float(value)

                #Record the Dictionary if there is a data
                if ( ignoreDict ):
                    self.avoidItems[game][property] = ignoreDict
                    continue

                #If Dictionary is empty => Array is not
                else:
                    self.avoidItems[game][property] = ignoreArray



###------------File Output Function------------###
###
###     This is Debug Use function implemented,
###     because of the large size of inventories
###     of some users and malfuncion of console
###     to output all items.

    def outputItemList(self):
        with open("out.txt", 'w') as fout:
            for game in self.userItems.values():
                for item in game:
                    out = str(item)
                    fout.write(out)
                    fout.write('\n\n')



###------------Main Body Function------------###
###
###     Returns a Dictionary based on user's
###     config, with such outline:
###     {
###        "game1": [item1, item2, ...],
###        "game2": [item1, item2, ...],
###        ...
###     }

    def getInventoryList(self):
        for game in self.games:
            #Gets a inventory JSON
            inventory = client().getItems(userID64 = self.userID, gameID = SteamData.GAME_ID[ game ])

            #If Empty => No items ( if cookie is specified )
            if ( not inventory ):
                self.userItems[game] = {}
                continue

            inventory = self.processInventory(game, inventory)

            #Convert to array
            inventory = list(inventory)

            self.userItems[game] = inventory

        self.outputItemList()



###------------Inventory Processing Funcions------------###
###
###     Each function handles each individual game.
###     Every inventory outline is different and using
###     a single function would cause errors, need
###     adjustments or complicate code and its
###     readability.

    def processInventory(self, game, inventory):
        items = {}

        itemQuantity     = inventory["rgInventory"]
        itemDescription  = inventory["rgDescriptions"]

        if   ( game == "CSGO"):
            items = self.processCSGOItems(itemDescription)

        elif ( game == "DOTA_2"):
            items = self.processDOTA2Items(itemDescription)

        elif ( game == "RUST"):
            items = self.processRUSTItems(itemDescription)


        ## TODO: Add other items
        elif ( game == "UNTURNED"):
            pass

        elif ( game == "DST" ):
            pass

        elif ( game == "TF2" ):
            pass

        #Count all items based on Description
        for individualItem in itemQuantity.values():
            if ( individualItem["classid"] in items ):
                items[ individualItem["classid"] ].quantity += int(individualItem["amount"])

        return items.values()

    def processCSGOItems(self, items):
        itemList = {}

        for item in items.values():
            #Get Basics
            itemName       = item["name"]
            itemID         = item["classid"]
            itemMarketName = item["market_hash_name"]

            #Get Quality
            itemQuality    = re.search(re.compile(SearchPatterns.CSGO["QUALITY"]), item["type"]).group()
            if ( itemQuality in self.avoidItems["CSGO"]["QUALITY"] ):
                continue

            #Get Type
            itemType       = re.search(re.compile(SearchPatterns.CSGO["TYPE"]),    item["type"]).group()
            if ( itemType in self.avoidItems["CSGO"]["TYPE"] ):
                continue

            #Get Tradable State
            isTradable     = True if ( item["tradable"]   == 1 ) else False
            if ( (not isTradable) and ("TRADABLE" in self.avoidItems["CSGO"]["ITEM_PROPERTY"]) ):
                continue

            #Get Marketable State
            isMarketable   = True if ( item["marketable"] == 1 ) else False
            if ( (not isMarketable) and ("MARKETABLE" in self.avoidItems["CSGO"]["ITEM_PROPERTY"]) ):
                continue

            item = Item(game        = "CSGO",
                        item_name   = itemName,
                        item_id     = itemID,
                        market_name = itemMarketName,
                        quality     = itemQuality,
                        type        = itemType,
                        tradable    = isTradable,
                        marketable  = isMarketable
                        )

            self.getAverageWeekPrice(item)

            if ( not self.withinPriceRange(item) ):
                continue

            itemList[itemID] = item

        return itemList

    def processDOTA2Items(self, items):
        itemList = {}

        for item in items.values():
            #Get Basics
            itemName       = item["name"]
            itemID         = item["classid"]
            itemMarketName = item["market_hash_name"]

            #Gets Quality
            itemQuality    = re.search(re.compile(SearchPatterns.DOTA_2["QUALITY"]), item["type"]).group()
            if ( itemQuality in self.avoidItems["DOTA_2"]["QUALITY"] ):
                continue


            #Removes the Quality with Space(\s or ' ') and titles
            itemType       = re.sub(itemQuality + ' ', '', item["type"]).title()
            if ( itemType in self.avoidItems["DOTA_2"]["TYPE"] ):
                continue

            isTradable     = True if ( item["tradable"]   == 1 ) else False
            if ( (not isTradable) and ("TRADABLE" in self.avoidItems["DOTA_2"]["ITEM_PROPERTY"]) ):
                continue

            isMarketable   = True if ( item["marketable"] == 1 ) else False
            if ( (not isMarketable) and ("MARKETABLE" in self.avoidItems["DOTA_2"]["ITEM_PROPERTY"]) ):
                continue

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

    def processRUSTItems(self, items):
        itemList = {}

        for item in items.values():
            #Get Basics
            itemName       = item["name"]
            itemID         = item["classid"]
            itemMarketName = item["market_hash_name"]

            #Get Quality
            #Get last element of tags and its name
            itemQuality    = item["type"]
            if ( itemQuality in self.avoidItems["RUST"]["QUALITY"] ):
                continue

            #Get Type
            itemType    = item["tags"][-1]["name"]
            if ( itemType in self.avoidItems["RUST"]["TYPE"]):
                continue

            #Get Tradable State
            isTradable     = True if ( item["tradable"]   == 1 ) else False
            if ( (not isTradable) and ("TRADABLE" in self.avoidItems["RUST"]["ITEM_PROPERTY"]) ):
                continue

            #Get Marketable State
            isMarketable   = True if ( item["marketable"] == 1 ) else False
            if ( (not isMarketable) and ("MARKETABLE" in self.avoidItems["RUST"]["ITEM_PROPERTY"]) ):
                continue

            itemList[itemID] = Item(game        = "RUST",
                                    item_name   = itemName,
                                    item_id     = itemID,
                                    market_name = itemMarketName,
                                    quality     = itemQuality,
                                    type        = itemType,
                                    tradable    = isTradable,
                                    marketable  = isMarketable
                                    )

        return itemList



###-------Additional Funcions for Calculations-------###
###
###     These functions are implemented to make
###     code more readable.

    def withinPriceRange(self, item):
        #   avgPrice <= LOWER_MARGIN
        if ( "LOWER_MARGIN" in self.avoidItems[item.gameName]["PRICE"] ):
            if ( item.averagePrice <= self.avoidItems[item.gameName]["PRICE"]["LOWER_MARGIN"] ):
                #NOT IN RANGE!
                return False

        #   UPPER_MARGIN <= avgPrice
        if ( "UPPER_MARGIN" in self.avoidItems[item.gameName]["PRICE"] ):
            if ( item.averagePrice >= self.avoidItems[item.gameName]["PRICE"]["UPPER_MARGIN"] ):
                #NOT IN RANGE!
                return False

        return True

    def getAverageWeekPrice(self, item):
        #If item is not MARKETABLE
        #Then there is no listing on Marketplace
        if ( not item.isMarketable ):
            return

        item.averagePrice = client().getAverageItemPrice(item)
