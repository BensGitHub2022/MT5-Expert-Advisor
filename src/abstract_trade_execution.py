import abc

class AbstractTradeExecution(abc.ABC):
    
    RISK = .02
    current_risk_per_trade = 0.0
    current_lot_size = 0.0
    account_info: object
    
    def __init__(self, account: object):
        self.account_info = account
        
    def calc_risk_per_trade(self) -> float:
        self.current_risk_per_trade = self.account_info.get_account_balance() * self.RISK
        return self.current_risk_per_trade

    def calc_lot_size(self, price) -> float:
        self.current_risk_per_trade = self.calc_risk_per_trade()
        self.current_lot_size = self.current_risk_per_trade / price
        return self.current_lot_size

    def close_all_positions(self, bid, ask, deviation) -> bool:
        positions = self.account_info.get_positions()
        for position in positions:
            self.close_position(position, bid, ask, deviation)
    
    def do_nothing(self):
        print("No actionable trades!")
        return
    
    @abc.abstractmethod
    def place_order(self) -> bool:
        pass

    @abc.abstractmethod
    def close_position(self) -> bool:
        pass

    @abc.abstractmethod
    def calc_lot_size(self) -> float:
        pass