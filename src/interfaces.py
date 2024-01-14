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

class ITradeExecutor(abc.ABC):

    @abc.abstractmethod
    def place_order(self) -> bool:
        pass

    @abc.abstractmethod
    def close_position(self) -> bool:
        pass

    @abc.abstractmethod
    def calc_lot_size(self) -> float:
        pass

class IAccount(abc.ABC):

    @abc.abstractmethod
    def get_positions(self) -> dict:
        pass

    @abc.abstractmethod
    def get_account_balance(self) -> float:
        pass

    


