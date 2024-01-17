
from src.interfaces import IContext
from src.context_mt5 import ContextMT5
from src.context_sim import ContextSimulator

class ContextFactory():

    production: bool

    def __init__(self, production: bool):
        self.production = production

    def create_context(self, json_settings: dict, credentials: dict) -> IContext:
        if (self.production):
            return ContextMT5(json_settings, credentials)
        else:
            return ContextSimulator(json_settings, credentials)
