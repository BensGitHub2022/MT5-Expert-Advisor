from src.interfaces import IAccount
from src.account_mt5 import AccountMT5
from src.account_sim import AccountSimulator

class AccountFactory():

    production: bool

    def __init__(self, production: bool):
        self.production = production

    def create_account(self, symbol, balance=100000, profit=0):
        if (self.production):
            return AccountMT5(symbol)
        else:
            return AccountSimulator(symbol, balance, profit)