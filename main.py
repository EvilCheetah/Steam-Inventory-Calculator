import time
import requests
import re
import json

#import CONST.URL
#import CONST.USER_DATA
from library.Item import item
from library.client import client
'''
def returnJSON():
    s = requests.Session()
    r = s.get(CONST.URL.INVENTORY.format(STEAM_ID64  = CONST.USER_DATA.STEAM_ID64,
                                         APP_ID      = CONST.USER_DATA.GAME_ID),
                            headers = CONST.URL.USER_HEADER,
                            params  = CONST.URL.COOKIE)
    print(r)
    if (r.status_code != "429"):
        inventoryJSON = r.json()
        userJson = json.dumps(inventoryJSON)
        with open("{}.json".format(CONST.USER_DATA.GAME_ID), 'w') as fout:
            fout.write(userJson)
    else:
        with open("{}.json".format(CONST.USER_DATA.GAME_ID), 'r') as fin:
            data = fin.read()

        inventoryJSON = json.loads(data)

    return inventoryJSON
'''
#user_inventory = returnJSON()

client().getItems(252490)

"""
userItemsDescription    = user_inventory["rgDescriptions"]
allUserItems            = user_inventory["rgInventory"]

itemsID             = {}
RustItems           = {}

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
