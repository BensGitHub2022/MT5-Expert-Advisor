import abc

# Meta trade interface - to abstract away and isolate MetaTrader SDK calls
class AbstractContext(abc.ABC):
    
    json_settings: dict
    credentials: dict

    def __init__(self, json_settings: dict, credentials: dict):
        """
        Initializes MetaTrader object
        :param json_settings: A dict containing symbol trading details.
        :param credentials: A dict containing MetaTrader5 login details.
        """
        self.json_settings = json_settings
        self.credentials = credentials

    @abc.abstractmethod
    def connect(self) -> bool:
        pass