Delimeters = [',', '.', ' ']

CURRENCY   = 0

USER_HEADER          = {"User-Agent": "Mozilla/5.0 (Linux; Android 10; SC-01M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/11.2 Chrome/75.0.3770.143 Mobile Safari/537.36"}
COOKIE               = {"steamLoginSecure":  ""}


INVENTORY            = ("https://steamcommunity.com/profiles/{STEAM_ID64}/inventory/json/{APP_ID}/2")

MARKET_LISTING 	     = ("https://steamcommunity.com/market/priceoverview/?appid={APP_ID}&market_hash_name={ITEM_NAME}&currency={CURRENCY_ID}")

MARKET_PRICE_HISTORY = ("https://steamcommunity.com/market/pricehistory/?appid={APP_ID}&market_hash_name={ITEM_NAME}&currency={CURRENCY_ID}")
