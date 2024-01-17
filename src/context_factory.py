
from src.abstract_context import AbstractContext
from src.context_mt5 import ContextMT5
from src.context_sim import ContextSimulator

class ContextFactory():

    production: bool

    def __init__(self, production: bool):
        self.production = production

    def create_context(self, json_settings: dict, credentials: dict) -> AbstractContext:
        if (self.production):
            return ContextMT5(json_settings, credentials)
        else:
            return ContextSimulator(json_settings, credentials)
