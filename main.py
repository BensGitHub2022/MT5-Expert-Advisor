from src.json_reader import JsonReader
from src.symbols_adapter import SymbolsAdapter
from src.trade_bot import TradeBot
from src.ema_strategy import EmaStrategy
from src.meta_trader_factory import MetaTraderFactory

from src.symbols_factory import SymbolsFactory

# Path to MetaTrader5 login details.
ACCOUNT_SETTINGS_PATH = "pkg/settings.json"
CREDENTIALS_FILE_PATH = "pkg/credentials.json"

MOCK_LOCATION = "pkg/candlesticks_modified.csv"

def main():
    print("Hello Trade Bot!")

    # Composition root

    json_settings = JsonReader(ACCOUNT_SETTINGS_PATH)
    symbol = json_settings.get_symbol()
    timeframe = json_settings.get_timeframe()
    print(symbol)

    credentials = JsonReader(CREDENTIALS_FILE_PATH)

    meta_trader_factory = MetaTraderFactory(production=True)
    meta_trader = meta_trader_factory.create_meta_trader()
    meta_trader.connect(json_settings.get_json_data(),credentials.get_json_data())

    strategy = EmaStrategy(symbol,timeframe,2,3)

    symbol_factory = SymbolsFactory(production=False)

    symbol = symbol_factory.create_symbol(symbol,timeframe, mock_location="pkg/candlesticks_modified.csv")
    strategy.set_current_candlestick_time(symbol.get_candlestick_time())
    strategy.process_seed(symbol.get_candlesticks(strategy.get_interval()))
    print(strategy.get_data_frame())
    strategy.check_signal()

    #tick_data = symbol.get_ticks(1)
    #print(tick_data)

    """
    symbolMock = SymbolsMock(symbol,timeframe)
    print(symbolMock.get_mt5_timeframe("one_minute"))
    
    master_df = symbolMock.get_candlesticks_from_csv(MOCK_LOCATION)
    df = symbolMock.get_candlesticks(200)
    candlestick_time = symbolMock.get_candlestick_time()
    new_candle = symbolMock.get_candlesticks(1)
    print(df)
    print(candlestick_time)
    print(new_candle)
    """
    
    while (True):
        if(strategy.check_next(symbol.get_candlestick_time())):
            strategy.process_next(symbol.get_candlesticks(1))
            print(strategy.get_data_frame())
            strategy.check_signal()
            #tick_data = symbol.get_ticks(1)
            #print(tick_data)
    
    
    
    """
    strategy = EmaStrategy()

    bot = TradeBot(strategy, meta_trader)
    bot.start()
    print("Bot started")

    print("Press X to stop")
    inp = input()
    # if (inp == 'X')

    bot.stop()
    print("Bot stopped")
    """
if __name__ == '__main__':
    main()