# import pandas as pd # Not used in main unless for debugging
import warnings # Bad
from pandas.errors import SettingWithCopyWarning # Bad

from api.web_service import WebService

from src.action_writer import ActionWriter
from src.constants import production
from src.factories.account_factory import AccountFactory
from src.trade_bot_manager import TradeBotManager

def main():
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
    
    account_factory = AccountFactory(production)
    account = account_factory.create_account(balance = 100000, profit = 0, action_writer=action_writer)
    
    # set up trade bot manager (manages bot thread pool)
    trade_bot_manager = TradeBotManager()
    web_service = WebService(__name__, trade_bot_manager, account, action_writer)
    web_service.run()
    
    # stay alive until there's a keyboard interrupt
    try:
        while(True):
            kill_bot = input()
            print(kill_bot + " is not a recognized command!")
    except KeyboardInterrupt:
        print("shutting down")
        trade_bot_manager.stop_all_bots()
        web_service.stop()
    
    input()

if __name__ == '__main__':
    main()

