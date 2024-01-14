
from src.interfaces import IMetaTrader
from src.context_mt5 import ContextMT5
from src.context_sim import ContextSimulator

class MetaTraderFactory():

    production: bool

    def __init__(self, production: bool):
        self.production = production

    def create_meta_trader(self, json_settings: dict, credentials: dict) -> IMetaTrader:
        if (self.production):
            return ContextMT5(json_settings, credentials)
        else:
            return ContextSimulator(json_settings, credentials)
