import MetaTrader5 as mt5
from enum import Enum

from src.shared_helper_functions import calc_lot_size

#RISK = .02

class TradeExecutorMT5():

    current_risk_per_trade: float 
    current_lot_size: float
    account_info: object

    def __init__(self, account: object) -> None:
        self.current_risk_per_trade = 0.0
        self.current_lot_size = 0.0
        self.account_info = account
    """
    def calc_risk_per_trade(self) -> float:
        self.current_risk_per_trade = self.account_info.get_account_balance() * RISK
        return self.current_risk_per_trade
    
    def calc_lot_size(self, price) -> float:
        self.current_risk_per_trade = calc_risk_per_trade(self.account_info.get_account_balance())
        self.current_lot_size = self.current_risk_per_trade / price
        return self.current_lot_size
    """
    
    def place_order(self, symbol, signal, price, deviation) -> bool:

        volume = calc_lot_size(price, self.account_info.get_account_balance())

        request = {
            "action": TradeAction['market_order'].value,
            "symbol": symbol,
            "volume": round(float(volume), 2),
            "type": OrderType[signal['action_str']].value,
            "price": round(float(price), 2),
            "deviation": deviation,
            "magic": 100,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        result = mt5.order_send(request)
        if result == None:
            raise RuntimeError('Error sending order: ' + str(mt5.last_error() or ''))
        print("result of order: ")
        print(result)
        print("1. order_send: {} {} {} lots at {} with deviation={} points".format(signal['action_str'], symbol,volume,price,deviation))
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("2. order_send failed, retcode={}".format(result.retcode))
            # request the result as a dictionary and display it element by element
            result_dict = result._asdict()
            for field in result_dict.keys():
                print("   {}={}".format(field, result_dict[field]))
                # if this is a trading request structure, display it element by element as well
                if field=="request":
                    trade_request_dict=result_dict[field]._asdict()
                    for trade_request_filled in trade_request_dict:
                        print("traderequest: {}={}".format(trade_request_filled,trade_request_dict[trade_request_filled]))
                        ### Need to decide what happens at order failure
            
            return False

        print("2. order_send done, ", result)
        print("opened position with POSITION_TICKET={}".format(result.order))

        return True
    
    def close_position(self, position, bid, ask, deviation) -> bool:
        
        request = {
            "action": TradeAction['market_order'].value,
            "position": position.ticket,
            "symbol": position.symbol,
            "volume": round(float(position.volume),2),
            "type": OrderType['buy'].value if position.type == 1 else OrderType['sell'].value,
            "price": round(float(ask),2) if position.type == 1 else round(float(bid),2),
            "deviation": deviation,
            "magic": 100,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        result = mt5.order_send(request)

        print("1. order_send: {} position on {} {} lots closed at {} with deviation={} points".format(
            "buy" if position.type == 1 else "sell", 
            position.symbol, 
            round(float(position.volume),2), 
            round(float(ask),2) if position.type == 1 else round(float(bid),2),
            deviation))
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print("2. order_send failed, retcode={}".format(result.retcode))
            # request the result as a dictionary and display it element by element
            result_dict = result._asdict()
            for field in result_dict.keys():
                print("   {}={}".format(field, result_dict[field]))
                # if this is a trading request structure, display it element by element as well
                if field=="request":
                    trade_request_dict=result_dict[field]._asdict()
                    for trade_request_filled in trade_request_dict:
                        print("traderequest: {}={}".format(trade_request_filled,trade_request_dict[trade_request_filled]))
            return False

        print("2. order_send done, ", result) 
        print("closed POSITION_TICKET={}, profit {}".format(position.ticket, position.profit))
    
    def close_all_positions(self, bid, ask, deviation) -> bool:
        positions = self.account_info.get_positions()
        for position in positions:
            self.close_position(position, bid, ask, deviation)
    
    def do_nothing(self) -> None:
        print("No actionable trades!")
        return
    
class OrderType(Enum):
    buy = mt5.ORDER_TYPE_BUY
    sell = mt5.ORDER_TYPE_SELL
    buy_limit = mt5.ORDER_TYPE_BUY_LIMIT
    sell_limit = mt5.ORDER_TYPE_SELL_LIMIT
    buy_stop = mt5.ORDER_TYPE_BUY_STOP
    sell_stop = mt5.ORDER_TYPE_SELL_STOP
    buy_stop_limit = mt5.ORDER_TYPE_BUY_STOP_LIMIT
    sell_stop_limit = mt5.ORDER_TYPE_SELL_STOP_LIMIT
    close_by = mt5.ORDER_TYPE_CLOSE_BY

class TradeAction(Enum):
    market_order = mt5.TRADE_ACTION_DEAL
    pending_order = mt5.TRADE_ACTION_PENDING
    change_open_pos_sltp = mt5.TRADE_ACTION_SLTP
    modify_param = mt5.TRADE_ACTION_MODIFY
    remove = mt5.TRADE_ACTION_REMOVE
    close_by = mt5.TRADE_ACTION_CLOSE_BY

