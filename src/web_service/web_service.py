import threading
from flask import Flask
from flask_cors import CORS
from src.interfaces import IAccount

class WebService():

    account: IAccount

    def __init__(self, name, account: IAccount) -> None:
        
        self.account = account

        self.app = Flask(name)
        CORS(self.app)

        self.app.add_url_rule("/account_balance", view_func=self.get_account_balance)
        self.app.add_url_rule("/account_profit", view_func=self.get_account_profit)
        self.app.add_url_rule("/account", view_func=self.get_account)
        self.app.add_url_rule("/position", view_func=self.get_position)        
        self.flask_thread = threading.Thread(target=self.thread_proc)
        self.flask_thread.daemon = True
    
    def run(self):
        self.flask_thread.start()

    def get_account_balance(self):
        return f"<p>Account Balance: {self.account.get_account_balance()}</p>"
    
    def get_account_profit(self):
        return f"<p>Account Profit: {self.account.get_account_profit()}</p>"
    
    def get_account(self):
        return f"<p>Current Account: {self.account.get_account_json()}</p>"

    def get_position(self):
        return f"<p>Current Position: {self.account.get_position_json()}</p>"

    def thread_proc(self):
        self.app.run("localhost", 5000)