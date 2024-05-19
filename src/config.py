from src.constants import production
from src.json_reader import JsonReader

class Config():

    filepath: str
    candlesticks_filepath: str
    ticks_filepath: str
    credentials: dict
    timeframe: str

    def __init__(self, symbol_name: str) -> None:
        json_reader: JsonReader
        if not production:
            self.filepath: str = "config/" + symbol_name + ".json"
            json_reader = JsonReader(self.filepath)
            self.candlesticks_filepath = json_reader.get_symbol_candlesticks_filepath()
            self.ticks_filepath = json_reader.get_symbol_ticks_filepath()
        else:
            self.filepath = "config/settings.json"
            json_reader = JsonReader(self.filepath)
            self.candlesticks_filepath = ""
            self.ticks_filepath = ""

        self.timeframe = json_reader.get_timeframe()
