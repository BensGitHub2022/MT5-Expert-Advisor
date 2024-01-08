class Ticks():

    def get_symbol_info_tick(self) -> dict:
        rounded_candlestick_time = int(round(self.candles_df.iloc[-1]['time']))
        tick_df = pd.DataFrame()
        while (tick_df.empty):
            tick_df = self.ticks_df_master.loc[self.ticks_df_master['time']==rounded_candlestick_time]
            rounded_candlestick_time -= 1
        tick = tick_df.to_dict('list')
        return tick