from collections import namedtuple
from mock import MagicMock, patch
from src.symbol_mt5 import SymbolMT5

import pytest
import sys
import unittest

sys.modules['mt5'] = MagicMock()

class SymbolMT5Tests(unittest.TestCase):
    
    symbol: SymbolMT5

    symbol_info_tick_response: namedtuple
    symbol_info_response: namedtuple
    bid_price = 0
    ask_price = 0
    pip_size = 0
    contract_size = 0

    @classmethod
    def setUpClass(self):
        SymbolInfo = namedtuple("SymoblInfo", ["trade_tick_size", "trade_contract_size"])
        self.symbol_info_response = SymbolInfo(self.pip_size, self.contract_size)
        SymbolInfoTick = namedtuple("SymbolInfoTick", ["bid","ask"])
        self.symbol_info_tick_response = SymbolInfoTick(self.bid_price, self.ask_price)
        self.symbol = SymbolMT5("testSymbol", "one_minute")

    @patch('src.symbol_mt5.mt5.last_error')
    @patch('src.symbol_mt5.mt5.symbol_info')
    def test_get_symbol_info_none_response(self, symbol_info_query, last_error_query):
        symbol_info_query.return_value = None
        last_error_query.return_value = None
        with pytest.raises(RuntimeError):
            self.symbol.get_symbol_info()

    @patch('src.symbol_mt5.mt5.symbol_info')
    def test_get_symbol_pip_size(self, symbol_info_query):
        symbol_info_query.return_value = self.symbol_info_response
        assert self.symbol.get_symbol_pip_size() == self.pip_size

    @patch('src.symbol_mt5.mt5.symbol_info')
    def test_get_symbol_contract_size(self, symbol_info_query):
        symbol_info_query.return_value = self.symbol_info_response
        assert self.symbol.get_symbol_contract_size() == self.contract_size

    @patch('src.symbol_mt5.mt5.last_error')
    @patch('src.symbol_mt5.mt5.symbol_info_tick')
    def test_get_symbol_info_tick_none_response(self, symbol_info_tick_query, last_error_query):
        symbol_info_tick_query.return_value = None
        last_error_query.return_value = None
        with pytest.raises(RuntimeError):
            self.symbol.get_symbol_info_tick()
            
    @patch('src.symbol_mt5.mt5.symbol_info_tick')
    def test_get_symbol_info_ask(self, symbol_info_tick_query):
        symbol_info_tick_query.return_value = self.symbol_info_tick_response
        assert self.symbol.get_symbol_info_ask() == self.ask_price
        
    @patch('src.symbol_mt5.mt5.symbol_info_tick')
    def test_get_symbol_info_ask(self, symbol_info_tick_query):
        symbol_info_tick_query.return_value = self.symbol_info_tick_response
        assert self.symbol.get_symbol_info_bid() == self.bid_price