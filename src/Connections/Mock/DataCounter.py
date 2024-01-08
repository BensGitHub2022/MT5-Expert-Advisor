import pandas as pd

class DataCounter():
    current_index: int
    dataframe_size: int
    df: pd.DataFrame

    def __init__(self, df: pd.DataFrame, current_index = 0) -> None:
        self.df = df
        self.dataframe_size = len(df)
        self.current_index = current_index

    def __iter__(self) -> object:
        return self.current_index

    def __next__(self) -> int:
        temp_index = self.current_index
        if (temp_index+1 >= self.dataframe_size):
            raise IndexError(f"{temp_index} is out of bounds of the current mock data!")
        else:
            self.current_index += 1
        return self.current_index
    
    def __previous__(self) -> int:
        temp_index = self.current_index
        if (temp_index-1 < 0):
            raise IndexError(f"{temp_index} is out of bounds of the current mock data!")
        else:
            self.current_index -= 1
        return self.current_index
        
    def __hasnext__(self) -> bool:
        temp_index = self.current_index
        if (temp_index+1 >= self.dataframe_size):
            return False
        else:
            return True
        
    def __hasprevious__(self) -> bool:
        temp_index = self.current_index
        if (temp_index-1 < 0):
            return False
        else:
            return True

    def __advance__(self, interval) -> int:
        temp_index = self.current_index + interval
        if (temp_index < 0 | temp_index >= self.dataframe_size):
            raise IndexError(f"{temp_index} is out of bounds of the current mock data!")
        else:
            self.current_index = temp_index
        return self.current_index
    
    def __setindex__(self, new_index) -> int:
        if (new_index < 0 | new_index >= self.dataframe_size):
            raise IndexError(f"{new_index} is out of bounds of the current mock data!")
        else:
            self.current_index = new_index
        return self.current_index
    
    def check_index(self, temp_index) -> bool:
        if (temp_index < 0 | temp_index >= self.dataframe_size):
            raise IndexError(f"{temp_index} is out of bounds of the current mock data!")
        return True