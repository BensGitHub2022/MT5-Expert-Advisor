import abc

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

    


