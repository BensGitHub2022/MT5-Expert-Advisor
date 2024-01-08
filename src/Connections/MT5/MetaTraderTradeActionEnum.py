from enum import Enum
import MetaTrader5 as mt5

class TradeAction(Enum):
    market_order = mt5.TRADE_ACTION_DEAL
    pending_order = mt5.TRADE_ACTION_PENDING
    change_open_pos_sltp = mt5.TRADE_ACTION_SLTP
    modify_param = mt5.TRADE_ACTION_MODIFY
    remove = mt5.TRADE_ACTION_REMOVE
    close_by = mt5.TRADE_ACTION_CLOSE_BY