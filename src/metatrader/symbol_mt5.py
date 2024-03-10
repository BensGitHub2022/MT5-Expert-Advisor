from datetime import datetime, timedelta, timezone
from enum import Enum

import MetaTrader5 as mt5
import numpy as np
import pandas as pd

from src.interfaces import ISymbol


class SymbolMT5(ISymbol):

    candles: np.array
    candles_df: pd.DataFrame

    symbol_name: str 
    mt5_timeframe: object
    timeframe: str
    start_pos: int
    
    # used only by ticks retrieval method, not the same as candlestick/system time inside EmaStrategy object
    current_time: timezone

    def __init__(self, symbol_name: str, timeframe: str) -> None:
        self.symbol_name = symbol_name
        self.timeframe = timeframe
        self.mt5_timeframe = self.get_mt5_timeframe(timeframe)
        self.start_pos = 0

    def get_candlesticks(self, num_candlesticks) -> pd.DataFrame:
        self.candles = mt5.copy_rates_from_pos(self.symbol_name, self.mt5_timeframe, self.start_pos, num_candlesticks)
        self.candles_df = pd.DataFrame(self.candles)
        return self.candles_df
    
    def get_candlestick_time(self) -> int:
        df = self.get_candlesticks(1)
        rounded_candlestick_time = int(round(df.iloc[-1]['time']))
        return rounded_candlestick_time
    
    def get_symbol_info(self) -> bool:
        symbol_info = mt5.symbol_info(self.symbol_name)
        if symbol_info is None:
            raise RuntimeError('No symbol info returned from MT5. Error is ' + str(mt5.last_error() or ''))
        return symbol_info._asdict()
    
    def get_symbol_pip_size(self) -> float:
        symbol_info = self.get_symbol_info()
        trade_tick_size = symbol_info['trade_tick_size']
        return trade_tick_size

    def get_symbol_contract_size(self) -> float:
        symbol_info = self.get_symbol_info()
        trade_contract_size = symbol_info['trade_contract_size']
        return trade_contract_size
    
    def get_symbol_info_tick(self) -> dict:
        symbol_info_tick = mt5.symbol_info_tick(self.symbol_name)
        if symbol_info_tick is None:
            error = mt5.last_error()
            raise RuntimeError('No symbol info tick returned from MT5. Error is ' + str(mt5.last_error() or ''))
        return symbol_info_tick._asdict()
    
    def get_symbol_info_bid(self) -> float:
        symbol_info_tick = self.get_symbol_info_tick()
        symbol_info_bid = symbol_info_tick['bid']
        return symbol_info_bid

    def get_symbol_info_ask(self) -> float:
        symbol_info_tick = self.get_symbol_info_tick()
        symbol_info_ask = symbol_info_tick['ask']
        return symbol_info_ask

    def get_ticks(self, num_ticks, current_time = 0) -> pd.DataFrame:
        self.current_time = current_time
        ticks = mt5.copy_ticks_from(self.symbol_name, self.current_time, num_ticks, mt5.COPY_TICKS_ALL)
        ticks_df = pd.DataFrame(ticks)
        return ticks_df
    
    def get_symbol_name(self) -> str:
        return self.symbol_name
    
    def get_symbol_timeframe(self) -> str:
        return self.timeframe

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
    one_minute = mt5.TIMEFRAME_M1
    two_minutes = mt5.TIMEFRAME_M2
    three_minutes = mt5.TIMEFRAME_M3
    four_minutes = mt5.TIMEFRAME_M4
    five_minutes = mt5.TIMEFRAME_M5
    six_minutes = mt5.TIMEFRAME_M6
    ten_minutes = mt5.TIMEFRAME_M10
    twelve_minutes = mt5.TIMEFRAME_M12
    fifteen_minutes = mt5.TIMEFRAME_M15
    twenty_minutes = mt5.TIMEFRAME_M20
    thirty_minutes = mt5.TIMEFRAME_M30
    one_month = mt5.TIMEFRAME_MN1
    one_hour = mt5.TIMEFRAME_H1
    two_hours = mt5.TIMEFRAME_H2
    three_hours = mt5.TIMEFRAME_H3
    four_hours = mt5.TIMEFRAME_H4
    six_hours = mt5.TIMEFRAME_H6
    eight_hours = mt5.TIMEFRAME_H8
    one_day = mt5.TIMEFRAME_D1