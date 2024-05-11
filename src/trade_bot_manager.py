from uuid import uuid4
from src.interfaces import IContext
from src.factories.account_factory import AccountFactory
from src.action_writer import ActionWriter
from src.ema_strategy import EmaStrategy
from src.factories.symbol_factory import SymbolFactory
from src.pool_manager import PoolManager
from src.trade_bot import TradeBot
from src.factories.trade_executor_factory import TradeExecutionFactory
# from src.ws_server import Messenger

class TradeBotManager():
    mt5_context: IContext
    pool_manager: PoolManager
    trade_bot_id_future_map: dict
    id_bot_map: dict
    
    def __init__(self, context: IContext, pool_manager: PoolManager):
        self.mt5_context = context
        self.pool_manager = pool_manager
        self.id_bot_map = dict()
    
    def start_trade_bot(self, symbol_name: str, ema_short: int, ema_long: int, messenger: str):
        action_writer = ActionWriter()
        
        symbol_factory = SymbolFactory(True)
        symbol = symbol_factory.create_symbol(symbol_name, "one_minute", candles_mock_location='config.candlesticks_filepath', ticks_mock_location='config.ticks_filepath')

        account_factory = AccountFactory(True)
        account = account_factory.create_account(balance = 100000, profit = 0, action_writer=action_writer)

        trade_execution_factory = TradeExecutionFactory(True)
        trade_executor = trade_execution_factory.create_trade_executor(account, symbol, messenger)
        
        strategy = EmaStrategy(symbol, ema_short, ema_long, action_writer, console_output=True)

        trade_bot = TradeBot(messenger, self.mt5_context, action_writer, strategy, symbol, account, trade_executor)
        
        try: 
            self.pool_manager.pool.submit(trade_bot.run)
            self.id_bot_map[trade_bot.uuid] = trade_bot
            return trade_bot.get_properties_as_dict()
        except:
            return None
    
    def delete_trade_bot(self, bot_id: int):
        if bot_id in self.id_bot_map:
            self.id_bot_map[bot_id].cancel()
            del self.id_bot_map[bot_id]
            return True
        return False

    def get_details_for_all_bots(self):
        bot_details = []
        for bot in self.id_bot_map.values():
            bot_details.append(bot.get_properties_as_dict())
        return bot_details
    
    def stop_all_bots(self):
        for bot in self.id_bot_map.values():
            bot.cancel()