from library.inventory import inventory
from config import config


if ( __name__ == "__main__" ):
    try:
        userConfig = config("CONFIG.cfg").userConfig

        inventory( userConfig ).getInventoryList()

    except KeyboardInterrupt:
        print("Program Terminated...")
