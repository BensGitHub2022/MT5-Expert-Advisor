from enum import Enum
import MetaTrader5 as mt5

class MetaTraderOrderTypeEnum(Enum):
    buy = mt5.ORDER_TYPE_BUY
    sell = mt5.ORDER_TYPE_SELL
    buy_limit = mt5.ORDER_TYPE_BUY_LIMIT
    sell_limit = mt5.ORDER_TYPE_SELL_LIMIT
    buy_stop = mt5.ORDER_TYPE_BUY_STOP
    sell_stop = mt5.ORDER_TYPE_SELL_STOP
    buy_stop_limit = mt5.ORDER_TYPE_BUY_STOP_LIMIT
    sell_stop_limit = mt5.ORDER_TYPE_SELL_STOP_LIMIT
    close_by = mt5.ORDER_TYPE_CLOSE_BY
