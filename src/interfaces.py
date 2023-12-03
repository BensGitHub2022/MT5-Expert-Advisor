
import abc
from src.candlesticks import Candlesticks

class Trade(object):
    pass

# Meta trade interface - to abstract away and isolate MetaTrader SDK calls
class IMetaTrader(abc.ABC):

    @abc.abstractmethod
    def connect(self) -> bool:
        pass

    @abc.abstractmethod
    def get_seed(self) -> object:
        pass

    @abc.abstractmethod
    def get_next(self) -> object:
        pass

    @abc.abstractmethod
    def get_candlesticks(self) -> Candlesticks:
        pass

    @abc.abstractmethod
    def check_if_next(self) -> bool:
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
    def find_signals(self, data: object) -> int:
        pass
    