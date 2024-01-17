import abc
import pandas as pd

from datetime import timezone

class AbstractSymbols(abc.ABC):

    candles_df: pd.DataFrame
    current_time: timezone
    mt5_timeframe: int
    symbol: str 
    timeframe: str

    start_pos = 0

    def __init__(self, symbol, timeframe):
        self.symbol = symbol
        self.timeframe = timeframe
        
    def get_symbol_name(self) -> str:
        return self.symbol
    
    def get_symbol_info_bid(self) -> float:
        symbol_info_tick = self.get_symbol_info_tick()
        symbol_info_bid = symbol_info_tick['bid']
        return symbol_info_bid

    def get_symbol_info_ask(self) -> float:
        symbol_info_tick = self.get_symbol_info_tick()
        symbol_info_ask = symbol_info_tick['ask']
        return symbol_info_ask
    
    @abc.abstractmethod
    def get_candlesticks(self, num_candlesticks) -> object:
        pass

    @abc.abstractmethod
    def get_candlestick_time(self) -> int:
        pass

    @abc.abstractmethod
    def get_symbol_info_tick(self) -> dict:
        pass
