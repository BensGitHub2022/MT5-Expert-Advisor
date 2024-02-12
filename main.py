import pandas as pd

from src.account_factory import AccountFactory
from src.action_writer import ActionWriter
from src.context_factory import ContextFactory
from src.ema_strategy import EmaStrategy
from src.json_reader import JsonReader
from src.symbol_factory import SymbolFactory
from src.trade_bot import TradeBot
from src.trade_executor_factory import TradeExecutionFactory

# Path to MetaTrader5 login details.
ACCOUNT_SETTINGS_PATH = "pkg/settings.json"
CREDENTIALS_FILE_PATH = "pkg/credentials.json"

CANDLES_MOCK_LOCATION = "mock/candlesticks_current.csv"
TICKS_MOCK_LOCATION = "mock/ticks_current.csv"

EMA_SHORT = 5
EMA_LONG = 8

PRODUCTION = True # added for convenience, all factories eventually created in main and passed to trade_bot

def main():
    print("Hello Trade Bot!")

    # Composition root
    pd.set_option('display.max_columns', None)

    json_settings = JsonReader(ACCOUNT_SETTINGS_PATH)
    credentials = JsonReader(CREDENTIALS_FILE_PATH)
    action_writer = ActionWriter()
    symbol = json_settings.get_symbol()
    timeframe = json_settings.get_timeframe()

    context_factory = ContextFactory(production=PRODUCTION)
    context = context_factory.create_context(credentials.get_json_data())
    
    symbol_factory = SymbolFactory(production=PRODUCTION)
    symbol = symbol_factory.create_symbol(symbol, timeframe, candles_mock_location=CANDLES_MOCK_LOCATION, ticks_mock_location=TICKS_MOCK_LOCATION)

    account_factory = AccountFactory(production=PRODUCTION)
    account = account_factory.create_account(symbol, balance = 99747.35, profit = 0, action_writer=action_writer)

    trade_execution_factory = TradeExecutionFactory(production=PRODUCTION)
    trade_executor = trade_execution_factory.create_trade_executor(account)
    
    strategy = EmaStrategy(symbol,EMA_SHORT,EMA_LONG, action_writer)

    trade_bot = TradeBot(context,action_writer, strategy, symbol, account, trade_executor)
    trade_bot.start()
    kill_bot = input()
    if (kill_bot == 'X'):
        trade_bot.stop()

if __name__ == '__main__':
    main()