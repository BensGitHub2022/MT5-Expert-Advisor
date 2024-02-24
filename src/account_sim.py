from datetime import datetime, timedelta, timezone

import json as JSON
import pandas as pd

from src.interfaces import IAccount

class AccountSimulator(IAccount):
    
    balance: float
    profit: float

    ticket: int
    symbol: object 
    
    last_position_df: pd.DataFrame
    positions_df: pd.DataFrame
    positions: dict

    account_df: pd.DataFrame

    action_writer: object

    def __init__(self, symbol: object, balance: float, profit: float, action_writer: object) -> None:
        self.balance = balance
        self.profit = profit
        self.ticket = 500000000
        self.positions = dict()
        self.positions_df = pd.DataFrame(columns=['symbol','ticket','time','type','volume','price','current_price','profit'])
        d = {'balance': [self.balance], 'real_profit': [self.profit]}
        self.account_df = pd.DataFrame(data=d)
        self.symbol = symbol
        self.action_writer = action_writer

    def update_balance(self, capital_committed) -> float:
        self.balance += capital_committed
        return self.balance

    def update_profit(self, profit) -> float:
        self.profit += profit
        return self.profit

    def update_account(self) -> bool:
        old_profit = self.account_df['real_profit'][0]
        old_balance = self.account_df['balance'][0]
        self.account_df['real_profit'].replace(old_profit,self.profit,inplace=True)
        self.account_df['balance'].replace(old_balance,self.balance,inplace=True)
        return True

    def get_account_balance(self) -> float:
        return self.balance
    
    def get_account_profit(self) -> float:
        return self.profit
    
    def get_account_json(self) -> JSON:
        account_json = self.account_df.to_json(orient="records")
        return account_json
    
    def get_position_json(self) -> JSON:
        position_json = self.positions_df.to_json(orient="records")
        return position_json

    def add_position(self, symbol, type, volume, price) -> bool:
        time = self.symbol.get_tick_time()
        current_price = price 
        d = {'symbol': symbol,'ticket':self.ticket,'time':time,'type':type,'volume':volume,'price':price,'current_price':current_price,'profit':self.calc_profit(type, price, current_price)}
        new_position_df = pd.DataFrame(data=[d])
        self.positions_df = pd.concat([self.positions_df, new_position_df], ignore_index=True)
        self.ticket += 1
        return True

    def remove_position(self, ticket) -> bool:
        position = self.positions_df.loc[self.positions_df['ticket']==ticket]
        volume = position['volume'][0]
        price = position['price'][0]
        current_price = position['current_price'][0]
        profit = position['profit'][0]
        type = position['type'][0]
        #real_profit = volume*profit #NOTE: This was a bug - this was being performed in both and was being double counted
        returned_capital = self.calc_capital_gain_loss(type,volume,current_price,price,profit)

        row_index = self.positions_df.index[self.positions_df['ticket'] == ticket][0]
        self.positions_df.drop([row_index],axis=0,inplace=True)
        
        self.last_position_df = position
        self.update_balance(returned_capital)
        self.update_profit(profit)
        self.update_account()
        self.record_position(self.last_position_df, self.account_df)
        return True
    
    def update_position(self, ticket) -> bool:
        position = self.positions_df.loc[self.positions_df['ticket']==ticket]
        volume = position['volume'][0]
        type = position['type'][0]
        price = position['price'][0]
        current_price = self.get_current_price(type)
        profit = self.calc_profit(type, price, current_price)
        real_profit = profit*volume
        old_profit=position['profit'][0]
        self.positions_df['profit'].replace(old_profit,real_profit,inplace=True)
        old_price = position['current_price'][0]
        self.positions_df['current_price'].replace(old_price,current_price,inplace=True)
        return True

    def calc_profit(self, type, price, current_price) -> float:
        profit = 0
        if(type == 'buy'):
            profit = current_price - price
        if(type == 'sell'):
            profit = price - current_price
        return profit
    
    def calc_capital_gain_loss(self, type, volume, current_price, price, real_profit) -> float:
        returned_capital = 0
        if(type == 'buy'):
            returned_capital = current_price*volume
        if(type == 'sell'):
            returned_capital = price*volume+real_profit
        return returned_capital

    # Note on 1.21.24 that positions are actually returned from MT5 as named Tuples
    def get_positions(self) -> tuple:
        if(self.positions_df.empty):
            return 0
        else:
            #self.positions = self.positions_df.to_dict(orient='index')
            self.positions = list(self.positions_df.itertuples(index=False, name="TradePosition"))
        return self.positions
    
    def get_position(self, ticket) -> pd.DataFrame:
        # Return one position out of the positions_df
        pass
      
    def get_current_price(self, type) -> float:
        current_price = 0
        if(type == 'buy'):
            current_price = self.symbol.get_symbol_info_bid()
        if(type == 'sell'):
            current_price = self.symbol.get_symbol_info_ask()
        return current_price
    
    # Option 1, use the current time as the trade time when running trade executor in mock
    # Update on 1.21.24 - currently using system time to record trades but this doesn't match MT5 real output
    def get_date_time_now(self) -> datetime:
        offset = timedelta(hours=2.0)
        tz_UTC_offset = timezone(offset,'GMT')
        dt = datetime.now(tz_UTC_offset)
        format = '%Y.%m.%d %H:%M:%S'
        dt_string = dt.strftime(format)
        return dt_string
    
    # Option 2, use the symbol time as the trade time when running trade executor in mock
    # Update on 1.21.24 - need to use symbol time to determine the trade time to mimick MT5
    def convert_epoch_time(self, time:int) -> datetime:
        pass
    
    # Pass symbol at instantiation or via setter method ???
    # Update on 1.21.24 - symbol is passed via dependency injection
    def set_symbol(self, symbol: object) -> object:
        self.symbol = symbol
        return self.symbol

    def record_position(self, position_df, action_df) -> bool:
        self.action_writer.record_position(position_df, action_df)
        self.action_writer.write_position()
        return True
