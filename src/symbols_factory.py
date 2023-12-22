
from src.interfaces import IMetaTrader
from src.symbols_adapter import SymbolsAdapter
from src.symbols_mock import SymbolsMock

class SymbolsFactory():

    production: bool

    def __init__(self, production: bool):
        self.production = production

    def create_symbol(self, symbol, timeframe, mock_location = "pkg/candlesticks.csv") -> IMetaTrader:
        if (self.production):
            return SymbolsAdapter(symbol, timeframe)
        else:
            return SymbolsMock(symbol, timeframe, mock_location)