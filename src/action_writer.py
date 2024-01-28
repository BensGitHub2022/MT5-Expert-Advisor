import pandas as pd

from datetime import datetime
from datetime import timedelta
from datetime import timezone

class ActionWriter():

    initialized: bool
    index: int
    action_history_df: pd.DataFrame
    action_history_filepath: str

    def __init__(self):
        """
        Constructor for ActionWriter
        :return:
        """
        self.action_history_df = pd.DataFrame()
        self.action_history_filepath = "log/action_history_" + self.get_date_time_now() + ".csv"
        self.initialized = False
        self.index = 0
        # with open(file=self.action_history_filepath, mode = 'a+') as csv_file:
        #     return
        
    def write_action(self) -> None:
        """
        This method writes the results of trades to a csv file called action_history.csv or another file of the user's choosing
        :return: none
        """
        if(not self.initialized):
            isheader = True
            self.initialized = True
        else:
            isheader = False

        pd.DataFrame.to_csv(self.action_history_df, self.action_history_filepath, index=False, header=isheader, mode='a')

    def record_action(self, df: pd.DataFrame, action_df: pd.DataFrame) -> pd.DataFrame:
        self.action_history_df = pd.merge(df,action_df,how='inner',left_index=True,right_index=True)
        return self.action_history_df
    
    def get_date_time_now(self) -> str:
        offset = timedelta(hours=2.0)
        tz_UTC_offset = timezone(offset,'GMT')
        dt = datetime.now(tz_UTC_offset)
        format = '%Y-%m-%d-%H-%M-%S'
        dt_string = dt.strftime(format)
        return dt_string
    
    def print_action(self) -> None:
        print(self.action_history_df)