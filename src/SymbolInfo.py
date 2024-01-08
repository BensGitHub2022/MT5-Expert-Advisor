class SymbolInfo():
    def get_symbol_name(self) -> str:
        return self.symbol
    
    def get_symbol_info_bid(self) -> float:
        symbol_info_tick = self.get_symbol_info_tick()
        symbol_info_bid = symbol_info_tick['bid'][0]
        return symbol_info_bid

    def get_symbol_info_ask(self) -> float:
        symbol_info_tick = self.get_symbol_info_tick()
        symbol_info_ask = symbol_info_tick['ask']
        return symbol_info_ask