import sys
import threading
from uuid import UUID, uuid4
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.constants import allowed_symbol_names
from src.interfaces import IAccount
from src.trade_bot_manager import TradeBotManager

class WebService():

    account: IAccount
    trade_bot_manager: TradeBotManager

    def __init__(self, name: str, account: IAccount, trade_bot_manager: TradeBotManager) -> None:
        self.trade_bot_manager = trade_bot_manager
        self.account = account

        self.app = Flask(name)
        CORS(self.app)

        self.app.add_url_rule("/account", view_func=self.get_account)
        self.app.add_url_rule("/orders-open", view_func=self.get_positions)
        self.app.add_url_rule("/orders-closed", view_func=self.get_history)
        self.app.add_url_rule("/create-bot", view_func=self.create_bot, methods=['POST'])
        self.app.add_url_rule("/delete-bot", view_func=self.delete_bot, methods=['POST'])
        self.app.add_url_rule("/get-bots", view_func=self.get_all_bots)
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
    
    def thread_proc(self):
        self.app.run("localhost", 5000)

    def create_bot(self):
        try:
            http_body = request.json
            ema_short = int(http_body['ema_short'])
            ema_long = int(http_body['ema_long'])
            symbol = http_body['symbol']
            if ema_short >= ema_long or symbol not in allowed_symbol_names or ema_short > 500 or ema_long > 1000:
                raise ValueError
            
            trade_bot_properties_json = self.trade_bot_manager.start_trade_bot(symbol, ema_short, ema_long)
            
            if trade_bot_properties_json == None:
                return jsonify({ "message": "Bot creation failed." }), 500
            else:
                return jsonify(trade_bot_properties_json), 201
        except ValueError:
            return jsonify({ "error": "Illegal request." }), 400

    def delete_bot(self):
        http_body = request.json
        bot_id = UUID(http_body["id"])
        bot_deleted = self.trade_bot_manager.delete_trade_bot(bot_id)
        if bot_deleted:
            return jsonify({ "message": f"Bot with id {bot_id} deleted." }), 200
        else:
            return jsonify({ "message": "Bot deletion failed." }), 500

    def get_all_bots(self):
        return jsonify(self.trade_bot_manager.get_details_for_all_bots()), 200
    
    def stop(self):
        sys.exit(0)