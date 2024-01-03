
import threading
import time
from src.interfaces import IStrategy, IMetaTrader

class TradeBot(object):
    
    # instance variables (passed in the constructor)
    strategy: IStrategy
    meta_trader: IMetaTrader

    # instance variables (created internally)
    thread: threading.Thread
    cancelled: bool

    def __init__(
            self,
            strategy: IStrategy,
            meta_trader: IMetaTrader):
        self.strategy = strategy
        self.meta_trader = meta_trader
        self.thread = threading.Thread(target=trade_bot_thread_func, args=(self,))
        self.cancelled = False

    def start(self):
        self.thread.start()

    def stop(self):
        self.cancelled = True
        self.thread.join()

    def thread_func(self):

        connected = self.meta_trader.connect()
        if (not connected):
            return

        seed = self.meta_trader.get_seed()
        self.strategy.process_seed(seed)

        n = 0
        while (not self.cancelled):
            next = self.meta_trader.get_next()
            self.strategy.process_next(next)

            # ask strategy what it wants to do
        
            result = "Traded!"
            print(result + " .. " + str(n))
            time.sleep(2)
            n = n + 1
        return

def trade_bot_thread_func(inst: TradeBot):
    inst.thread_func()
