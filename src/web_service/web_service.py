import threading
from flask import Flask
from flask_cors import CORS
from src.interfaces import IAccountSnapshot

class WebService():

    account_snapshot: IAccountSnapshot

    def __init__(self, name, account_snapshot: IAccountSnapshot) -> None:
        
        self.account_snapshot = account_snapshot

        self.app = Flask(name)
        CORS(self.app)

        self.app.add_url_rule("/account_balance", view_func=self.get_account_balance)
        self.app.add_url_rule("/account_profit", view_func=self.get_account_profit)
        self.app.add_url_rule("/account", view_func=self.get_account)        
        self.flask_thread = threading.Thread(target=self.thread_proc)
        self.flask_thread.daemon = True
    
    def run(self):
        self.flask_thread.start()

    def get_account_balance(self):
        return f"<p>Account Balance: {self.account_snapshot.get_account_balance()}</p>"
    
    def get_account_profit(self):
        return f"<p>Account Profit: {self.account_snapshot.get_account_profit()}</p>"
    
    def get_account(self):
        return f"<p>Account Balance: {self.account_snapshot.get_account_balance()}</p><p>Account Profit: {self.account_snapshot.get_account_profit()}</p>"
    

    def thread_proc(self):
        self.app.run("localhost", 5000)