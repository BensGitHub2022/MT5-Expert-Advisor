from src.interfaces import ISymbol
from src.symbol_mt5 import SymbolMT5
from src.symbol_sim import SymbolSimulator


class SymbolFactory():

    production: bool

    def __init__(self, production: bool):
        self.production = production

    def create_symbol(self, symbol, timeframe, candles_mock_location = "mock/candlesticks.csv", ticks_mock_location="mock/ticks.csv") -> ISymbol:
        if (self.production):
            return SymbolMT5(symbol, timeframe)
        else:
            return SymbolSimulator(symbol, timeframe, candles_mock_location, ticks_mock_location)