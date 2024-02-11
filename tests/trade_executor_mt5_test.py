from collections import namedtuple
from mock import MagicMock, patch
from src.account_mt5 import AccountMT5
from src.trade_executor_mt5 import TradeExecutorMT5

import pytest
import sys
import unittest

sys.modules['mt5'] = MagicMock()

class TradeExecutorMT5Tests(unittest.TestCase):
    
    trade_executor: TradeExecutorMT5
    symbol = "test symbol"
    signal = -1
    price = 0.0
    deviation = 20
    
    @classmethod
    def setUpClass(self):
        mock_account = AccountMT5()
        mock_account.get_account_info = MagicMock('get_account_info')
        mock_account.get_account_info.return_value = {
            "balance": 0
        }
        self.trade_executor = TradeExecutorMT5(mock_account)
    
    # To be implemented after the signal class is implemented
    # @patch('src.trade_executor_mt5.mt5.last_error')
    # @patch('src.trade_executor_mt5.mt5.order_send')
    # @patch('src.trade_executor_mt5.calc_lot_size')
    # def test_place_order_none_response(self, calc_lot_size, order_send_request, last_error_query):
    #     calc_lot_size.return_value = 1
    #     order_send_request.return_value = None
    #     last_error_query.return_value = None
    #     with pytest.raises(RuntimeError):
    #         self.trade_executor.place_order(self.symbol, self.signal, self.price, self.deviation)
