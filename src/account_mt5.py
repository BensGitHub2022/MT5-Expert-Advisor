import MetaTrader5 as mt5
import pandas as pd

from src.interfaces import IAccount

class AccountMT5(IAccount):

    balance: float
    profit: float

    ticket: int # do we use this ticket variable in live implementation ? 1.21.24 - to decide
    symbol: object # should we pass a symbol object to this class ? 1.21.24 - implemented in sim class, need to add to live implementation
    
    positions_df: pd.DataFrame
    positions: dict

    def __init__(self, symbol) -> None:
        self.balance = self.get_account_balance()
        self.profit = self.get_account_profit()
        self.positions = dict()
        # self.positions_df = pd.DataFrame() # Not used
        self.symbol = symbol # Added to meet requirements of factory method and interface, currently not used. Will be updated when more dependency injection is added
        
    def get_account_info(self) -> dict:
        account_info_dict = mt5.account_info()._asdict()
        return account_info_dict
    
    def get_account_balance(self) -> float:
        account_info_dict = self.get_account_info()
        balance = account_info_dict['balance']
        return balance
    
    def get_account_profit(self) -> float:
        account_info_dict = self.get_account_info()
        profit = account_info_dict['profit']
        return profit
    
    def get_positions(self) -> tuple: # Note on 1.21.24 that MT5 returns positions as a named Tuple
        self.positions = mt5.positions_get()
        return self.positions
    
    # Unsure if this is necessary - easier to work with positions as a dict rather than a DataFrame # 1.21.24 - positions are actually Tuples
    """
    def get_positions_df(self) -> pd.DataFrame:
        self.get_positions()
        self.positions_df = pd.DataFrame(list(self.positions),columns=self.positions[0]._asdict().keys())
        return self.positions_df
    """