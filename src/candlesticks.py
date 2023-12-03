import numpy as np
import pandas as pd
from enum import Enum
import MetaTrader5 as mt5

class Candlesticks():

    candles: np.array
    candles_df: pd.DataFrame

    symbol: str 
    mt5_timeframe: int
    timeframe: str
    start_pos: int
    num_candlesticks: int

    def __init__(self, symbol: str, timeframe: str, num_candlesticks: int) -> None:
        self.symbol = symbol
        self.timeframe = timeframe
        self.mt5_timeframe = self.get_mt5_timeframe(timeframe)
        self.start_pos = 1
        self.num_candlesticks = num_candlesticks
        self.candles = mt5.copy_rates_from_pos(self.symbol, self.mt5_timeframe, self.start_pos, self.num_candlesticks)
        self.candles_df = pd.DataFrame(self.candles)

    def get_candles_dataframe(self) -> pd.DataFrame:
            return self.candles_df

    def get_mt5_timeframe(self, timeframe: str):
        """
        Gets a MetaTrader 5-readable timeframe.
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