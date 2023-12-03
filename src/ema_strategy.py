import pandas as pd
import talib as ta
from datetime import datetime
import pytz

from src.interfaces import IStrategy

class EmaStrategy(IStrategy):

    symbol: str
    timeframe: str
    interval: int

    df: pd.DataFrame
    ema_short: int
    ema_long: int
    action: int

    current_time: int

    def __init__(self, symbol: str, timeframe:str, ema_short:int, ema_long:int):
        self.symbol = symbol
        self.timeframe = timeframe
        self.ema_short = ema_short
        self.ema_long = ema_long
        self.interval = self.ema_long+1
        self.action = 0
        

    def process_seed(self, data: object) -> bool:
        self.df = data
        self.calc_ema_short(self.df)
        self.calc_ema_long(self.df)
        self.calc_ema_cross(self.df)
        return True

    def process_next(self, data: object) -> bool:
        new_candle = data
        self.df.drop(index=[0], axis=0, inplace=True)
        self.df = pd.concat([self.df, new_candle])
        self.calc_ema_short(self.df)
        self.calc_ema_long(self.df)
        self.calc_ema_cross(self.df)
        return True

    def check_if_next(self, exists)->bool:
        if (exists):
            return True
        else:
            return False

    def find_signals(self, data: object) -> int:
        pass

    def calc_ema_short(self, data:object) -> object:
        self.df = data
        self.df['EMA_short'] =  ta.EMA(self.df['close'], timeperiod=self.ema_short)

    def calc_ema_long(self, data:object) -> object:
        self.df = data
        self.df['EMA_long'] = ta.EMA(self.df['close'], timeperiod=self.ema_long)

    def calc_ema_cross(self, data:object) -> int:
        self.df = data
        ema_short = self.df['EMA_short']
        ema_long = self.df['EMA_long']

        #buy if short ema crosses above long ema
        if (ema_short.iloc[-2] < ema_long.iloc[-2]) and (ema_short.iloc[-1] > ema_long.iloc[-1]):
            self.action = 1

        #sell if short ema crosses below long ema
        if (ema_short.iloc[-2] > ema_long.iloc[-2]) and (ema_short.iloc[-1] < ema_long.iloc[-1]):
            self.action = -1
        return self.action

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
    
    def get_current_time(self) -> int:
        tz_London = pytz.timezone('Europe/London')
        dt = datetime.now(tz_London)
        epoch_time = datetime(1970,1,1,tzinfo=tz_London)
        delta = dt-epoch_time
        return delta.total_seconds()