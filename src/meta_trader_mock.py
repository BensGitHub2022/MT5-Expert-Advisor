
from src.interfaces import IMetaTrader, SymbolsAdapter, Trade

class MetaTraderMock(IMetaTrader):
    something: float

    def __init__(self):
        self.something = 0

    def connect(self) -> bool:
        # always happy
        return True

    def get_seed(self) -> object:
        return "Seed"

    def get_next(self) -> object:
        return "Next"

    def get_candlesticks(self) -> SymbolsAdapter:
        c = SymbolsAdapter()
        return c
    
    def check_if_next(self) -> bool:
        return True

    def execute_trade(self, trade: Trade):
        return "Traded!"
    
