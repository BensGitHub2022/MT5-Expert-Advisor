from src.json_reader import JsonReader

# Path to MetaTrader5 login details.
ACCOUNT_SETTINGS_PATH = "config/settings.json"
CREDENTIALS_FILE_PATH = "config/credentials.json"

EMA_SHORT = 500
EMA_LONG = 1000

PRODUCTION = False # added for convenience, all factories eventually created in main and passed to trade_bot

class Config():

    filepath: str
    production: int
    ema_long: int
    ema_short: int
    symbol: str
    timeframe: str
    candlesticks_filepath: str
    ticks_filepath: str
    credentials: dict

    json_reader: JsonReader

    def __init__(self, args: list) -> None:
        # NOTE: Args Key:
        # 1 - symbol name OR settings => 0 in args[] list!
        # 2 - Production flag, 1 == True, 0 == False => 1 in args[] list!
        # 3 - EMA short == False => 2 in args[] list!
        # 4 - EMA long == False => 3 in args[] list!
        # Example: BTCUSD 1 500 1000
        try:
            self.filepath: str = "config/" + args[0] + ".json"
            self.production: int = int(args[1])
            self.ema_short: int = int(args[2])
            self.ema_long: int = int(args[3])
        except:
            self.filepath: str = ACCOUNT_SETTINGS_PATH
            self.production: bool = PRODUCTION
            self.ema_short = EMA_SHORT
            self.ema_long = EMA_LONG

        self.json_reader = JsonReader(self.filepath)
        
        self.symbol = self.json_reader.get_symbol()
        self.timeframe = self.json_reader.get_timeframe()
        if (self.production == False):
            self.candlesticks_filepath = self.json_reader.get_symbol_candlesticks_filepath()
            self.ticks_filepath = self.json_reader.get_symbol_ticks_filepath()
        else:
            self.candlesticks_filepath = ""
            self.ticks_filepath = ""

        self.credentials = JsonReader(file_path=CREDENTIALS_FILE_PATH).get_json_data()
        


        