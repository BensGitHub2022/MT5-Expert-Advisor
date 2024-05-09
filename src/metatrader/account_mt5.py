import MetaTrader5 as mt5
from datetime import datetime;

from src.interfaces import IAccount


class AccountMT5(IAccount):

    def get_account_info(self) -> dict:
        account_info = mt5.account_info()
        if account_info is None:
            raise RuntimeError('No account info returned from MT5. Error is ' + str(mt5.last_error() or ''))
        return account_info._asdict()
    
    def get_account_balance(self) -> float:
        account_info_dict = self.get_account_info()
        balance = account_info_dict['balance']
        return balance
    
    def get_account_profit(self) -> float:
        account_info_dict = self.get_account_info()
        profit = account_info_dict['profit']
        return profit
    
    def get_positions(self) -> dict: # Note on 1.21.24 that MT5 returns positions as a named Tuple
        try:
            positions = mt5.positions_get()
            return positions
        except BaseException:
            raise RuntimeError('No positions returned from MT5. Error is ' + str(mt5.last_error() or ''))
    
    def get_deal_history(self) -> dict:
        try:
            start = datetime(2010, 1, 1)
            end = datetime.now()
            deals = mt5.history_deals_get(start, end)
            list = [deal._asdict() for deal in deals]
            return { "history": list }
        except BaseException:
            raise RuntimeError('No historical positions returned from MT5. Error is ' + str(mt5.last_error() or ''))


    # NOTE: The presentation of positions is much more human readable when you use the code below.
    # In order to log the output of positions to a csv file it might be beneficial to uncomment this function and send it to action_writer
    # Currently we only record positions when running in simulation mode
    # Positions are readily available from MT5 terminal but it might be wise to keep our own record in a csv
    """
    def get_positions_df(self) -> pd.DataFrame:
        self.get_positions()
        self.positions_df = pd.DataFrame(list(self.positions),columns=self.positions[0]._asdict().keys())
        return self.positions_df
    """