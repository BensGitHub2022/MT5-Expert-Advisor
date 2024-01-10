import pandas as pd

class TicksHelper():

    def get_symbol_info_tick(self) -> dict:
        rounded_candlestick_time = int(round(self.candles_df.iloc[-1]['time']))
        tick_df = pd.DataFrame()
        while (tick_df.empty):
            tick_df = self.ticks_df_master.loc[self.ticks_df_master['time']==rounded_candlestick_time]
            rounded_candlestick_time -= 1
        tick = tick_df.to_dict('list')
        return tick
    
    def get_symbol_info_bid(self) -> float:
        symbol_info_tick = self.get_symbol_info_tick()
        symbol_info_bid = symbol_info_tick['bid'][0]
        return symbol_info_bid

    def get_symbol_info_ask(self) -> float:
        symbol_info_tick = self.get_symbol_info_tick()
        symbol_info_ask = symbol_info_tick['ask']
        return symbol_info_ask