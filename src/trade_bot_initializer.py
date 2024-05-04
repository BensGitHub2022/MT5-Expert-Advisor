from flask import Response
from src.interfaces import IContext
from src.pool_manager import PoolManager
from src.config import Config
from src.factories.account_factory import AccountFactory
from src.action_writer import ActionWriter
from src.ema_strategy import EmaStrategy
from src.factories.symbol_factory import SymbolFactory
from src.trade_bot import TradeBot
from src.factories.trade_executor_factory import TradeExecutionFactory

class TradeBotInitializer():
    counter = 0
    symbol_names = ["USDCNH", "USDJPY", "EURUSD"]
    mt5_context: IContext
    
    def __init__(self, context: IContext):
        self.mt5_context = context
    
    def start_trade_bot(self):
        action_writer = ActionWriter()
        
        symbol_factory = SymbolFactory(True)
        symbol = symbol_factory.create_symbol(self.symbol_names[self.counter], "one_minute", candles_mock_location='config.candlesticks_filepath', ticks_mock_location='config.ticks_filepath')

        account_factory = AccountFactory(True)
        account = account_factory.create_account(balance = 100000, profit = 0, action_writer=action_writer)

        trade_execution_factory = TradeExecutionFactory(True)
        trade_executor = trade_execution_factory.create_trade_executor(account, symbol)
        
        strategy = EmaStrategy(symbol, 2, 3, action_writer, console_output=True)

        trade_bot = TradeBot(self.mt5_context, action_writer, strategy, symbol, account, trade_executor)
        
        trade_bot.start()
        self.counter += 1
        
        try:
            while(not trade_bot.cancelled):
                kill_bot = input()
                print(kill_bot + " is not a recognized command!")
        except KeyboardInterrupt:
            trade_bot.cancelled = True
            trade_bot.stop()
        # pool_manager = PoolManager()
        # if self.counter < len(self.symbol_names):
        #     print('starting trade bot')
        #     order_bot = OrderBot(self.symbol_names[self.counter])
        #     pool_manager.pool.submit(order_bot.check_for_trades, pool_manager.pipeline, pool_manager.event)
        #     print('submitted to pool for ' + self.symbol_names[self.counter])
        #     self.counter += 1
        # return Response("{'a':'b'}", status=201, mimetype='application/json')