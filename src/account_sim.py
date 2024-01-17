import pandas as pd

from src.abstract_account import AbstractAccount

from datetime import datetime
from datetime import timedelta
from datetime import timezone

class AccountSimulator(AbstractAccount):

    def __init__(self):
        self.balance = 100
        self.profit = 100
        self.ticket = 500000000
        self.positions_df = pd.DataFrame('symbol','ticket','time','type','volume','price','current_price','profit') 

    def update_balance(self, profit) -> None:
        self.balance += profit

    def update_profit(self, profit) -> None:
        self.profit += profit

    def get_account_balance(self) -> float:
        return self.balance
        
    def add_position(self, symbol, type, volume, price) -> bool:
        time = self.get_date_time_now() # change this to match candlestick time ?
        current_price = self.get_current_price(type)
        d = {'symbol': symbol,'ticket':self.ticket,'time':time,'type':type,'volume':volume,'price':price,'current_price':current_price,'profit':self.calc_profit(type, price, current_price)}
        new_position_df = pd.DataFrame(data=d)
        self.positions_df = pd.concat([self.positions_df, new_position_df], ignore_index=True)
        self.ticket =+ 1
        return True

    def remove_position(self, ticket) -> float:
        profit = self.get_profit(ticket)
        row_index = self.positions_df.index[self.positions_df['ticket'] == ticket]
        self.positions_df.drop([row_index],axis=0)
        return profit
    
    def update_position(self, ticket) -> bool:
        position = self.positions_df.iloc[['ticker']==ticket]
        type = position.iloc['type']
        price = position.iloc['price']
        current_price = self.get_current_price(type)
        profit = self.calc_profit(type, price, current_price)
        position.iloc['profit'] = profit
        position.iloc['current_price'] = current_price
        return True

    def calc_profit(self, type, price, current_price) -> float:
        profit = 0
        if(type == 'buy'):
            profit = current_price - price
        if(type == 'sell'):
            profit = price - current_price
        return profit

    def get_positions(self) -> dict:
        self.positions = self.positions_df.to_dict(orient='dict')
        return self.positions
    
    def get_position(self, ticket) -> pd.DataFrame:
        # Return one position out of the positions_df
        pass
    
    def get_profit(self, ticket) -> float:
        profit = self.positions_df['profit'].iloc[['ticket'] == ticket]
        return profit
    
    def get_current_price(self, type) -> float:
        current_price = 0
        if(type == 'buy'):
            current_price = self.symbol.get_symbol_info_bid()
        if(type == 'sell'):
            current_price = self.symbol.get_symbol_info_ask()
        return current_price
    
    def get_account_profit(self) -> float:
        account_info_dict = self.get_account_info()
        profit = account_info_dict['profit']
        return profit
    
    # Option 1, use the current time as the trade time when running trade executor in mock
    def get_date_time_now(self) -> datetime:
        offset = timedelta(hours=2.0)
        tz_UTC_offset = timezone(offset,'GMT')
        dt = datetime.now(tz_UTC_offset)
        format = '%Y.%m.%d %H:%M:%S'
        dt_string = dt.strftime(format)
        return dt_string
    
    # Option 2, use the symbol time as the trade time when running trade executor in mock
    def convert_epoch_time(self, time:int) -> datetime:
        pass
    
    # Pass symbol at instantiation or via setter method ???
    def set_symbol(self, symbol: object) -> object:
        self.symbol = symbol
        return self.symbol
