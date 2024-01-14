
from src.interfaces import IMetaTrader

class ContextSimulator(IMetaTrader):

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

    def connect(self) -> bool:
        # always happy
        print("Trading bot initialized!")
        print("Trading bot login successful!")
        return True
    
