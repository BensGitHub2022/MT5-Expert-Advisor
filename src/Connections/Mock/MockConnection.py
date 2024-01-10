import pandas as pd

from src.Connections.ConnectionInterface import ConnectionInterface
from src.Connections.Mock.MockDataSource import MockDataSource

class MockConnection(ConnectionInterface):
    symbol_tracker_map = {}

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
        if symbol not in self.symbol_tracker_map:
            self.symbol_tracker_map[symbol] = MockDataSource(symbol, timeframe)
    
        return self.symbol_tracker_map[symbol].get_next_candle_set(num_candlesticks)
        
    def get_ticks_for_symbol(self, symbol, num_ticks) -> pd.DataFrame:
        if symbol not in self.symbol_tracker_map:
            self.symbol_tracker_map[symbol] = MockDataSource(symbol, num_ticks)
    
        return self.symbol_tracker_map[symbol].get_next_tick_set()
    
    def get_symbol_info() -> str:
        return ""
    
    def send_order():
        # to-do
        # MockBank.send_order()
        return 0
    
    def cancel_order():
        #to-do
        return 0