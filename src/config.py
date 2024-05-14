from src.constants import production
from src.json_reader import JsonReader

class Config():

    filepath: str
    candlesticks_filepath: str
    ticks_filepath: str
    credentials: dict
    timeframe: str

    json_reader: JsonReader

    def __init__(self, symbol_name: str) -> None:
        self.filepath: str = "config/" + symbol_name + ".json"
        self.json_reader = JsonReader(self.filepath)
        self.timeframe = self.json_reader.get_timeframe()
        
        if not production:
            self.candlesticks_filepath = self.json_reader.get_symbol_candlesticks_filepath()
            self.ticks_filepath = self.json_reader.get_symbol_ticks_filepath()
        else:
            self.candlesticks_filepath = ""
            self.ticks_filepath = ""
