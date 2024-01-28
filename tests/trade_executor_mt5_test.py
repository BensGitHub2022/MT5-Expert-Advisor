from collections import namedtuple
from mock import MagicMock, patch
from src.trade_executor_mt5 import TradeExecutorMT5

import pytest
import sys
import unittest

sys.modules['mt5'] = MagicMock()

class TradeExecutorMT5Tests(unittest.TestCase):
    
    trade_executor: TradeExecutorMT5
    
    @classmethod
    def setUpClass(self):
        self.trade_executor = TradeExecutorMT5()
    
    @patch('src.symbol_mt5.mt5.last_error')
    @patch('src.symbol_mt5.mt5.symbol_info')
    def test_get_symbol_info_none_response(self, symbol_info_query, last_error_query):
        symbol_info_query.return_value = None
        last_error_query.return_value = None
        with pytest.raises(RuntimeError):
            self.symbol.get_symbol_info()