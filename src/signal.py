from src.signal_type import SignalType

class Signal():
    signal_type: SignalType

    def __init__(self, signal_type: SignalType):
        self.signal_type = signal_type