import pandas as pd
import talib as ta
import time
import winsound
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from src.interfaces import IStrategy
# from src.action_writer import ActionWriter

SMOOTHENING = 2

class EmaStrategy(IStrategy):

    ### COMMENT KEY ###
    # [1] This gets instantiated, is helpful for debugging, but not heavily used
    # [2] Was helpful for understanding a concept but is not relied upon

    symbol: str # passed to the class at initialization
    timeframe: str # passed to the class at initialization

    previous_df: pd.DataFrame # the previous rolling candlestick window used to calc EMAs (Note: this is used for debugging but not heavily relied upon [1])
    df: pd.DataFrame # the current rolling candlestick window used to calc EMAs
    new_candle_df: pd.DataFrame # the next candlestick added to the rolling window to calc new EMAs 
    
    ema_short: int # passed to the class at initialization
    ema_long: int # passed to the class at initialization
    ema_short_weighting: float # smoothening factor which is calculated off the smoothening constant and EMA window
    ema_long_weighting: float # smoothening factor which is calculated off the smoothening constant and EMA window
    
    action_df: pd.DataFrame # a separate datastructure used to store the EMAs and the result of the signals
    action_str: str # action based on signal analysis as a string {'buy', 'sell', 'no signal'}
    action: int # action based on signal analysis as an integer {1, -1, 0}
    signal: dict # signal from signal analysis as a dict {'action': 1/-1/0, 'action_str'; "buy"/"sell"/"no signal"}

    # action_writer: object # records all activity processed by the strategy, see action writer class

    initialized: bool
    frequency: int
    duration: int

    # This is not used or relied upon but can be called to ensure that the candlesticks & ticks are relatively close to the system time. 
    # Ensure that the data we are fetching does not have too much delay from local time
    current_system_time: int # The local time not, i.e. machine time (See comments above ^ [2]). 
    
    # This is relied upon and essential to the strategy
    current_candlestick_time: int # Current candlestick time pulled from the most recent candlestick

    def __init__(self, symbol: str, timeframe:str, ema_short:int, ema_long:int) -> None:
        """
        Constructor for EmaStrategy
        :param symbol: the symbol which is the focus of the ema strategy, passed as a string
        :param timeframe: the period used by the strategy (i.e., minute, five-minute, etc), passed as a string
        :param ema_short: the window of the short-term EMA, passed as an integer
        :param ema_short: the window of the long-term EMA, passed as an integer
        :return: None
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.ema_short = ema_short
        self.ema_long = ema_long
        self.ema_short_weighting = SMOOTHENING/(ema_short+1)
        self.ema_long_weighting = SMOOTHENING/(ema_long+1)
        
        self.action_df = pd.DataFrame(columns = ['EMA_short', 'EMA_long','action','action_str'])
        self.action = 0
        self.action_str = ''
        self.signal = {'action': self.action, 'action_str': self.action_str}

        # self.action_writer = ActionWriter()
        self.initialized = False
        self.frequency = 500
        self.duration = 2000
        
    def process_seed(self, df: object) -> bool:
        """
        This method processes the initial seed data for the strategy. It applies two helper methods to establish the signals_df which the strategy relies upon to make decisions.
        :param df: A dataframe of candlesticks passed to the method from a candlesticks object
        :return: True if the method succeeds in processing a seed
        """
        self.df = df
        self.process_seed_emas(self.df)
        return True

    def process_next(self, new_candle_df: object) -> bool:
        """
        This method processes the next candlestick and applies a helper function to caclulate a new signal within the signals_df which the strategy relies upon to make decisions.
        :param new_candle_df: A candlestick dataframe passed to the method from a candlestick object
        :return: True if the method succeeds in processing the next candlestick
        """
        self.new_candle_df = new_candle_df
        self.previous_df = self.df
        self.df.drop(index=[0], axis=0, inplace=True)
        self.df = pd.concat([self.df, new_candle_df],ignore_index=True)
        self.process_new_emas(new_candle_df)
        return True

    def check_next(self, current_candlestick_time: int)->bool:
        """
        This method checks to see if there is a new candlestick available to make decisions on. It compares the epoch time in the current candlestick retreived from the metatrader API to the candlestick time stored within the EmaStrategy class.
        :param current_candlestick_time: The candlestick time passed to the method as an int from a candlestick object.
        :return: True if the passed candlestick time is different than the stored current time. False if the times are the same.
        """
        if (current_candlestick_time != self.current_candlestick_time):
            self.current_candlestick_time = current_candlestick_time
            print("New candle!")
            return True
        else:
            print("... sleeping")
            time.sleep(1)
            return False

    def process_seed_emas(self, data: pd.DataFrame) -> bool:
        self.action_df['EMA_short'] = ta.EMA(data['close'], timeperiod=self.ema_short)
        self.action_df['EMA_long'] = ta.EMA(data['close'], timeperiod=self.ema_long)
        return True

    def process_new_emas(self, data: pd.DataFrame) -> bool:
        self.action_df.drop(index=[0], axis=0, inplace=True)
        current_close = data['close'].iloc[-1]
        previous_ema_short = self.action_df['EMA_short'].iloc[-1]
        previous_ema_long = self.action_df['EMA_long'].iloc[-1]
        new_ema_short = previous_ema_short + self.ema_short_weighting*(current_close-previous_ema_short)
        new_ema_long = previous_ema_long + self.ema_long_weighting*(current_close-previous_ema_long)
        d = {'EMA_short': [new_ema_short], 'EMA_long': [new_ema_long]}
        new_df = pd.DataFrame(data = d)
        self.action_df = pd.concat([self.action_df,new_df], ignore_index=True)
        return True

    def check_signal(self) -> dict:        
        ema_short = self.action_df['EMA_short']
        ema_long = self.action_df['EMA_long']

        self.action_str = "No signal"
        self.action = 0

        #buy if short ema crosses above long ema
        if (ema_short.iloc[-2] < ema_long.iloc[-2]) and (ema_short.iloc[-1] > ema_long.iloc[-1]):
            self.action_str = "buy"
            self.action = 1
            self.signal = {'action': self.action, 'action_str': self.action_str}
            winsound.Beep(self.frequency, self.duration)

        #sell if short ema crosses below long ema
        if (ema_short.iloc[-2] > ema_long.iloc[-2]) and (ema_short.iloc[-1] < ema_long.iloc[-1]):
            self.action_str = "sell"
            self.action = -1
            self.signal = {'action': self.action, 'action_str': self.action_str}
            winsound.Beep(self.frequency, self.duration)
        
        self.action_df.loc[self.ema_long,'action'] = self.action
        self.action_df.loc[self.ema_long,'action_str'] = self.action_str
        self.signal = {'action': self.action, 'action_str': self.action_str}

        return self.signal
    
    # def record_action(self) -> bool:
    #     if(not self.initialized):
    #         self.action_writer.record_action(self.df, self.action_df)
    #         self.initialized = True
    #     else:
    #         self.action_writer.record_action(self.df.tail(1), self.action_df.tail(1))

    #     self.action_writer.write_action()

        return True

    def get_ema_short(self) -> int:
        return self.ema_short

    def get_ema_long(self) -> int:
        return self.ema_long
    
    def get_symbol(self) -> str:
        return self.symbol
    
    def get_timeframe(self) -> str:
        return self.timeframe
    
    def get_dataframe(self) -> pd.DataFrame:
        return self.df
    
    def get_action(self) -> int:
        return self.action
    
    def get_action_str(self) -> str:
        return self.action_str
    
    def get_action_df(self) -> pd.DataFrame:
        return self.action_df
    
    # def get_action_writer(self) -> object:
    #     return self.action_writer

    def get_signal(self) -> dict:
        return self.signal

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

    def get_strategy_name(self) -> str:
        return "EMA Strategy"

# Maybe ???
### This is a consideration that has not been implemented! ###
"""
class Signals():

    signals_df: pd.DataFrame # a separate datastructure used to store the EMAs 
    action_str: str
    action: int
    signal: dict

    def __init__(self) -> None:
        pass
"""