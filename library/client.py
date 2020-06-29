import requests
import json

from .CONST import URL
from .CONST import USER_DATA
from .Item import item


class client:
    def __init__(self):
        pass

    def getItems(self, gameID):
        r = requests.post(URL.INVENTORY.format(STEAM_ID64   = USER_DATA.STEAM_ID64,
                                               APP_ID       = gameID),
                          data = URL.COOKIE
                         )
        print(r)

        if (r.status_code != '429'):
            userInventory = r.json()
            self.cacheInventory(gameID, userInventory)

        else:
            userInventory = self.uncacheInventory(gameID)

    def cacheInventory(self, gameID, inventory):
        with open("json/{}.json".format(gameID), 'w') as fout:
            if inventory:
                fout.write( json.dumps(inventory) )
            else:
                fout.write("{}")

    def uncacheInventory(self, gameID):
        try:
            with open("json/{}.json".format(gameID), 'r') as fin:
                inventory = json.loads( fin.read() )

            return inventory

        except FileNotFoundError:
            print("There is not file Cached")
            return {}
