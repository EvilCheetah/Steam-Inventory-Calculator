import requests
import json

from .CONST import URL


class client:
    #gets user's inventory as a json
    def getItems(self, userID64, gameID):

        #need a cookie["steamLoginSecure"] in order to
        #avoid StatusCode 429 - Forbidden
        r = requests.post(URL.INVENTORY.format(STEAM_ID64   = userID64,
                                               APP_ID       = gameID),
                          cookies = URL.COOKIE
                         )

        #If connection is not Forbidden => Read and Cache
        if (r.status_code != 429):
            userInventory = r.json()

            #Either:
            # 1) Status Code == 429 (Forbidden)
            # 2) User Doesn't have items from the game
            #
            # Assuming #2, since cookie is specified
            if (userInventory["success"] == "false"):
                return {}

            self.cacheInventory(gameID, userInventory)

        #Otherwise read from the file
        else:
            userInventory = self.uncacheInventory(gameID)

        return userInventory

    #Saves an inventory as a JSON file
    #PATH: /json/
    def cacheInventory(self, gameID, inventory):
        with open("json/{}.json".format(gameID), 'w') as fout:

            #If inventory is not empty => dump
            if inventory:
                fout.write( json.dumps(inventory) )
            else:
                fout.write("{}")

    #Reads the inventory from local JSON
    def uncacheInventory(self, gameID):
        try:
            with open("json/{}.json".format(gameID), 'r') as fin:
                inventory = json.loads( fin.read() )

            return inventory

        except FileNotFoundError:
            print("There is not file Cached for Game: {}".format(gameID))
            return {}
