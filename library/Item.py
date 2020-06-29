from .CONST import gameID

class item:
    def __init__(self,
                 game               = None,
                 itemName           = None,
                 quantity           = 0,
                 itemID             = None,
                 market_hash_name   = None,
                 category           = None):

        self.gameName = game
        self.gameID   = gameID.gameList[game] if game else None
        self.itemName = itemName
        self.quantity = quantity
        self.itemID   = itemID
        self.market_hash_name = market_hash_name
        self.category = category

    def __str___(self):
        return ("{name}  -  {quantity}\n"
                "Item ID = {id}\n").format(name     = self.itemName,
                                           quantity = self.quantity,
                                           id       = self.itemID)

    def __repr__(self):
        return ("{name}   -  {quantity}\n"
                "Item ID  =  {id}\n"
                "Category -  {category}").format(name     = self.itemName,
                                                 quantity = self.quantity,
                                                 id       = self.itemID,
                                                 category = self.category)
