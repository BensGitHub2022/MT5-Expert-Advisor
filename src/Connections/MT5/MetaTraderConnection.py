from enum import Enum
import MetaTrader5 as mt5
import pandas as pd
from src.CommonEnums.Timeframe import Timeframe
from src.Connections.ConnectionInterface import ConnectionInterface
from src.Connections.MT5.JsonReader import JsonReader

class MetaTraderConnection(ConnectionInterface):
    # Paths to MetaTrader5 login details.
    credentials = JsonReader("src/Connections/MT5/credentials.json").get_json_data()
    json_settings = JsonReader("pkg/settings.json").get_json_data()

    def __init__(self):
        self.connect()
    
    """
    Attempts to initialize and log into MetaTrader5.
    :returns bool: True if initialization and login succeeds. Otherwise, false.
    """
    def connect(self) -> bool:

        try:
            pathway = self.credentials["mt5"]["terminal_pathway"]
            login = self.credentials["mt5"]["login"]
            password = self.credentials["mt5"]["password"]
            server = self.credentials["mt5"]["server"]
            timeout = self.json_settings["mt5"]["timeout"]

            mt5.initialize(
                pathway, login=login, password=password, server=server, timeout=timeout
            )
            print("Trading bot initialized!")

            # Safe to login here. Returns true if login succeeds. Otherwise, returns false.
            mt5.login(
                login=login, password=password, server=server, timeout=timeout
            )
            print("Trading bot login successful!")

        except KeyError as e:
            print(f"The queried dictionary key does not exist: {e.args}")
            raise e
        except ConnectionError as e:
            print(f"Could not connect to MetaTrader5: {e.args}")
            raise e
        except PermissionError as e:
            print(f"Login failed to connect to MetaTrader 5: {e.args}")
            raise 
    
    def get_candles_for_symbol(self, symbol, timeframe, num_candlesticks) -> pd.DataFrame:
        try:
            if timeframe == Timeframe.one_minute:
                return pd.DataFrame(mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, num_candlesticks))
            return None
        except Exception as e:
            print(e)
            raise
        
    def get_ticks_for_symbol(self, symbol, num_ticks) -> pd.DataFrame:
        ticks = mt5.copy_ticks_from(symbol, self.current_time, num_ticks, mt5.COPY_TICKS_ALL)
        return pd.DataFrame(ticks)
    
    def get_symbol_info(self, symbol) -> str:
        return mt5.symbol_info(symbol)._asdict()
    
    def send_order():
        # to-do
        return 0
    
    def cancel_order():
        #to-do
        return 0
    
    def get_account_balance() -> int:
        #to-do
        return 0
