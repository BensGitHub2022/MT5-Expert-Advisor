from enum import Enum
from src.Enums.OrderType import OrderType
from src.Enums.Timeframe import Timeframe
from src.Enums.TradeAction import TradeAction
import MetaTrader5 as mt5

class MetaTraderEnumConverters:
    order_type_map = {
        OrderType.buy: mt5.ORDER_TYPE_BUY,
        OrderType.sell: mt5.ORDER_TYPE_SELL,
        OrderType.buy_limit: mt5.ORDER_TYPE_BUY_LIMIT,
        OrderType.sell_limit: mt5.ORDER_TYPE_SELL_LIMIT,
        OrderType.buy_stop: mt5.ORDER_TYPE_BUY_STOP,
        OrderType.sell_stop: mt5.ORDER_TYPE_SELL_STOP,
        OrderType.buy_stop_limit: mt5.ORDER_TYPE_BUY_STOP_LIMIT,
        OrderType.sell_stop_limit: mt5.ORDER_TYPE_SELL_STOP_LIMIT,
        OrderType.close_by: mt5.ORDER_TYPE_CLOSE_BY
    }
    
    timeframe_map = {
        Timeframe.one_minute: mt5.TIMEFRAME_M1,
        Timeframe.two_minutes: mt5.TIMEFRAME_M2,
        Timeframe.three_minutes: mt5.TIMEFRAME_M3,
        Timeframe.four_minutes: mt5.TIMEFRAME_M4,
        Timeframe.five_minutes: mt5.TIMEFRAME_M5,
        Timeframe.six_minutes: mt5.TIMEFRAME_M6,
        Timeframe.ten_minutes: mt5.TIMEFRAME_M10,
        Timeframe.twelve_minutes: mt5.TIMEFRAME_M12,
        Timeframe.fifteen_minutes: mt5.TIMEFRAME_M15,
        Timeframe.twenty_minutes: mt5.TIMEFRAME_M20,
        Timeframe.thirty_minutes: mt5.TIMEFRAME_M30,
        Timeframe.one_month: mt5.TIMEFRAME_MN1,
        Timeframe.one_hour: mt5.TIMEFRAME_H1,
        Timeframe.two_hours: mt5.TIMEFRAME_H2,
        Timeframe.three_hours: mt5.TIMEFRAME_H3,
        Timeframe.four_hours: mt5.TIMEFRAME_H4,
        Timeframe.six_hours: mt5.TIMEFRAME_H6,
        Timeframe.eight_hours: mt5.TIMEFRAME_H8,
        Timeframe.one_day: mt5.TIMEFRAME_D1
    }
    
    trade_action_map = {
        TradeAction.market_order: mt5.TRADE_ACTION_DEAL,
        TradeAction.pending_order: mt5.TRADE_ACTION_PENDING,
        TradeAction.change_open_pos_sltp: mt5.TRADE_ACTION_SLTP,
        TradeAction.modify_param: mt5.TRADE_ACTION_MODIFY,
        TradeAction.remove: mt5.TRADE_ACTION_REMOVE,
        TradeAction.close_by: mt5.TRADE_ACTION_CLOSE_BY
    }
    
    @staticmethod
    def get_mt5_order_type(order_type: str):
        return MetaTraderEnumConverters.order_type_map.get(order_type)
    
    @staticmethod
    def get_mt5_timeframe(timeframe: str) -> str:
        if timeframe == Timeframe.one_minute:
            return mt5.TIMEFRAME_M1
        return 1000
    
    @staticmethod
    def get_mt5_trade_action(trade_action: str):
        return MetaTraderEnumConverters.trade_action_map.get(trade_action)