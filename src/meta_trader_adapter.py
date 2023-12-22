import MetaTrader5 as mt5
import pandas as pd

from src.interfaces import IMetaTrader, Trade
from src.symbols_adapter import SymbolsAdapter
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

    def execute_trade(self, trade: Trade):
        return "Traded!"