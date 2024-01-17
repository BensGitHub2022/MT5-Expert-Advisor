from src.json_reader import JsonReader
from src.trade_bot import TradeBot
from src.ema_strategy import EmaStrategy
from src.symbols_factory import SymbolsFactory
from src.context_factory import ContextFactory
from src.account_factory import AccountFactory
from src.trade_execution_factory import TradeExecutionFactory

import pandas as pd

# Path to MetaTrader5 login details.
ACCOUNT_SETTINGS_PATH = "pkg/settings.json"
CREDENTIALS_FILE_PATH = "pkg/credentials.json"

CANDLES_MOCK_LOCATION = "mock/candlesticks_current.csv"
TICKS_MOCK_LOCATION = "mock/ticks_current.csv"

EMA_SHORT = 5
EMA_LONG = 8

INTERVAL = EMA_LONG+1
NEXT = 1

def main():
    print("Hello Trade Bot!")

    # Composition root
    pd.set_option('display.max_columns', None)

    json_settings = JsonReader(ACCOUNT_SETTINGS_PATH)
    symbol = json_settings.get_symbol()
    timeframe = json_settings.get_timeframe()

    credentials = JsonReader(CREDENTIALS_FILE_PATH)

    meta_trader_factory = ContextFactory(production=True)
    meta_trader = meta_trader_factory.create_context(json_settings.get_json_data(),credentials.get_json_data())
    meta_trader.connect()

    strategy = EmaStrategy(symbol,timeframe,EMA_SHORT,EMA_LONG)
    action_writer = strategy.get_action_writer()
    
    symbol_factory = SymbolsFactory(production=True)
    symbol = symbol_factory.create_symbol(symbol,timeframe, candles_mock_location=CANDLES_MOCK_LOCATION, ticks_mock_location=TICKS_MOCK_LOCATION) # Mock
    # symbol = symbol_factory.create_symbol(symbol,timeframe) # Production
    print("Using the " + strategy.get_strategy_name() + ", trading on " + symbol.get_symbol_name())
    # print(symbol.get_symbol_info()) # Need to implement in mock!

    account_factory = AccountFactory(production=True)
    account = account_factory.create_account()

    trade_execution_factory = TradeExecutionFactory(production=True)
    trade_executor = trade_execution_factory.create_trade_executor(account)
    
    positions = account.get_positions()
    print(positions)
    
    strategy.set_current_candlestick_time(symbol.get_candlestick_time())
    strategy.process_seed(symbol.get_candlesticks(INTERVAL))
    
    print(symbol.get_symbol_info_bid())

    strategy.record_action()
    action_writer.print_action()
    
    while (True):
        if(strategy.check_next(symbol.get_candlestick_time())):
            strategy.process_next(symbol.get_candlesticks(NEXT))
            signal = strategy.check_signal()
            
            if signal.get('action') == 1:
                if(account.get_positions()):
                    trade_executor.close_all_positions(symbol.get_symbol_info_bid(), symbol.get_symbol_info_ask(),20)
                trade_executor.place_order(symbol.get_symbol_name(),signal,symbol.get_symbol_info_ask(),20) 
            elif signal.get('action') == -1:
                if(account.get_positions()):
                    trade_executor.close_all_positions(symbol.get_symbol_info_bid(), symbol.get_symbol_info_ask(),20)
                trade_executor.place_order(symbol.get_symbol_name(),signal,symbol.get_symbol_info_bid(),20) 
            else:
                trade_executor.do_nothing()
             
            strategy.record_action()
            action_writer.print_action()
    

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