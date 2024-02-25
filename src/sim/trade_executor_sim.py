import pandas as pd

from src.shared_helper_functions import calc_lot_size

RISK = .02

class TradeExecutorSimulator():

    current_risk_per_trade: float 
    current_lot_size: float
    account_info: object

    def __init__(self, account: object) -> None:
        self.current_risk_per_trade = 0.0
        self.current_lot_size = 0.0
        self.account_info = account
    
    def place_order(self, symbol, signal, price, deviation) -> bool:
        balance = self.account_info.get_account_balance()
        volume = calc_lot_size(price, balance)
        type = signal['action_str']
        capital_committed = (-1)*(volume * price)
        result_add_position = self.account_info.add_position(symbol,type,volume,price)
        result_update_balance = self.account_info.update_balance(capital_committed)
        print("result of order: ")
        print("add position: {}, update balance: {}".format(result_add_position, result_update_balance))
        print("1. order_send: {} {} {} lots at {} with deviation={} points".format(signal['action_str'], symbol,volume,price,deviation))
        return True

    def close_position(self, position, bid, ask, deviation) -> bool:
        ticket = position.ticket
        self.account_info.update_position(ticket)
        result_remove_position = self.account_info.remove_position(ticket)
        print("result of order: ")
        print("closed position: {}, update balance: {}".format(result_remove_position, self.account_info.get_account_balance()))
        print("1. order_send: {} position on {} {} lots closed at {} with deviation={} points".format(
            "buy" if position.type == 1 else "sell", 
            position.symbol, 
            round(float(position.volume),2), 
            round(float(ask),2) if position.type == 1 else round(float(bid),2),
            deviation))
        return True
    
    def close_all_positions(self, bid, ask, deviation) -> bool:
        positions = self.account_info.get_positions()
        for position in positions:
            self.close_position(position, bid, ask, deviation)

    def do_nothing(self) -> None:
        #print("No actionable trades!")
        return
