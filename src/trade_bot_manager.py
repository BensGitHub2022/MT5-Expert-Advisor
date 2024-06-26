import concurrent.futures
from src.config import Config
from src.factories.context_factory import ContextFactory
from src.interfaces import IAccount, IContext
from src.factories.account_factory import AccountFactory
from src.action_writer import ActionWriter
from src.ema_strategy import EmaStrategy
from src.factories.symbol_factory import SymbolFactory
from src.trade_bot import TradeBot
from src.factories.trade_executor_factory import TradeExecutionFactory
from src.constants import production
from src.ws_server import Messenger, TradeBotWebsocketServer

# This class is a singleton. There should only ever be one trade bot manager
class TradeBotManager():

    context: IContext
    first_bot_created: bool
    id_bot_map: dict
    messenger: Messenger
    pool : concurrent.futures.ThreadPoolExecutor
    web_socket_server: TradeBotWebsocketServer

    def __new__(self):
        if not hasattr(self, 'instance'):
            context_factory = ContextFactory(production)
            self.context = context_factory.create_context()
            self.context.connect()
            
            self.first_bot_created = False
            self.id_bot_map = dict()
            self.messenger = Messenger()
            self.pool = concurrent.futures.ThreadPoolExecutor()
            self.web_socket_server = TradeBotWebsocketServer(self.messenger)
            self.instance = super(TradeBotManager, self).__new__(self)
        return self.instance
    
    def start_trade_bot(self, symbol_name: str, ema_short: int, ema_long: int, account: IAccount, action_writer: ActionWriter):
        config = Config(symbol_name)
        
        symbol_factory = SymbolFactory(production)
        symbol = symbol_factory.create_symbol(symbol_name, config.timeframe, candles_mock_location=config.candlesticks_filepath, ticks_mock_location=config.ticks_filepath)

        trade_execution_factory = TradeExecutionFactory(production)
        messenger = self.messenger if not self.first_bot_created else None
        trade_executor = trade_execution_factory.create_trade_executor(account, symbol, messenger)
        
        strategy = EmaStrategy(symbol, ema_short, ema_long, action_writer, console_output=True)

        trade_bot = TradeBot(messenger, self.context, action_writer, strategy, symbol, account, trade_executor)
        
        try: 
            self.pool.submit(trade_bot.run)
            if not self.first_bot_created:
                self.web_socket_server.start()
                self.messenger.start()
                self.first_bot_created = True
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
        self.web_socket_server.stop()
        self.messenger.stop()