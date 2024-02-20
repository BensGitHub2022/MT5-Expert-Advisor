
from src.metatrader.context_mt5 import ContextMT5
from src.sim.context_sim import ContextSimulator
from src.interfaces import IContext


class ContextFactory():

    production: bool

    def __init__(self, production: bool):
        self.production = production

    def create_context(self, credentials: dict) -> IContext:
        if (self.production):
            return ContextMT5(credentials)
        else:
            return ContextSimulator(credentials)
