
from src.interfaces import IContext

class ContextSimulator(IContext):

    json_settings: dict
    credentials: dict    

    def __init__(self, credentials: dict):
        """
        Initializes MetaTrader object
        :param credentials: A dict containing MetaTrader5 login details.
        """
        self.credentials = credentials

    def connect(self) -> bool:
        # always happy
        print("Trading bot initialized!")
        print("Trading bot login successful!")
        return True
    
