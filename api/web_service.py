import threading
from flask import Flask, request, jsonify
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
<<<<<<< HEAD
        self.app.add_url_rule("/orders-closed", view_func=self.get_history)  
        self.app.add_url_rule("/add_symbol", view_func=self.add_symbol)   
=======
        self.app.add_url_rule("/orders-closed", view_func=self.get_history)
        self.app.add_url_rule("/create-bot", view_func=self.create_bot, methods=['POST'])   
>>>>>>> main
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

<<<<<<< HEAD
=======
    def create_bot(self):
        try:
            data = request.json
            ema_short = int(data['ema_short'])
            ema_long = int(data['ema_long'])
            symbol = data['symbol']
            if ema_short >= ema_long or symbol not in ["BTCUSD", "ETHUSD"] or ema_short > 500 or ema_long > 1000:
                raise ValueError
            
            # Make bot

            response_payload = { "message": f"Bot created." }
            return jsonify(response_payload), 201
        except ValueError:
            return jsonify({ "error": "Illegal request." }), 400
>>>>>>> main
