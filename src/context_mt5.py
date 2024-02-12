import MetaTrader5 as mt5

from src.interfaces import IContext


class ContextMT5(IContext): 

    credentials: dict

    def __init__(self, credentials: dict):
        """
        Initializes MetaTrader object
        :param credentials: A dict containing MetaTrader5 login details.
        """
        self.credentials = credentials

    def connect(self) -> bool:
        """
        Attempts to initialize and log into MetaTrader5.
        :returns bool: True if initialization and login succeeds. Otherwise, false.
        """

        try:
            pathway = self.credentials["mt5"]["terminal_pathway"]
            login = self.credentials["mt5"]["login"]
            password = self.credentials["mt5"]["password"]
            server = self.credentials["mt5"]["server"]
            timeout = self.credentials["mt5"]["timeout"]

            initialized = mt5.initialize(
                pathway, login=login, password=password, server=server, timeout=timeout
            )
            if initialized:
                print("Trading bot initialized!")
            else:
                raise ConnectionError

            # Safe to login here. Returns true if login succeeds. Otherwise, returns false.
            logged_in = mt5.login(
                login=login, password=password, server=server, timeout=timeout
            )

            if logged_in:
                print("Trading bot login successful!")
            else:
                raise PermissionError

        except KeyError as e:
            print(f"The queried dictionary key does not exist: {e.args}")
            raise e
        except ConnectionError as e:
            print(f"Could not connect to MetaTrader5: {e.args}")
            raise e
        except PermissionError as e:
            print(f"Login failed to connect to MetaTrader 5: {e.args}")
            raise e
        
        return True