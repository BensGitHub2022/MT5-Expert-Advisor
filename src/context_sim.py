
from src.abstract_context import AbstractContext

class ContextSimulator(AbstractContext):

    def connect(self) -> bool:
        # always happy
        print("Trading bot initialized!")
        print("Trading bot login successful!")
        return True
    
