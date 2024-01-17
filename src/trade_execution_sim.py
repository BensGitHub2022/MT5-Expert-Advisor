import pandas as pd

from src.abstract_trade_execution import AbstractTradeExecution

class TradeExecutorSimulator(AbstractTradeExecution):

    current_profit: float # have we defined yet?
    
    positions: dict
    positions_df: pd.DataFrame # necessary?

    def place_order(self, symbol, signal, price, deviation) -> bool:
        volume = self.calc_lot_size(price)
        type = signal['action_str']
        capital_committed = (-1)*(volume * price)
        self.account_info.add_position(symbol,type,volume,price)
        self.account_info.update_balance(capital_committed)
        return True

    def close_position(self, position, bid, ask, deviation) -> bool:
        ticket = position.ticket
        self.account_info.update_position(ticket)
        profit = self.account_info.get_profit(ticket)
        self.account_info.remove_position(ticket)
        self.account_info.update_balance(profit)
        self.account_info.update_profit(profit)
        return True