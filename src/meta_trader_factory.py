
from src.interfaces import IMetaTrader
from src.meta_trader_adapter import MetaTraderAdapter
from src.meta_trader_mock import MetaTraderMock

class MetaTraderFactory():

    production: bool

    def __init__(self, production: bool):
        self.production = production

    def create_meta_trader(self) -> IMetaTrader:
        if (self.production):
            return MetaTraderAdapter()
        else:
            return MetaTraderMock()
