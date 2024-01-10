from enum import auto, Enum

class OrderType(Enum):
    buy = auto()
    sell = auto()
    buy_limit = auto()
    sell_limit = auto()
    buy_stop = auto()
    sell_stop = auto()
    buy_stop_limit = auto()
    sell_stop_limit = auto()
    close_by = auto()
