
from src.interfaces import ISymbols
from src.symbols_mt5 import SymbolsMT5
from src.symbols_sim import SymbolsSimulator

class SymbolsFactory():

    production: bool

    def __init__(self, production: bool):
        self.production = production

    def create_symbol(self, symbol, timeframe, candles_mock_location = "mock/candlesticks.csv", ticks_mock_location="mock/ticks.csv") -> ISymbols:
        if (self.production):
            return SymbolsMT5(symbol, timeframe)
        else:
            return SymbolsSimulator(symbol, timeframe, candles_mock_location, ticks_mock_location)