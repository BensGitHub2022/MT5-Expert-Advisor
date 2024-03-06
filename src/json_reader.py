import json
import os


class JsonReader(object):

    file_path: str
    json_data: dict

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.json_data = self.get_json_from_file(self.file_path)

    def get_json_from_file(self, file_path: str) -> dict:
        """
        Attempts to deserialize the data in the given file path
        into a json array.

        :param file_path: The file path to deserialize from.
        :returns dict: A dictionary mirroring the json format.
        """

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf8") as file:
                # Convert to json object
                json_data = json.load(file)
                return json_data
        raise FileExistsError(f"Could not locate resource: {file_path}")
    
    def get_json_data(self) -> dict:
        return self.json_data

    def get_symbol(self) -> str:
        return self.json_data["mt5"]["symbol"]
    
    def get_timeframe(self) -> str:
        return self.json_data["mt5"]["timeframe"]
    
    def get_symbol_candlesticks_filepath(self) -> str:
        return self.json_data["mt5"]["candlesticks"]
    
    def get_symbol_ticks_filepath(self) -> str:
        return self.json_data["mt5"]["ticks"]
    
    def get_credentials(self) -> dict:
        return self.json_data["mt5"]
    