import threading

from src.action_writer import ActionWriter
from src.interfaces import (IAccount, IContext, IStrategy, ISymbol,
                            ITradeExecutor)
from src.signal import Signal
from src.signal_type import SignalType


class TradeBot(object):
    
    # instance variables (passed in the constructor)
    context: IContext
    strategy: IStrategy
    symbol: ISymbol
    account: IAccount
    trade_executor: ITradeExecutor
    action_writer: ActionWriter

    # instance variables (created internally)
    thread: threading.Thread
    cancelled: bool

    def __init__(self, context: IContext, action_writer: ActionWriter,strategy: IStrategy, symbol: ISymbol, account: IAccount, trade_executor: ITradeExecutor):
        self.context = context
        self.action_writer = action_writer
        self.strategy = strategy
        self.symbol = symbol
        self.account = account
        self.trade_executor = trade_executor

        self.thread = threading.Thread(target=trade_bot_thread_func, args=(self,))
        self.cancelled = False

    def start(self):
        print("Trade Bot started execution!")
        print("Press 'ctrl + C' to stop")
        self.thread.start()
        
    def stop(self):
        print("Trade Bot stopped execution!")
        self.cancelled = True
        self.thread.join()

    def thread_func(self):

        print("Using the " + self.strategy.get_strategy_name() + ", trading on " + self.symbol.get_symbol_name() + ", at " + self.symbol.get_symbol_timeframe() + ", with fast EMA: " + str(self.strategy.get_ema_short()) + " and slow EMA: " + str(self.strategy.get_ema_long()))
        
        print("---Trade Output---")

        self.strategy.set_current_candlestick_time()
        self.strategy.process_seed()

        self.strategy.record_action()

        while (not self.cancelled):
            if(self.strategy.check_next()):
                self.strategy.process_next()
                signal: Signal = self.strategy.check_signal()
                
                match signal.signal_type:
                    case SignalType.BUY | SignalType.SELL:
                        if(self.account.get_positions()):
                            self.trade_executor.close_all_positions(20)
                        self.trade_executor.place_order(signal,20) 
                    case SignalType.SKIP:
                        self.trade_executor.do_nothing()
                
                self.strategy.record_action()

        return

# Globally declared function
def trade_bot_thread_func(inst: TradeBot):
    inst.thread_func()
