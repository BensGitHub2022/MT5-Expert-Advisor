
import abc
from src.symbols_adapter import SymbolsAdapter

class Trade(object):
    pass

# Meta trade interface - to abstract away and isolate MetaTrader SDK calls
class IMetaTrader(abc.ABC):

    @abc.abstractmethod
    def connect(self) -> bool:
        pass

    @abc.abstractmethod
    def execute_trade(self, trade: Trade) -> str:
        pass

class IStrategy(abc.ABC):

    @abc.abstractmethod
    def process_seed(self, data: object) -> bool:
        pass

    @abc.abstractmethod
    def process_next(self, data: object) -> bool:
        pass

    @abc.abstractmethod
    def check_next(self) -> bool:
        pass

    @abc.abstractmethod
    def check_signal(self) -> bool:
        pass
    