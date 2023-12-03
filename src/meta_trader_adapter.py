import MetaTrader5 as mt5
import pandas as pd

from src.interfaces import IMetaTrader, Trade
from src.candlesticks import Candlesticks
from src.json_reader import JsonReader

class MetaTraderAdapter(IMetaTrader):
    something: float

    symbol: str 
    timeframe: str 

    json_settings: dict
    credentials: dict

    def __init__(self):
        self.something = 0

    def connect(self, json_settings: dict, credentials: dict) -> bool:
        """
        Attempts to initialize and log into MetaTrader5.
        :param json_settings: A dict containing MetaTrader5 login details.
        :returns bool: True if initialization and login succeeds. Otherwise, false.
        """
        
        self.json_settings = json_settings
        self.credentials = credentials

        try:
            pathway = self.credentials["mt5"]["terminal_pathway"]
            login = self.credentials["mt5"]["login"]
            password = self.credentials["mt5"]["password"]
            server = self.credentials["mt5"]["server"]
            timeout = self.json_settings["mt5"]["timeout"]

            initialized = mt5.initialize(
                pathway, login=login, password=password, server=server, timeout=timeout
            )
            if initialized:
                print("Trading bot initialized!")
            else:
                raise ConnectionError

            # Safe to login here. Returns true if login succeeds. Otherwise, returns false.
            logged_in = mt5.login(
                login=login, password=password, server=server, timeout=timeout
            )

            if logged_in:
                print("Trading bot login successful!")
            else:
                raise PermissionError

        except KeyError as e:
            print(f"The queried dictionary key does not exist: {e.args}")
            raise e
        except ConnectionError as e:
            print(f"Could not connect to MetaTrader5: {e.args}")
            raise e
        except PermissionError as e:
            print(f"Login failed to connect to MetaTrader 5: {e.args}")
            raise e
        
        return True

    def set_candlesticks(self, symbol: str, timeframe: str) -> None:
        self.symbol = symbol
        self.timeframe = timeframe

    def get_seed(self, seed_count) -> object:
        c = self.get_candlesticks(seed_count)
        df = c.get_candles_dataframe()
        return df

    def get_next(self) -> object:
        c = self.get_candlesticks(1)
        df = c.get_candles_dataframe()
        return df

    def get_candlesticks(self, num_candlesticks) -> Candlesticks:
        c = Candlesticks(self.symbol,self.timeframe,num_candlesticks)
        return c
    
    def check_if_next(self, current_time) -> bool:
        new_candle = self.get_candlesticks(1)
        new_candle = new_candle.get_candles_dataframe()
        time_per_candle = new_candle['time'][0]
        if(current_time != time_per_candle):
            return True
        else:
            return False

    def execute_trade(self, trade: Trade):
        return "Traded!"
    
