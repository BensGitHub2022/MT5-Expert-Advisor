from src.account_mt5 import AccountMT5
from src.account_sim import AccountSimulator
from src.interfaces import IAccount


class AccountFactory():

    production: bool

    def __init__(self, production: bool):
        self.production = production

    def create_account(self, symbol, balance=100000, profit=0, action_writer = object) -> IAccount:
        if (self.production):
            return AccountMT5()
        else:
            return AccountSimulator(symbol, balance, profit, action_writer)