from datetime import timezone
from enum import Enum

import numpy as np
import pandas as pd

from src.interfaces import ISymbol


class SymbolSimulator(ISymbol):

    ### Unique to Mock class ###
    candles_df_master: pd.DataFrame
    ticks_df_master: pd.DataFrame
    counter: object
    mock_location: str
    ### #################### ###

    candles_df: pd.DataFrame

    symbol: str 
    timeframe: str 
    start_pos: int

    current_time: int # NOTE: the only use for this is to obtain ticks based on current candlestick time but get_ticks method hasn't been defined yet. 

    def __init__(self, symbol, timeframe, candles_mock_location="mock/candlesticks.csv", ticks_mock_location="mock/ticks.csv"):
        self.symbol = symbol # NOTE: Devise a way to set the symbol to match the mock location of a file
        self.timeframe = timeframe
        
        self.ticks_df_master = self.get_ticks_from_csv(ticks_mock_location)
        self.candles_df_master = self.get_candlesticks_from_csv(candles_mock_location)
        self.counter = Counter(self.candles_df_master)
    
    def get_candlesticks(self, num_candlesticks) -> pd.DataFrame:
        if (self.counter.__hasnext__()):
            interval = self.counter.__iter__()+num_candlesticks
        else:
            return pd.DataFrame()
        self.candles_df = self.candles_df_master.iloc[self.counter.__iter__():interval]
        self.counter.__advance__(num_candlesticks)
        return self.candles_df
    
    def get_candlestick_time(self) -> int:
        df = self.get_candlesticks(1)
        if (df.empty):
            return -1
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
    
    def get_symbol_timeframe(self) -> str:
        return self.timeframe

    # NOTE: ### Implementation unique to mock method ###
    # Get candlesticks master file
    def get_candlesticks_from_csv(self, candles_mock_location) -> pd.DataFrame:
        """
        Retrieves mock data from csv file in mock directory.
        :param candles_mock_location: The path to the mock data which is stored in candlesticks (bar chart format) as a csv
        :return: The candlesticks master dataframe with ALL mock data to be tested.
        """
        candles_df_master = pd.read_csv(candles_mock_location,index_col=0,sep=",", low_memory=False)
        return candles_df_master
    
    # Get ticks master file
    def get_ticks_from_csv(self, ticks_mock_location) -> pd.DataFrame:
        """
        Retrieves mock data from csv file in mock directory.
        :param ticks_mock_location: The path to the mock data which is stored in ticks (price movement) as a csv
        :return: The ticks master dataframe with ALL mock data to be tested.
        """
        ticks_df_master = pd.read_csv(ticks_mock_location, index_col=0,sep=",", low_memory=False)
        return ticks_df_master

# Advances through candlesticks stored in data frame from csv file
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
        else:
            return True