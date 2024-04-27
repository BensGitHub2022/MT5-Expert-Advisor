import threading
from flask import Flask
from flask_cors import CORS
from src.interfaces import IAccount
from src.interfaces import IContext
from src.trade_bot_initializer import TradeBotInitializer

class WebService():

    account: IAccount
    trade_bot_initializer: TradeBotInitializer

    def __init__(self, name, account: IAccount, context: IContext) -> None:
        self.trade_bot_initializer = TradeBotInitializer(context)
        self.account = account

        self.app = Flask(name)
        CORS(self.app)

        self.app.add_url_rule("/account", view_func=self.get_account)
        self.app.add_url_rule("/orders-open", view_func=self.get_positions)
        self.app.add_url_rule("/orders-closed", view_func=self.get_history)  
        self.app.add_url_rule("/add_symbol", view_func=self.add_symbol)   
        self.flask_thread = threading.Thread(target=self.thread_proc)
        self.flask_thread.daemon = True
    
    def run(self):
        self.flask_thread.start()

    def get_account(self):
        return self.account.get_account_info()

    def get_positions(self):
        return self.account.get_positions()
    
    def get_history(self):
        return self.account.get_deal_history()
    
    def add_symbol(self):
        print('adding symbol')
        return self.trade_bot_initializer.start_trade_bot()

    def thread_proc(self):
        self.app.run("localhost", 5000)

