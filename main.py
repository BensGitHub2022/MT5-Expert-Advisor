# import pandas as pd # Not used in main unless for debugging
import warnings # Bad
from pandas.errors import SettingWithCopyWarning # Bad

import sys

from api.web_service import WebService
from src.factories.context_factory import ContextFactory
from src.pool_manager import PoolManager

from src.config import Config
from src.trade_executor import TradeExecutor

def main():
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

    context_factory = ContextFactory(production=True)
    context = context_factory.create_context(config.credentials)

    WebService(__name__, None, context).run()

    trade_executor = TradeExecutor(context)
    pool_manager = PoolManager()
    pool_manager.pool.submit(trade_executor.execute_trades, pool_manager.pipeline, pool_manager.event)
    
    print('Enter the name of the symbol you would like to trade on: ')
    input()

if __name__ == '__main__':
    main()