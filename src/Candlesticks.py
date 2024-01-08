import pandas as pd

class Candlesticks:
    
    dataframe: pd.DataFrame
    
    def __init__ (symbol_dataframe: pd.DataFrame):
        dataframe = symbol_dataframe
    
    def get_candlestick_time(self) -> int:
        df = self.get_candlesticks(1)
        self.counter.__previous__()
        rounded_candlestick_time = int(round(df.iloc[-1]['time']))
        self.current_time = rounded_candlestick_time
        return rounded_candlestick_time