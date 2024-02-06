import MetaTrader5 as mt5

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
    
    def get_positions(self) -> tuple: # Note on 1.21.24 that MT5 returns positions as a named Tuple
        positions = mt5.positions_get()
        if positions is None:
            raise RuntimeError('No positions returned from MT5. Error is ' + str(mt5.last_error() or ''))
        return positions

    # Unsure if this is necessary - easier to work with positions as a dict rather than a DataFrame # 1.21.24 - positions are actually Tuples
    """
    def get_positions_df(self) -> pd.DataFrame:
        self.get_positions()
        self.positions_df = pd.DataFrame(list(self.positions),columns=self.positions[0]._asdict().keys())
        return self.positions_df
    """