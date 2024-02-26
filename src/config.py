import sys

# Path to MetaTrader5 login details.
ACCOUNT_SETTINGS_PATH = "pkg/settings.json"
CREDENTIALS_FILE_PATH = "pkg/credentials.json"

EMA_SHORT = 500
EMA_LONG = 1000

PRODUCTION = False # added for convenience, all factories eventually created in main and passed to trade_bot

class Config():

    def __init__(self, args: list) -> None:
        # NOTE: Args Key:
        # 1 - symbol name OR settings
        # 2 - Production flag, 1 == True, 0 == False
        # Example: BTCUSD 1
        try:
            filepath: str = "pkg/" + sys.argv[1] + ".json"
            production: int = int(sys.argv[2])
            ema_short: int = int(sys.argv[3])
            ema_long: int = int(sys.argv[4])
        except:
            filepath: str = ACCOUNT_SETTINGS_PATH
            production: bool = PRODUCTION
            ema_short = EMA_SHORT
            ema_long = EMA_LONG


        