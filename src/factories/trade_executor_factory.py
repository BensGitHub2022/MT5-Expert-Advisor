from src.interfaces import IAccount, ISymbol
from src.metatrader.trade_executor_mt5 import TradeExecutorMT5
from src.sim.trade_executor_sim import TradeExecutorSimulator


class TradeExecutionFactory():

    production: bool

    def __init__(self, production: bool):
        self.production = production

    def create_trade_executor(self, account: IAccount, symbol: ISymbol):
        if (self.production):
            return TradeExecutorMT5(account, symbol)
        else:
            return TradeExecutorSimulator(account, symbol)