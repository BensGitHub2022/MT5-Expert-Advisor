import pandas as pd

RISK = .02

class TradeExecutorAdapter():

    current_balance: float
    current_risk_per_trade: float 
    current_lot_size: float
    
    positions: dict
    positions_df: pd.DataFrame

    def __init__(self, account_balance = 100000) -> None:
        self.current_risk_per_trade = 0.0
        self.current_lot_size = 0.0
        self.current_balance = self.get_account_balance(account_balance)
        self.positions_df = pd.DataFrame()

    def calc_risk_per_trade(self) -> float:
        self.current_risk_per_trade = self.current_balance * RISK
        return self.current_risk_per_trade

    def calc_lot_size(self, price) -> float:
        self.current_risk_per_trade = self.calc_risk_per_trade()
        self.current_lot_size = self.current_risk_per_trade / price
        return self.current_lot_size

    def place_order(self, symbol, signal, price, deviation) -> bool:

        volume = self.calc_lot_size(price)

        





    def get_account_balance(self, account_balance = 100000) -> float:
        return account_balance