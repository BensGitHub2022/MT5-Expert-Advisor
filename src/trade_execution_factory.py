from src.abstract_trade_execution import AbstractTradeExecution
from src.trade_execution_mt5 import TradeExecutorMT5
from src.trade_execution_sim import TradeExecutorSimulator

class TradeExecutionFactory():

    production: bool

    def __init__(self, production: bool):
        self.production = production

    def create_trade_executor(self, account: object) -> AbstractTradeExecution:
        if (self.production):
            return TradeExecutorMT5(account)
        else:
            return TradeExecutorSimulator(account)