from .client import client
from .CONST import SteamData
from time import sleep

class inventory:
    def __init__(self, config):
        self.config         = config
        self.userID         = config["USER_DATA"]["STEAM_ID64"]
        self.userCurrency   = config["USER_DATA"]["CURRENCY"]
        self.games          = []
        self.userItems      = {}

        self.readGames()
        
    def readGames(self):
        for key in self.config["GAMES"]:
            if (self.config["GAMES"][key] == "True"):
                self.games.append( key )

    def getInventoryList(self):
        for game in self.games:
            itemList = client().getItems(userID64 = self.userID, gameID = SteamData.gamesID[ game ])

            if ( not itemList ):
                self.userItems[game] = {}
                continue

            itemList = self.processInventory(itemList)

    def processInventory(self, gameUserInventory):
        items            = gameUserInventory["rgInventory"]
        itemDescription  = gameUserInventory["rgDescriptions"]




"""
for key, value in userItemsDescription.items():
    itemsID[ value["classid"] ] = {
            "name":         value["name"],
            "M_H_N":        value["market_hash_name"]
    }
    #"category":     value["tags"][0]["name"] if 1 not in value["tags"] else value["tags"][1]["name"],
    if '1' in value["tags"]:
        print("1st Exists")
    else:
        print("there is no element with key 1")
    #print(category)
    #"M_H_N":         value["market_hash_name"]
    #
    #itemsID[ value["classid"] ]["trade"]

for key, value in allUserItems.items():
    if value["classid"] not in RustItems:
        item_name = itemsID[ value["classid"] ]
        item_quantity  = int(value["amount"])
        singleItem = item(game     = "Rust", itemName = item_name,
                          quantity = item_quantity, itemID = value["classid"])

        RustItems[ value["classid"] ] = singleItem

    else:
        item_quantity = int( value["amount"] )
        RustItems[ value["classid"] ].quantity += item_quantity

for key, value in RustItems.items():
    print(value)
"""
