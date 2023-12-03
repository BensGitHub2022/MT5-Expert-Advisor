from src.json_reader import JsonReader
from src.candlesticks import Candlesticks
from src.trade_bot import TradeBot
from src.ema_strategy import EmaStrategy
from src.meta_trader_factory import MetaTraderFactory

# Path to MetaTrader5 login details.
ACCOUNT_SETTINGS_PATH = "pkg/settings.json"
CREDENTIALS_FILE_PATH = "pkg/credentials.json"

def main():
    print("Hello Trade Bot!")

    # Composition root

    json_settings = JsonReader(ACCOUNT_SETTINGS_PATH)
    symbol = json_settings.get_symbol()
    timeframe = json_settings.get_timeframe()
    print(symbol)

    credentials = JsonReader(CREDENTIALS_FILE_PATH)

    factory = MetaTraderFactory(production=True)
    meta_trader = factory.create_meta_trader()
    meta_trader.connect(json_settings.get_json_data(),credentials.get_json_data())

    candlestick = Candlesticks(symbol,timeframe,1)
    df = candlestick.get_candles_dataframe()
    print(df)

    strategy = EmaStrategy(symbol,timeframe,50,200,)
    meta_trader.set_candlesticks(strategy.get_symbol(),strategy.get_timeframe())
    seed_count = strategy.get_interval()
    seed = meta_trader.get_seed(seed_count)
    strategy.process_seed(seed)
    print(strategy.get_data_frame())
    print(strategy.get_current_time())
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