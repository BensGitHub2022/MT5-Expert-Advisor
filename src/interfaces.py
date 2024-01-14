import abc

# Meta trade interface - to abstract away and isolate MetaTrader SDK calls
class IContext(abc.ABC):

    @abc.abstractmethod
    def connect(self) -> bool:
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
    
    """
    @abc.abstractmethod
    def check_signal(self) -> bool:
        pass
    """

class ISymbols(abc.ABC):
    
    @abc.abstractmethod
    def get_candlesticks(self, num_candlesticks) -> object:
        pass

    @abc.abstractmethod
    def get_candlestick_time(self) -> int:
        pass

    @abc.abstractmethod
    def get_symbol_info_tick(self) -> dict:
        pass

    


