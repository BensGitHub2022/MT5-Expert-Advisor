from enum import Enum
import MetaTrader5 as mt5

class Timeframe(Enum):
    one_minute = mt5.TIMEFRAME_M1
    two_minutes = mt5.TIMEFRAME_M2
    three_minutes = mt5.TIMEFRAME_M3
    four_minutes = mt5.TIMEFRAME_M4
    five_minutes = mt5.TIMEFRAME_M5
    six_minutes = mt5.TIMEFRAME_M6
    ten_minutes = mt5.TIMEFRAME_M10
    twelve_minutes = mt5.TIMEFRAME_M12
    fifteen_minutes = mt5.TIMEFRAME_M15
    twenty_minutes = mt5.TIMEFRAME_M20
    thirty_minutes = mt5.TIMEFRAME_M30
    one_month = mt5.TIMEFRAME_MN1
    one_hour = mt5.TIMEFRAME_H1
    two_hours = mt5.TIMEFRAME_H2
    three_hours = mt5.TIMEFRAME_H3
    four_hours = mt5.TIMEFRAME_H4
    six_hours = mt5.TIMEFRAME_H6
    eight_hours = mt5.TIMEFRAME_H8
    one_day = mt5.TIMEFRAME_D1