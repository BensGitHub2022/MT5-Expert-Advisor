import MetaTrader5 as mt5

from src.interfaces import IContext
from src.json_reader import JsonReader

class ContextMT5(IContext): 

    CREDENTIALS_FILE_PATH = "config/credentials.json"

    def connect(self) -> bool:
        """
        Attempts to initialize and log into MetaTrader5.
        :returns bool: True if initialization and login succeeds. Otherwise, false.
        """

        try:
            credentials = JsonReader(file_path=self.CREDENTIALS_FILE_PATH).get_json_data()
            pathway = credentials["mt5"]["terminal_pathway"]
            login = credentials["mt5"]["login"]
            password = credentials["mt5"]["password"]
            server = credentials["mt5"]["server"]
            timeout = credentials["mt5"]["timeout"]

            initialized = mt5.initialize(
                pathway, login=login, password=password, server=server, timeout=timeout
            )
            if initialized:
                print("Trading account initialized!")
            else:
                raise ConnectionError

            # Safe to login here. Returns true if login succeeds. Otherwise, returns false.
            logged_in = mt5.login(
                login=login, password=password, server=server, timeout=timeout
            )

            if logged_in:
                print("Trading account login successful!")
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