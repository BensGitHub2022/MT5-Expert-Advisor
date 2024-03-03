from src.metatrader.account_mt5 import AccountMT5
from src.sim.account_sim import AccountSimulator
from src.interfaces import IAccount


class AccountFactory():

    production: bool

    def __init__(self, production: bool):
        self.production = production

    def create_account(self, balance=100000, profit=0, action_writer = object) -> IAccount:
        if (self.production):
            return AccountMT5()
        else:
            return AccountSimulator(balance, profit, action_writer)