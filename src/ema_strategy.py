import pandas as pd
import talib as ta
import time
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from src.interfaces import IStrategy

class EmaStrategy(IStrategy):

    symbol: str
    timeframe: str
    interval: int

    previous_df: pd.DataFrame
    df: pd.DataFrame
    new_candle_df: pd.DataFrame
    ema_short: int
    ema_long: int
    action_str: str
    action: int

    current_system_time: int
    current_candlestick_time: int

    def __init__(self, symbol: str, timeframe:str, ema_short:int, ema_long:int):
        self.symbol = symbol
        self.timeframe = timeframe
        self.ema_short = ema_short
        self.ema_long = ema_long
        self.interval = self.ema_long+1
        self.action = 0 

    def process_seed(self, df: object) -> bool:
        self.df = df
        self.calc_ema_short(self.df)
        self.calc_ema_long(self.df)
        return True

    def process_next(self, new_candle_df: object) -> bool:
        self.new_candle_df = new_candle_df
        self.previous_df = self.df
        self.df.drop(index=[0], axis=0, inplace=True)
        self.df = pd.concat([self.df, new_candle_df],ignore_index=True)
        self.calc_ema_short(self.df)
        self.calc_ema_long(self.df)
        return True

    def check_next(self, current_candlestick_time)->bool:
        if (current_candlestick_time != self.current_candlestick_time):
            self.current_candlestick_time = current_candlestick_time
            print("New candle!")
            return True
        else:
            print("Zzz")
            time.sleep(1)
            return False

    def calc_ema_short(self, data:object) -> object:
        self.df = data
        self.df['EMA_short'] =  ta.EMA(self.df['close'], timeperiod=self.ema_short)

    def calc_ema_long(self, data:object) -> object:
        self.df = data
        self.df['EMA_long'] = ta.EMA(self.df['close'], timeperiod=self.ema_long)

    def check_signal(self) -> bool:
        ema_short = self.df['EMA_short']
        ema_long = self.df['EMA_long']

        self.action_str = "No signal"

        #buy if short ema crosses above long ema
        if (ema_short.iloc[-2] < ema_long.iloc[-2]) and (ema_short.iloc[-1] > ema_long.iloc[-1]):
            self.action_str = "BUY"
            self.action = 1
            print(self.action_str)
            print(self.get_current_candlestick_time()-60)
            return True

        #sell if short ema crosses below long ema
        if (ema_short.iloc[-2] > ema_long.iloc[-2]) and (ema_short.iloc[-1] < ema_long.iloc[-1]):
            self.action_str = "SELL"
            self.action = -1
            print(self.action_str)
            print(self.get_current_candlestick_time()-60)
            return True
        
        self.action = 0
        print(self.action_str)
        return False

    def get_ema_short(self) -> int:
        return self.ema_short

    def get_ema_long(self) -> int:
        return self.ema_long
    
    def get_symbol(self) -> str:
        return self.symbol
    
    def get_timeframe(self) -> str:
        return self.timeframe
    
    def get_interval(self) -> int:
        return self.interval
    
    def get_data_frame(self) -> pd.DataFrame:
        return self.df
    
    def get_action(self) -> int:
        return self.action
    
    def set_current_system_time(self) -> None:
        self.current_system_time = self.get_system_time()

    def get_system_time(self) -> int:
        offset = timedelta(hours=2.0)
        tz_UTC_offset = timezone(offset,'GMT')
        dt = datetime.now(tz_UTC_offset)
        epoch_time = datetime(1970,1,1,tzinfo=tz_UTC_offset)
        delta = dt-epoch_time
        rounded_delta = int(round(delta.total_seconds()))
        return rounded_delta

    def set_current_candlestick_time(self, candlestick_time: int) -> None:
        self.current_candlestick_time = candlestick_time

    def get_current_candlestick_time(self) -> int:
        return self.current_candlestick_time