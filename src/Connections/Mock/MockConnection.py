import pandas as pd

from src.Connections.AbstractConnection import AbstractConnection
from src.Connections.Mock.MockDataSource import MockDataSource

class MockConnection(AbstractConnection):
    symbol_candle_tracker_map = {}
    symbol_tick_tracker_map = {}

    def __init__(self):
        self.connect()
    
    """
    Attempts to initialize and log into MetaTrader5.
    :returns bool: True if initialization and login succeeds. Otherwise, false.
    """
    def connect(self) -> bool:
        print("Trading bot initialized!")
        print("Trading bot login successful!")
        return True
    
    def get_candles_for_symbol(self, symbol, timeframe, num_candlesticks) -> pd.DataFrame:
        if symbol not in self.symbol_candle_tracker_map:
            self.symbol_candle_tracker_map[symbol] = MockDataSource(symbol, timeframe)
    
        return self.symbol_candle_tracker_map[symbol].get_next_candle_set(num_candlesticks)
    
    def get_symbol_info() -> str:
        return ""
    
    def place_order(self, symbol, signal, volume, price, deviation) -> bool:
        # to-do
        # MockBank.send_order()
        return True
    
    def get_account_balance(self) -> float:
        return 10.0
    
    def get_ask_price(self, symbol) -> int:
        return 10
    
    def get_bid_price(self, symbol) -> int:
       return 10
   
    def get_positions(self) -> dict:
        return {}
    
    