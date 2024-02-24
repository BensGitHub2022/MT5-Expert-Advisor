from src.interfaces import IAccountSnapshot

class AccountSnapshot(IAccountSnapshot):
    
    balance: float
    profit: float

    def __init__(self, balance, profit) -> None:
        self.balance = balance
        self.profit = profit


    def get_account_balance(self) -> float:
        return self.balance
    
    def get_account_profit(self) -> float:
        return self.profit
    
    def update_account_balance(self, new_balance: float) -> bool:
        self.balance = new_balance
        return True
    
    def update_account_profit(self, new_profit: float) -> bool:
        self.profit = new_profit
    
