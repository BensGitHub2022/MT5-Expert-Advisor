from src.TradeBot import TradeBot
from src.TradingStrategies.ema_strategy import EmaStrategy
from src.Enums.Timeframe import Timeframe
from src.Enums.ConnectionOption import ConnectionOption

EMA_SHORT = 5
EMA_LONG = 8
SYMBOL = "BCHUSD"
TIMEFRAME = Timeframe.one_minute
CONNECTION_CHOICE = ConnectionOption.MT5

def main():
    strategy = EmaStrategy(EMA_SHORT, EMA_LONG)
    emaTradeBot = TradeBot(strategy, SYMBOL, TIMEFRAME, CONNECTION_CHOICE)
    
    emaTradeBot.look_for_trades()

main()