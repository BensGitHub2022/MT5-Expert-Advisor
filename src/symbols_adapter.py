import numpy as np
import pandas as pd
from enum import Enum
import MetaTrader5 as mt5

from datetime import datetime
from datetime import timedelta
from datetime import timezone

class SymbolsAdapter():

    candles: np.array
    candles_df: pd.DataFrame

    symbol: str 
    mt5_timeframe: int
    timeframe: str
    start_pos: int
    current_time: timezone

    # unused
    num_candlesticks: int
    num_ticks: int

    def __init__(self, symbol: str, timeframe: str) -> None:
        self.symbol = symbol
        self.timeframe = timeframe
        self.mt5_timeframe = self.get_mt5_timeframe(timeframe)
        self.start_pos = 0

    def set_symbol(self, symbol: str, timeframe: str) -> None:
        self.symbol = symbol
        self.timeframe = timeframe

    def set_candlesticks_start_pos(self, start_pos=0) -> None:
        self.start_pos = start_pos

    def set_ticks_date(self,current_time=0) -> None:
        if (current_time != 0):
            # tz_UTC = pytz.timezone('GMT')
            offset = timedelta(hours=2.0)
            tz_UTC_offset = timezone(offset,'GMT')
            self.current_time = datetime.now(tz_UTC_offset)
        else:
            self.current_time = 0

    def get_candlesticks(self, num_candlesticks) -> pd.DataFrame:
        self.candles = mt5.copy_rates_from_pos(self.symbol, self.mt5_timeframe, self.start_pos, num_candlesticks)
        self.candles_df = pd.DataFrame(self.candles)
        return self.candles_df
    
    def get_candlestick_time(self) -> int:
        df = self.get_candlesticks(1)
        rounded_candlestick_time = int(round(df.iloc[-1]['time']))
        return rounded_candlestick_time
    
    def get_symbol_info(self) -> bool:
        symbol_info = mt5.symbol_info(self.symbol)._asdict()
        return symbol_info

    def get_ticks(self, num_ticks, current_time = 0) -> bool:
        self.current_time = current_time
        ticks = mt5.copy_ticks_from(self.symbol, self.current_time, num_ticks, mt5.COPY_TICKS_ALL)
        ticks_df = pd.DataFrame(ticks)
        return ticks_df

    def get_mt5_timeframe(self, timeframe: str):
        """
        Gets a MetaTrader 5 readable timeframe.
        :param timeframe: The to-be located timeframe as a string.
        :return: A MetaTrader 5 timeframe.
        """
        try:
            return Timeframe[timeframe].value
        except KeyError as e:
            print(f"{timeframe} is not a legal timeframe. {e}")
            raise e

class Timeframe(Enum):
    one_minute  = mt5.TIMEFRAME_M1
    two_minutes  = mt5.TIMEFRAME_M2
    three_minutes  = mt5.TIMEFRAME_M3
    four_minutes  = mt5.TIMEFRAME_M4
    five_minutes  = mt5.TIMEFRAME_M5
    six_minutes  = mt5.TIMEFRAME_M6
    ten_minutes = mt5.TIMEFRAME_M10
    twelve_minutes = mt5.TIMEFRAME_M12
    fifteen_minutes = mt5.TIMEFRAME_M15
    twenty_minutes = mt5.TIMEFRAME_M20
    thirty_minutes = mt5.TIMEFRAME_M30
    one_month = mt5.TIMEFRAME_MN1
    one_hour  = mt5.TIMEFRAME_H1
    two_hours  = mt5.TIMEFRAME_H2
    three_hours  = mt5.TIMEFRAME_H3
    four_hours  = mt5.TIMEFRAME_H4
    six_hours  = mt5.TIMEFRAME_H6
    eight_hours  = mt5.TIMEFRAME_H8
    one_day  = mt5.TIMEFRAME_D1