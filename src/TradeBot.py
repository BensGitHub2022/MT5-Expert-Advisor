from src.Enums.ConnectionOption import ConnectionOption
from src.Connections.AbstractConnection import AbstractConnection
from src.Connections.Mock.MockConnection import MockConnection
from src.Connections.MT5.MetaTraderConnection import MetaTraderConnection
from src.TradingStrategies.ema_strategy import EmaStrategy

NUM_CANDLESTICKS = 20

class TradeBot():
    connection: AbstractConnection
    strategy: EmaStrategy
    symbol: str
    timeframe: str
    
    def __init__(self, _strategy: EmaStrategy, _symbol: str, _timeframe: str, connection_choice: ConnectionOption):
        self.strategy = _strategy
        self.symbol = _symbol
        self.timeframe = _timeframe
        if connection_choice == ConnectionOption.MT5:
            self.connection = MetaTraderConnection()
        else:
            self.connection = MockConnection()

    def look_for_trades(self):
        print("Using the " + self.strategy.get_strategy_name() + ", trading on " + self.symbol)
        
        first_candlestick_set = self.connection.get_candles_for_symbol(self.symbol, self.timeframe, NUM_CANDLESTICKS)
        time = int(round(first_candlestick_set.iloc[-1]['time']))

        self.strategy.set_current_candlestick_time(time)
        self.strategy.process_seed(first_candlestick_set)

        while (True):
            candlestick_set = self.connection.get_candles_for_symbol(self.symbol, self.timeframe, NUM_CANDLESTICKS)
            # why are we doing this check? Is it just for mocks?
            if(int(round(first_candlestick_set.iloc[-1]['time']))):
                self.strategy.process_next(candlestick_set)
                signal = self.strategy.check_signal()
                if signal["action"] == 0:
                    self.connection.do_nothing()
                else:
                    self.trade(signal["action"])
                # strategy.record_action()
                # action_writer.print_action()

    def trade(self, signal):
        bid_price = self.connection.get_bid_price(self.symbol)
        ask_price = self.connection.get_ask_price(self.symbol)
        self.connection.close_all_open_positions(bid_price, ask_price, 20)
        balance = self.connection.get_account_balance();
        price: int
        if signal == 1:
            price = ask_price
        else:
            price = bid_price
        volume = self.calc_lot_size(price, balance)
        order_placed = self.connection.place_order(self.symbol, signal, price, volume, 20)
        
        print("order placed: ")
        print(order_placed)

    def calc_risk(self, balance: int) -> float:
        return balance * 0.02

    def calc_lot_size(self, price, balance) -> float:
        risk_per_trade = self.calc_risk(balance)
        return risk_per_trade / price