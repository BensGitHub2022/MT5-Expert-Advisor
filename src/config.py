from src.constants import production
from src.json_reader import JsonReader

# Path to MetaTrader5 login details.
ACCOUNT_SETTINGS_PATH = "config/settings.json"
CREDENTIALS_FILE_PATH = "config/credentials.json"

class Config():

    filepath: str
    candlesticks_filepath: str
    ticks_filepath: str
    credentials: dict

    json_reader: JsonReader

    def __init__(self) -> None:
        self.credentials = JsonReader(file_path=CREDENTIALS_FILE_PATH).get_json_data()
        


        