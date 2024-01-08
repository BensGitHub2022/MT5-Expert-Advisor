from src.Connections.ConnectionInterface import ConnectionInterface
from src.Connections.Mock.MockConnection import MockConnection
from src.Connections.MT5.MetaTraderConnection import MetaTraderConnection
from src.trade_bot import TradeBot
from src.TradingStrategies.ema_strategy import EmaStrategy
from src.symbols_factory import SymbolsFactory
from src.trade_execution_adapter import TradeExecutorAdapter

import pandas as pd

EMA_SHORT = 5
EMA_LONG = 8

INTERVAL = EMA_LONG + 1
NEXT = 1

USE_REAL_DATA = True

def main():
    print("Hello Trade Bot!")
    
    connection: ConnectionInterface
    
    if USE_REAL_DATA:
        connection = MetaTraderConnection()
    else:
        connection = MockConnection()


    # Composition root
    pd.set_option('display.max_columns', None)

    strategy = EmaStrategy(symbol, timeframe, EMA_SHORT,EMA_LONG)
    # action_writer = strategy.get_action_writer()
    
    symbol_factory = SymbolsFactory(production=False)
    symbol = symbol_factory.create_symbol(symbol,timeframe, candles_mock_location=CANDLES_MOCK_LOCATION, ticks_mock_location=TICKS_MOCK_LOCATION) # Mock
    # symbol = symbol_factory.create_symbol(symbol,timeframe) # Production
    print("Using the " + strategy.get_strategy_name() + ", trading on " + symbol.get_symbol_name())
    # print(symbol.get_symbol_info()) # Need to implement in mock!

    #trade_executor = TradeExecutorAdapter()
    
    #positions = trade_executor.get_positions()
    #print(positions)
    
    strategy.set_current_candlestick_time(symbol.get_candlestick_time())
    strategy.process_seed(symbol.get_candlesticks(INTERVAL))
    
    print(symbol.get_symbol_info_bid())

    # strategy.record_action()
    # action_writer.print_action()
    
    while (True):
        if(strategy.check_next(symbol.get_candlestick_time())):
            strategy.process_next(symbol.get_candlesticks(NEXT))
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