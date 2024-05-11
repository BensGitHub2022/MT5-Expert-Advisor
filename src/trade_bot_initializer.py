from src.interfaces import IContext
from src.factories.account_factory import AccountFactory
from src.action_writer import ActionWriter
from src.ema_strategy import EmaStrategy
from src.factories.symbol_factory import SymbolFactory
from src.pool_manager import PoolManager
from src.trade_bot import TradeBot
from src.factories.trade_executor_factory import TradeExecutionFactory
from src.ws_server import Messenger, TradeBotWebsocketServer

class TradeBotInitializer():
    mt5_context: IContext
    pool_manager: PoolManager
    
    def __init__(self, context: IContext, pool_manager: PoolManager):
        self.mt5_context = context
        self.pool_manager = pool_manager
    
    def start_trade_bot(self, symbol_name: str, ema_short: int, ema_long: int):
        action_writer = ActionWriter()
        messenger = Messenger()
        ws_server = TradeBotWebsocketServer(messenger)
        
        symbol_factory = SymbolFactory(True)
        symbol = symbol_factory.create_symbol(symbol_name, "one_minute", candles_mock_location='config.candlesticks_filepath', ticks_mock_location='config.ticks_filepath')

        account_factory = AccountFactory(True)
        account = account_factory.create_account(balance = 100000, profit = 0, action_writer=action_writer)

        trade_execution_factory = TradeExecutionFactory(True)
        trade_executor = trade_execution_factory.create_trade_executor(account, symbol, messenger)
        
        strategy = EmaStrategy(symbol, ema_short, ema_long, action_writer, console_output=True)

        trade_bot = TradeBot(self.mt5_context, action_writer, strategy, symbol, account, trade_executor)
        
        self.pool_manager.pool.submit(trade_bot.start)
        messenger.start()
        ws_server.start()
        
        return "200"