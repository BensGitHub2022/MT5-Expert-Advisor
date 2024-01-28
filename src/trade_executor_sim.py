import pandas as pd

from src.shared_helper_functions import calc_lot_size

RISK = .02

class TradeExecutorSimulator():

    current_risk_per_trade: float 
    current_lot_size: float

    current_profit: float # have we defined yet?
    
    positions: dict
    positions_df: pd.DataFrame # necessary?

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
        self.current_risk_per_trade = self.calc_risk_per_trade()
        self.current_lot_size = self.current_risk_per_trade / price
        return self.current_lot_size
    """

    def place_order(self, symbol, signal, price, deviation) -> bool:
        balance = self.account_info.get_account_balance()
        volume = calc_lot_size(price, balance)
        type = signal['action_str']
        capital_committed = (-1)*(volume * price)
        self.account_info.add_position(symbol,type,volume,price)
        self.account_info.update_balance(capital_committed)
        return True

    def close_position(self, position, bid, ask, deviation) -> bool:
        ticket = position.ticket
        self.account_info.update_position(ticket)
        balance_update = self.account_info.remove_position(ticket)
        self.account_info.update_balance(balance_update.capital)
        self.account_info.update_profit(balance_update.profit)
        return True
    
    def close_all_positions(self, bid, ask, deviation) -> bool:
        positions = self.account_info.get_positions()
        for position in positions:
            self.close_position(position, bid, ask, deviation)

    def do_nothing(self) -> None:
        print("No actionable trades!")
        return
