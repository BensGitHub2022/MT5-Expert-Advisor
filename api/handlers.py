from flask import jsonify
import MetaTrader5 as meta
from datetime import datetime

def get_open_orders():
    try:
        tuple = meta.orders_get()
        orders_arr = []
        for o in tuple:
            data = {
                "ticket": o.ticket,
                "time_setup": o.time_setup_msc,
                "order_type": o.type,
                "volume_current": o.volume_current,
                "stop_loss": o.sl,
                "take_profit": o.tp,
                "price_open": o.price_open,
                "price_current": o.price_current,
                "symbol": o.symbol,
                "comment": o.comment
            }
            orders_arr.append(data)
        return jsonify({ "orders": orders_arr }), 200
    except BaseException:
        return jsonify({ "error": meta.last_error() }), 500

def get_closed_orders():

    try:
        tuple = meta.history_deals_get(datetime(2010, 1, 1), datetime.now())
        orders_arr = []
        for o in tuple:
            data = {
                "ticket": o.ticket,
                "time": o.time_msc,
                "order_type": o.type,
                "volume": o.volume,
                "profit": o.profit,
                "symbol": o.symbol,
                "comment": o.comment,
            }
            orders_arr.append(data)
        return jsonify({ "orders": orders_arr }), 200
    except BaseException:
        return jsonify({ "error": meta.last_error() }), 500
