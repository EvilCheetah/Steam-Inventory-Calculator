from .CONST import SteamData

class Item:
    def __init__(self,
                 game               = None,
                 item_name          = None,
                 item_id            = None,
                 market_name        = None,
                 quality            = None,
                 type               = None,
                 tradable           = None,
                 marketable         = None,
                 quantity           = 0):

        self.gameName     = game
        self.gameID       = SteamData.GAME_ID[game] if game else None
        self.itemName     = item_name
        self.itemID       = item_id
        self.marketName   = market_name

        #Quality == Rarity
        self.quality      = quality

        #Type == Item Class
        self.type         = type

        self.isTradable   = tradable
        self.isMarketable = marketable

        #Quantity == Amount
        self.quantity     = quantity

    def __str___(self):
        return ("{name}\n"
                "Item ID    - {id}\n"
                "Quality    - {quality}\n"
                "Type       - {type}\n"
                "Tradable   - {tradable}\n"
                "Marketable - {marketable}\n"
                "You Own    - {quantity}\n").format(name          = self.itemName,
                                                    id            = self.itemID,
                                                    quality       = self.quality,
                                                    type          = self.type,
                                                    tradable      = self.isTradable,
                                                    marketable    = self.isMarketable,
                                                    quantity      = self.quantity)


    #Cannot replace with:
    #   return self.__str__()
    #Because of const recursion
    def __repr__(self):
        return ("{name}\n"
                "Item ID    - {id}\n"
                "Quality    - {quality}\n"
                "Type       - {type}\n"
                "Tradable   - {tradable}\n"
                "Marketable - {marketable}\n"
                "You Own    - {quantity}\n").format(name          = self.itemName,
                                                    id            = self.itemID,
                                                    quality       = self.quality,
                                                    type          = self.type,
                                                    tradable      = self.isTradable,
                                                    marketable    = self.isMarketable,
                                                    quantity      = self.quantity)
