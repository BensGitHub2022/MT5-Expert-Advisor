
from src.interfaces import IContext

class TradeExecutor():
    mt5_context: IContext
    
    def __init__(self, context):
        self.mt5_context = context

    def execute_trades(self, queue, event):
        print('executing trades')
        while not event.is_set(): # or not queue.empty():
            if not queue.empty():
                order = queue.get()
                print(
                    "Consumer got order: %s (queue size=%d)", order, queue.qsize()
                )

        print("Consumer received event. Exiting")