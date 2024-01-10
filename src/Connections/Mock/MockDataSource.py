import os
import pandas as pd

from src.Connections.Mock.DataCounter import DataCounter

class MockDataSource():

    ticks_directory = "./MockTicks"
    
    candles_df_master: pd.DataFrame
    ticks_df_master: pd.DataFrame
    counter: DataCounter
    symbol: str

    def __init__(self, symbol, timeframe):
        self.symbol = symbol
        self.timeframe = timeframe
        self.candles_df_master = self.get_all_candlesticks_from_csv()
        self.counter = DataCounter(self.candles_df_master)

    def get_next_candle_set(self, num_candlesticks) -> pd.DataFrame:
        interval = self.counter.__iter__() + num_candlesticks
        if self.counter.check_index(interval):
            candles_df = self.candles_df_master.iloc[self.counter.__iter__():interval]
            self.counter.__advance__(num_candlesticks)
            return candles_df

    def get_next_tick_set(self, num_ticks, current_time = 0) -> pd.DataFrame:
        pass

    ### Implementation unique to mock method ###
    # Get candlesticks master file
    def get_all_candlesticks_from_csv(self) -> pd.DataFrame:
        """
        Retrieves mock data from csv file in mock directory.
        :return: The master dataframe with ALL mock data to be tested.
        """
        candles_mock_location = os.getcwd() + "\\src\\Connections\\Mock\\MockCandles\\" + self.symbol + ".csv"
        candles_df_master = pd.read_csv(candles_mock_location, index_col = 0)
        return candles_df_master
    
    # Get ticks master file
    def get_all_ticks_from_csv(self, ticks_mock_location) -> pd.DataFrame:
        """
        Retrieves mock data from csv file in mock directory.
        :return: The master dataframe with ALL mock data to be tested.
        """
        ticks_mock_location = self.candles_directory + self.symbol + ".csv"
        ticks_df_master = pd.read_csv(ticks_mock_location, index_col=0)
        return ticks_df_master