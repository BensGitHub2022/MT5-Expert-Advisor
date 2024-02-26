# import pandas as pd # Not used in main unless for debugging
import warnings # Bad
from pandas.errors import SettingWithCopyWarning # Bad

import sys

from src.factories.account_factory import AccountFactory
from src.action_writer import ActionWriter
from src.factories.context_factory import ContextFactory
from src.ema_strategy import EmaStrategy
from src.json_reader import JsonReader
from src.factories.symbol_factory import SymbolFactory
from src.trade_bot import TradeBot
from src.factories.trade_executor_factory import TradeExecutionFactory

# Path to MetaTrader5 login details.
ACCOUNT_SETTINGS_PATH = "config/settings.json"
CREDENTIALS_FILE_PATH = "config/credentials.json"

EMA_SHORT = 500
EMA_LONG = 1000

PRODUCTION = False # added for convenience, all factories eventually created in main and passed to trade_bot

def main():
    # NOTE: Args Key:
    # 1 - symbol name OR settings
    # 2 - Production flag, 1 == True, 0 == False
    # 3 - EMA short
    # 4 - EMA long
    # Example: BTCUSD 1 500 1000
    try:
        filepath: str = "config/" + sys.argv[1] + ".json"
        production: int = int(sys.argv[2])
        ema_short: int = int(sys.argv[3])
        ema_long: int = int(sys.argv[4])
    except:
        filepath: str = ACCOUNT_SETTINGS_PATH
        production: bool = PRODUCTION
        ema_short = EMA_SHORT
        ema_long = EMA_LONG
    
    # Composition root
    print("Hello Trade Bot!")
    
    # NOTE: Need to decide if these present true issues.
    warnings.simplefilter(action='ignore', category=FutureWarning) # Bad <- this one relates to passing NaN to pd.concat, will be depricated in future
    warnings.simplefilter(action='ignore', category=SettingWithCopyWarning) # Bad <- this one relates to copy of a slice of a dataframe
    # OR
    # pd.set_option('mode.chained_assignment', None)
    # OR
    # with pd.option_context('mode.chained_assignment', None):
    # ^ needs to implemented in method of calling function

    json_settings = JsonReader(file_path=filepath)
    credentials = JsonReader(file_path=CREDENTIALS_FILE_PATH)
    
    symbol = json_settings.get_symbol()
    timeframe = json_settings.get_timeframe()
    if (production == False):
        candlesticks_filepath = json_settings.get_symbol_candlesticks_filepath()
        ticks_filepath = json_settings.get_symbol_ticks_filepath()
    else:
        candlesticks_filepath = ""
        ticks_filepath = ""

    action_writer = ActionWriter()

    context_factory = ContextFactory(production=production)
    context = context_factory.create_context(credentials.get_json_data())
    
    symbol_factory = SymbolFactory(production=production)
    symbol = symbol_factory.create_symbol(symbol, timeframe, candles_mock_location=candlesticks_filepath, ticks_mock_location=ticks_filepath)

    account_factory = AccountFactory(production=production)
    account = account_factory.create_account(symbol, balance = 100000, profit = 0, action_writer=action_writer)

    trade_execution_factory = TradeExecutionFactory(production=production)
    trade_executor = trade_execution_factory.create_trade_executor(account)
    
    strategy = EmaStrategy(symbol,ema_short,ema_long, action_writer, console_output=production)

    trade_bot = TradeBot(context, action_writer, strategy, symbol, account, trade_executor)
    trade_bot.start()
    kill_bot = input()
    if (kill_bot == 'X'):
        trade_bot.stop()

if __name__ == '__main__':
    main()