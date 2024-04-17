import pandas as pd

from src.interfaces import IAccount, ISymbol
from src.shared_helper_functions import calc_lot_size
from src.signal import Signal
from src.signal_type import SignalType

class TradeExecutorSimulator():

    current_risk_per_trade: float 
    current_lot_size: float
    account_info: IAccount
    symbol: ISymbol

    def __init__(self, account: IAccount, symbol: ISymbol) -> None:
        self.current_risk_per_trade = 0.0
        self.current_lot_size = 0.0
        self.account_info = account
        self.symbol = symbol
    
    def place_order(self, signal: Signal, deviation) -> bool:
        symbol = self.symbol.get_symbol_name()
        time = self.symbol.get_tick_time()
        bid = self.symbol.get_symbol_info_bid()
        ask = self.symbol.get_symbol_info_ask()
        price = ask if signal.signal_type == SignalType.BUY else bid

        balance = self.account_info.get_account_balance()
        volume = calc_lot_size(price, balance)
        type = signal.signal_type.value
        capital_committed = (-1)*(volume * price)
        result_add_position = self.account_info.add_position(symbol,time,type,volume,price)
        result_update_balance = self.account_info.update_balance(capital_committed)
        print("result of order: ")
        print("add position: {}, update balance: {}".format(result_add_position, result_update_balance))
        print("1. order_send: {} {} {} lots at {} with deviation={} points".format(signal.signal_type.value, symbol,volume,price,deviation))
        return True

    def close_position(self, position, deviation) -> bool:
        bid = self.symbol.get_symbol_info_bid()
        ask = self.symbol.get_symbol_info_ask()
        if (position.type == "sell"):
            price = ask
        if (position.type == "buy"):
            price = bid

        ticket = position.ticket
        self.account_info.update_position(ticket, price)
        result_remove_position = self.account_info.remove_position(ticket)
        print("result of order: ")
        print("closed position: {}, update balance: {}".format(result_remove_position, self.account_info.get_account_balance()))
        print("1. order_send: {} position on {} {} lots closed at {} with deviation={} points".format(
            "buy" if position.type == "sell" else "sell", 
            position.symbol, 
            round(float(position.volume),2), 
            round(float(ask),2) if position.type == "sell" else round(float(bid),2),
            deviation))
        return True
    
    def close_all_positions(self, deviation) -> bool:
        positions = self.account_info.get_positions()
        for position in positions:
            self.close_position(position, deviation)

    def do_nothing(self) -> None:
        #print("No actionable trades!")
        return
