import numpy as np
import pandas as pd
from enum import Enum

from src.interfaces import ISymbol

from datetime import timezone


class SymbolSimulator(ISymbol):

    ### Unique to Mock class ###
    candles_df_master: pd.DataFrame
    ticks_df_master: pd.DataFrame
    counter: object
    mock_location: str
    ### #################### ###

    candles_df: pd.DataFrame

    symbol: str 
    mt5_timeframe: int # do we use this in mock ?
    timeframe: str # do we use this in mock ?
    start_pos: int # how do we use start pos in mock?

    current_time: timezone # do we use this in mock ?

    def __init__(self, symbol, timeframe, candles_mock_location="mock/candlesticks.csv", ticks_mock_location="mock/ticks.csv"):
        self.symbol = symbol
        self.timeframe = timeframe
        self.mt5_timeframe = self.get_mt5_timeframe(timeframe) # do we need this?
        self.start_pos = 0 # how do we use start pos in mock? # counter unique to mock 
        
        self.ticks_df_master = self.get_ticks_from_csv(ticks_mock_location)
        self.candles_df_master = self.get_candlesticks_from_csv(candles_mock_location)
        self.counter = Counter(self.candles_df_master)

    def set_symbol(self, symbol: str, timeframe: str) -> None:
        self.symbol = symbol
        self.timeframe = timeframe # do we use this in mock?
        
    def get_candlesticks(self, num_candlesticks) -> pd.DataFrame:
        interval = self.counter.__iter__()+num_candlesticks
        if (self.counter.check_index(interval)):
            self.candles_df = self.candles_df_master.iloc[self.counter.__iter__():interval]
            self.counter.__advance__(num_candlesticks)
        return self.candles_df
    
    def get_candlestick_time(self) -> int:
        df = self.get_candlesticks(1)
        self.counter.__previous__()
        rounded_candlestick_time = int(round(df.iloc[-1]['time']))
        self.current_time = rounded_candlestick_time
        return rounded_candlestick_time
    
    def get_symbol_info_tick(self) -> dict:
        rounded_candlestick_time = int(round(self.candles_df.iloc[-1]['time']))
        tick_df = pd.DataFrame()
        while (tick_df.empty):
            tick_df = self.ticks_df_master.loc[self.ticks_df_master['time']==rounded_candlestick_time]
            rounded_candlestick_time -= 1
        tick = tick_df.to_dict('list')
        return tick

    def get_symbol_info_bid(self) -> float:
        symbol_info_tick = self.get_symbol_info_tick()
        symbol_info_bid = symbol_info_tick['bid'][0]
        return symbol_info_bid

    def get_symbol_info_ask(self) -> float:
        symbol_info_tick = self.get_symbol_info_tick()
        symbol_info_ask = symbol_info_tick['ask'][0]
        return symbol_info_ask
    
    def get_tick_time(self) -> int:
        symbol_info_tick = self.get_symbol_info_tick()
        symbol_info_time = symbol_info_tick['time'][0]
        return symbol_info_time

    def get_ticks(self, num_ticks, current_time = 0) -> pd.DataFrame:
        pass

    def get_symbol_name(self) -> str:
        return self.symbol

    ### Implementation unique to mock method ###
    # Get candlesticks master file
    def get_candlesticks_from_csv(self, candles_mock_location) -> pd.DataFrame:
        """
        Retrieves mock data from csv file in mock directory.
        :param candles_mock_location: The path to the mock data which is stored in candlesticks (bar chart format) as a csv
        :return: The master dataframe with ALL mock data to be tested.
        """
        candles_df_master = pd.read_csv(candles_mock_location,index_col=0)
        return candles_df_master
    
    # Get ticks master file
    def get_ticks_from_csv(self, ticks_mock_location) -> pd.DataFrame:
        """
        
        """
        ticks_df_master = pd.read_csv(ticks_mock_location, index_col=0)
        return ticks_df_master
    
    # change which mock candlesticks file is used
    def set_candles_df_master(self, candles_mock_location) -> pd.DataFrame:
        df = self.get_candlesticks_from_csv(candles_mock_location)
        self.candles_df_master = df
        return self.candles_df_master

    # change which mock ticks file is used
    def set_ticks_df_master(self, ticks_mock_location) -> pd.DataFrame:
        df = self.get_ticks_from_csv(ticks_mock_location)
        self.ticks_df_master = df
        return self.ticks_df_master

    # unused
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
            
    # unused
    def set_candlesticks_start_pos(self, start_pos=0) -> None:
        self.start_pos = start_pos # how do we use start pos in mock?
        self.counter.__setindex__(start_pos) # counter unique to mock

    # set ticks date method is open for implementation in mock

# unused
class Timeframe(Enum):
    one_minute = 60
    two_minutes = 120
    three_minutes = 180
    four_minutes = 240
    five_minutes = 300
    six_minutes = 360
    ten_minutes = 600
    twelve_minutes = 720
    fifteen_minutes = 900
    twenty_minutes = 1200
    thirty_minutes = 1800
    one_month = 2628000
    one_hour = 3600
    two_hours = 7200
    three_hours = 10800
    four_hours = 14400
    six_hours = 21600
    eight_hours = 28800
    one_day = 86400

class Counter():
    current_index: int
    dataframe_size: int
    df: pd.DataFrame

    def __init__(self, df: pd.DataFrame, current_index = 0) -> None:
        self.df = df
        self.dataframe_size = len(df)
        self.current_index = current_index

    def __iter__(self) -> object:
        return self.current_index

    def __next__(self) -> int:
        temp_index = self.current_index
        if (temp_index+1 >= self.dataframe_size):
            raise IndexError(f"{temp_index} is out of bounds of the current mock data!")
        else:
            self.current_index += 1
        return self.current_index
    
    def __previous__(self) -> int:
        temp_index = self.current_index
        if (temp_index-1 < 0):
            raise IndexError(f"{temp_index} is out of bounds of the current mock data!")
        else:
            self.current_index -= 1
        return self.current_index
        
    def __hasnext__(self) -> bool:
        temp_index = self.current_index
        if (temp_index+1 >= self.dataframe_size):
            return False
        else:
            return True
        
    def __hasprevious__(self) -> bool:
        temp_index = self.current_index
        if (temp_index-1 < 0):
            return False
        else:
            return True

    def __advance__(self, interval) -> int:
        temp_index = self.current_index + interval
        if (temp_index < 0 | temp_index >= self.dataframe_size):
            raise IndexError(f"{temp_index} is out of bounds of the current mock data!")
        else:
            self.current_index = temp_index
        return self.current_index
    
    def __setindex__(self, new_index) -> int:
        if (new_index < 0 | new_index >= self.dataframe_size):
            raise IndexError(f"{new_index} is out of bounds of the current mock data!")
        else:
            self.current_index = new_index
        return self.current_index
    
    def check_index(self, temp_index) -> bool:
        if (temp_index < 0 | temp_index >= self.dataframe_size):
            raise IndexError(f"{temp_index} is out of bounds of the current mock data!")
        return True