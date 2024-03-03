# import pandas as pd # Not used in main unless for debugging
import warnings # Bad
from pandas.errors import SettingWithCopyWarning # Bad

import sys

from src.factories.account_factory import AccountFactory
from src.action_writer import ActionWriter
from src.factories.context_factory import ContextFactory
from src.ema_strategy import EmaStrategy
from src.factories.symbol_factory import SymbolFactory
from src.trade_bot import TradeBot
from src.factories.trade_executor_factory import TradeExecutionFactory
from src.config import Config

# NOTE: For websocket test
from src.interfaces import IMessenger
import threading
import asyncio
import websockets
import websockets.sync
import websockets.sync.server


class Messenger(IMessenger):
    sem = threading.Semaphore()
    lock = threading.Lock()
    queue = list()

    def queue_message(self, message: str) -> None:
        self.lock.acquire()
        self.queue.append(message)
        self.sem.release()
        self.lock.release()

    def get_message(self) -> str:
        self.sem.acquire()
        message = ""
        self.lock.acquire()
        if (self.queue != []):
            message = self.queue.pop(0)
        self.lock.release()
        return message

messenger = Messenger()

def trade_bot_service(websocket):
    while True:
        message = messenger.get_message()
        if (message != ""):
            websocket.send(message)

def server_thread_proc():
    with websockets.sync.server.serve(trade_bot_service, "localhost", 5678) as server:
        server.serve_forever()


def main():
    thread = threading.Thread(target=server_thread_proc)
    thread.start()

    # NOTE: Args Key:
    # 1 - symbol name OR settings
    # 2 - Production flag, 1 == True, 0 == False
    # 3 - EMA short
    # 4 - EMA long
    # Example: BTCUSD 1 500 1000
    args = sys.argv[1:]
    config = Config(args)
    
    # NOTE: (Supress warnings) Need to decide if these present true issues.
    warnings.simplefilter(action='ignore', category=FutureWarning) # Bad <- this one relates to passing NaN to pd.concat, will be depricated in future
    warnings.simplefilter(action='ignore', category=SettingWithCopyWarning) # Bad <- this one relates to copy of a slice of a dataframe
    # OR
    # pd.set_option('mode.chained_assignment', None)
    # OR
    # with pd.option_context('mode.chained_assignment', None):
    # ^ needs to implemented in method of calling function

    # Composition root
    print("Hello Trade Bot!")

    action_writer = ActionWriter()

    context_factory = ContextFactory(production=config.production)
    context = context_factory.create_context(config.credentials)
    
    symbol_factory = SymbolFactory(production=config.production)
    symbol = symbol_factory.create_symbol(config.symbol, config.timeframe, candles_mock_location=config.candlesticks_filepath, ticks_mock_location=config.ticks_filepath)

    account_factory = AccountFactory(production=config.production)
    account = account_factory.create_account(balance = 100000, profit = 0, action_writer=action_writer)

    trade_execution_factory = TradeExecutionFactory(production=config.production)
    trade_executor = trade_execution_factory.create_trade_executor(account, symbol)
    
    strategy = EmaStrategy(symbol,config.ema_short,config.ema_long, action_writer, console_output=config.production)

    trade_bot = TradeBot(messenger, context, action_writer, strategy, symbol, account, trade_executor)
    
    trade_bot.start()
    
    try:
        while(not trade_bot.cancelled):
            kill_bot = input()
            print(kill_bot + " is not a recognized command!")
    except KeyboardInterrupt:
        trade_bot.cancelled = True
        trade_bot.stop()
        thread.join()

if __name__ == '__main__':
    main()