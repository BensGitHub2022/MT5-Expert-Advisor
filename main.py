# import pandas as pd # Not used in main unless for debugging
import warnings # Bad
from pandas.errors import SettingWithCopyWarning # Bad

from api.web_service import WebService
from src.factories.context_factory import ContextFactory
from src.interfaces import IContext
from src.pool_manager import PoolManager

from src.constants import production

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
    context = authenticate_trading_account()
    set_up_thread_pool(context)
    
    input()

def authenticate_trading_account() ->  IContext:
    context_factory = ContextFactory(production)
    context = context_factory.create_context()
    context.connect()
    
def set_up_thread_pool(context: IContext) -> WebService:
    pool_manager = PoolManager()
    web_service = WebService(__name__, None, context, pool_manager)
    web_service.run()
    return web_service

if __name__ == '__main__':
    main()