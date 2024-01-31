import MetaTrader5 as meta
from flask import Flask, jsonify
from typing import List, Callable

class Endpoint():
    name: str
    handler: Callable

    def __init__(self, name: str, handler: Callable):
        self.name = name
        self.handler = handler

class API():
    app = None

    def __init__(self, name, endpoints: List[Endpoint]):
        self.app = Flask(name)
        for e in endpoints:
            self.app.add_url_rule(e.name, view_func=e.handler)

    def run(self):
        self.app.run("localhost", 5000)





















# app = Flask(__name__)

# @app.route("/orders-open")
# def get_open_orders():
#     try:
#         tuple = meta.orders_get()
#         orders_arr = []
#         for o in tuple:
#             data = {
#                 "ticket": o.ticket,
#                 "time_setup": o.time_setup_msc,
#                 "order_type": o.type,
#                 "volume_current": o.volume_current,
#                 "stop_loss": o.sl,
#                 "take_profit": o.tp,
#                 "price_open": o.price_open,
#                 "price_current": o.price_current,
#                 "symbol": o.symbol,
#                 "comment": o.comment
#             }
#             orders_arr.append(data)
#         return jsonify({ "orders": orders_arr }), 200
#     except BaseException:
#         return jsonify({ "error": meta.last_error() }), 500
    
# @app.route("/orders-closed")
# def get_closed_orders():
#     try:
#         tuple = meta.history_deals_get()
#         orders_arr = []
#         for o in tuple:
#             data = {
#                 "ticket": o.ticket,
#                 "time": o.time_msc,
#                 "order_type": o.type,
#                 "volume": o.volume,
#                 "profit": o.profit,
#                 "symbol": o.symbol,
#                 "comment": o.comment,
#             }
#             orders_arr.append(data)
#         return jsonify({ "orders": orders_arr }), 200
#     except BaseException:
#         return jsonify({ "error": meta.last_error() }), 500

# app.run(debug=True)