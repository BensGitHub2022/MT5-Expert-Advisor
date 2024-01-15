import pandas as pd

class AbstractConnection():
    """
    Collects data and methods common to connections to traders or mock data
    """
    def connect(self) -> bool:
        pass
    
    def get_candles_for_symbol(self, symbol, timeframe, num_candlesticks) -> pd.DataFrame:
        pass
    
    def get_symbol_info() -> str:
        pass
    
    def place_order(self, symbol, signal, volume, price, deviation) -> bool:
        pass
    
    def get_account_info(self) -> dict:
        pass
    
    def close_position(self, position, bid, ask, deviation) -> bool:
        pass
    
    def get_positions(self) -> dict:
        pass
    
    def get_symbol_info_tick(self, symbol) -> dict:
        pass
    
    def get_ask_price(self, symbol) -> int:
        pass
    
    def get_bid_price(self, symbol) -> int:
        pass
    
    def do_nothing(self):
        print("No actionable trades!")
    
    def get_account_balance(self):
        pass
    
    def close_all_open_positions(self, bid, ask, deviation) -> bool:
        positions = self.get_positions()
        for position in positions:
            self.close_position(position, bid, ask, deviation)