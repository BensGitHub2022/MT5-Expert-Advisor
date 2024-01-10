import os
import json

class JsonReader(object):
    json_data: dict

    def __init__(self, file_path: str) -> None:
        self.json_data = self.get_json_from_file(file_path)

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
    
    def get_symbols_collection(self) -> list:
        return self.json_data["mt5"]["symbols"]
    
    def get_symbol(self) -> str:
        return self.json_data["mt5"]["symbols"][0]
    
    def get_timeframe(self) -> str:
        return self.json_data["mt5"]["timeframe"]