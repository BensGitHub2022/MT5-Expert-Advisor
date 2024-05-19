
from src.interfaces import IContext


class ContextSimulator(IContext):

    def connect(self) -> bool:
        # always happy
        print("Trading bot initialized!")
        print("Trading bot login successful!")
        return True
    
