
from src.interfaces import IMetaTrader
from src.meta_trader_adapter import MetaTraderAdapter
from src.meta_trader_mock import MetaTraderMock

class MetaTraderFactory():

    production: bool

    def __init__(self, production: bool):
        self.production = production

    def create_meta_trader(self, json_settings: dict, credentials: dict) -> IMetaTrader:
        if (self.production):
            return MetaTraderAdapter(json_settings, credentials)
        else:
            return MetaTraderMock(json_settings, credentials)
