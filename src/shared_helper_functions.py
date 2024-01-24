RISK = .02

def calc_risk_per_trade(balance: float) -> float:
        return balance * RISK

def calc_lot_size(price: float, balance: float) -> float:
        current_risk_per_trade = calc_risk_per_trade(balance)
        current_lot_size = current_risk_per_trade / price
        return current_lot_size