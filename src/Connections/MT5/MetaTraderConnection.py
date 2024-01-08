import MetaTrader5 as mt5
import pandas as pd
from src.Connections.ConnectionInterface import ConnectionInterface
import JsonReader

class MetaTraderConnection(ConnectionInterface):
    # Paths to MetaTrader5 login details.
    credentials = JsonReader("pkg/credentials.json")
    json_settings = JsonReader("pkg/settings.json")

    _connection = None;

    def __new__(cls):
        if cls._connection is None:
            cls._connection = super(MetaTraderConnection, cls).__new__(cls)
        return cls._connnection
    
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
            raise 
    
    def get_candles_for_symbol(self, symbol, timeframe, num_candlesticks) -> pd.DataFrame:
        return mt5.copy_rates_from_pos(symbol, timeframe, self.start_pos, num_candlesticks)
        
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