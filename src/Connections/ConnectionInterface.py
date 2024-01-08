import pandas as pd

class ConnectionInterface():
    """
    Collects data and methods common to connections to traders or mock data
    """
    def connect(self) -> bool:
        pass
    
    def get_candles_for_symbol(self, symbol, timeframe, num_candlesticks) -> pd.DataFrame:
        pass
        
    def get_ticks_for_symbol(self, symbol, num_ticks) -> pd.DataFrame:
        pass
    
    def get_symbol_info() -> str:
        pass
    
    def send_order():
        pass
    
    def cancel_order():
        pass
    
    def get_account_balance() -> int:
        pass