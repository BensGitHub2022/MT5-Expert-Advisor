from src.Connections.ConnectionInterface import ConnectionInterface
from src.Connections.Mock.MockConnection import MockConnection
from src.Connections.MT5.MetaTraderConnection import MetaTraderConnection
from src.trade_bot import TradeBot
from src.TradingStrategies.ema_strategy import EmaStrategy
from src.CommonEnums.Timeframe import Timeframe

import pandas as pd

EMA_SHORT = 5
EMA_LONG = 8

INTERVAL = EMA_LONG + 1
NEXT = 1

USE_REAL_DATA = False
SYMBOL = "BCHUSD"
TIMEOUT = 60000
TIMEFRAME = Timeframe.one_minute
NUM_CANDLESTICKS = 20

def main():
    print("Hello Trade Bot!")
    
    connection: ConnectionInterface
    
    if USE_REAL_DATA:
        connection = MetaTraderConnection()
    else:
        connection = MockConnection()

    # Composition root
    pd.set_option('display.max_columns', None)

    strategy = EmaStrategy(SYMBOL, TIMEFRAME, EMA_SHORT, EMA_LONG)

    print("Using the " + strategy.get_strategy_name() + ", trading on " + SYMBOL)
    
    first_candlestick_set = connection.get_candles_for_symbol(SYMBOL, TIMEFRAME, NUM_CANDLESTICKS)
    time = int(round(first_candlestick_set.iloc[-1]['time']))

    strategy.set_current_candlestick_time(time)
    strategy.process_seed(first_candlestick_set)

    while (True):
        candlestick_set = connection.get_candles_for_symbol(SYMBOL, TIMEFRAME, NUM_CANDLESTICKS)
        if(int(round(first_candlestick_set.iloc[-1]['time']))):
            strategy.process_next(candlestick_set)
            signal = strategy.check_signal()
            """
            match signal.get('action'):
                case 1:
                    if(trade_executor.get_positions()):
                        trade_executor.close_all_positions(symbol.get_symbol_info_bid(), symbol.get_symbol_info_ask(),20)
                    trade_executor.place_order(symbol.get_symbol_name(),signal,symbol.get_symbol_info_ask(),20) 
                case -1:
                    if(trade_executor.get_positions()):
                        trade_executor.close_all_positions(symbol.get_symbol_info_bid(), symbol.get_symbol_info_ask(),20)
                    trade_executor.place_order(symbol.get_symbol_name(),signal,symbol.get_symbol_info_bid(),20) 
                case 0:
                    trade_executor.do_nothing()
            """     
            # strategy.record_action()
            # action_writer.print_action()
    

    """
    strategy = EmaStrategy()

    bot = TradeBot(strategy, meta_trader)
    bot.start()
    print("Bot started")

    print("Press X to stop")
    inp = input()
    # if (inp == 'X')

    bot.stop()
    print("Bot stopped")
    """
if __name__ == '__main__':
    main()