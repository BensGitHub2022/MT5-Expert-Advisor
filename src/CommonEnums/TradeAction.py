from enum import Enum, auto

class TradeAction(Enum):
    market_order = auto()
    pending_order = auto()
    change_open_pos_sltp = auto()
    modify_param = auto()
    remove = auto()
    close_by = auto()