import abc
import pandas as pd

class AbstractAccount(abc.ABC):
    
    balance: float
    profit: float

    ticket: int # do we use this ticket variable in live implementation ?
    symbol: object # should we pass a symbol object to this class ? 
    
    positions_df: pd.DataFrame
    positions = dict()

    @abc.abstractmethod
    def get_positions(self) -> dict:
        pass

    @abc.abstractmethod
    def get_account_balance(self) -> float:
        pass
    
    @abc.abstractmethod
    def get_account_profit(self) -> float:
        pass