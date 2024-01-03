
from src.interfaces import ISymbols
from src.symbols_adapter import SymbolsAdapter
from src.symbols_mock import SymbolsMock

class SymbolsFactory():

    production: bool

    def __init__(self, production: bool):
        self.production = production

    def create_symbol(self, symbol, timeframe, candles_mock_location = "mock/candlesticks.csv", ticks_mock_location="mock/ticks.csv") -> ISymbols:
        if (self.production):
            return SymbolsAdapter(symbol, timeframe)
        else:
            return SymbolsMock(symbol, timeframe, candles_mock_location, ticks_mock_location)