import MetaTrader5 as mt5
import pandas as pd
from src.Enums.Timeframe import Timeframe
from src.Connections.AbstractConnection import AbstractConnection
from src.Connections.MT5.JsonReader import JsonReader

class MetaTraderConnection(AbstractConnection):
    # Paths to MetaTrader5 login details.
    credentials = JsonReader("src/Connections/MT5/credentials.json").get_json_data()
    json_settings = JsonReader("pkg/settings.json").get_json_data()

    def __init__(self):
        self.connect()
    
    """
    Attempts to initialize and log into MetaTrader5.
    :returns bool: True if initialization and login succeeds. Otherwise, False.
    """
    def connect(self) -> bool:

        try:
            pathway = self.credentials["mt5"]["terminal_pathway"]
            login = self.credentials["mt5"]["login"]
            password = self.credentials["mt5"]["password"]
            server = self.credentials["mt5"]["server"]
            timeout = self.json_settings["mt5"]["timeout"]

            initialized = mt5.initialize(
                pathway, login=login, password=password, server=server, timeout=timeout
            )

            if initialized:
                print("Trading bot initialized!")
            else:
                raise ConnectionError

            # Safe to login here. Returns true if login succeeds. Otherwise, returns false.
            logged_in = mt5.login(
                login=login, password=password, server=server, timeout=timeout
            )

            if logged_in:
                print("Trading bot login successful!")
            else:
                raise PermissionError

        except KeyError as e:
            print(f"The queried dictionary key does not exist: {e.args}")
            raise e
        except ConnectionError as e:
            print(f"Could not connect to MetaTrader5: {e.args}")
            raise e
        except PermissionError as e:
            print(f"Login failed to connect to MetaTrader 5: {e.args}")
            raise 
    
    def get_candles_for_symbol(self, symbol, timeframe, num_candlesticks) -> pd.DataFrame:
        try:
            if timeframe == Timeframe.one_minute:
                candles = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, num_candlesticks)
                return pd.DataFrame(candles)
            return None
        except Exception as e:
            print(e)
            raise
    
    def get_symbol_info_tick(self, symbol) -> dict:
        return mt5.symbol_info_tick(symbol)._asdict()
    
    def get_ask_price(self, symbol) -> int:
        return self.get_symbol_info_tick(symbol)['ask']
    
    def get_bid_price(self, symbol) -> int:
       return self.get_symbol_info_tick(symbol)['bid']
    
    def get_symbol_info(self, symbol) -> str:
        return mt5.symbol_info(symbol)._asdict()
    
    def place_order(self, symbol, signal, volume, price, deviation) -> bool:
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": round(float(volume),2),
            "price": round(float(price),2),
            "deviation": deviation,
            "magic": 100,
            "comment": "python script open",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        if 1:
            request["type"] = mt5.ORDER_TYPE_BUY
            print("buying")
        else:
            request["type"] = mt5.ORDER_TYPE_SELL
            print("selling")
        
        return mt5.order_send(request)
    
    def get_account_balance(self) -> float:
        return mt5.account_info()._asdict()['balance']
    
    def close_position(self, position, bid, ask, deviation) -> bool:
        request = {
            "action": TradeAction['market_order'].value,
            "position": position.ticket,
            "symbol": position.symbol,
            "volume": round(float(position.volume),2),
            "type": OrderType['buy'].value if position.type == 1 else OrderType['sell'].value,
            "price": round(float(ask),2) if position.type == 1 else round(float(bid),2),
            "deviation": deviation,
            "magic": 100,
            "comment": "python script close",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }

        return mt5.order_send(request)
    
    def get_positions(self) -> dict:
        return mt5.positions_get()
