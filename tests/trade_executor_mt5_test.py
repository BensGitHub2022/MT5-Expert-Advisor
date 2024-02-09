from mock import MagicMock, patch
from src.account_mt5 import AccountMT5
from src.signal import Signal
from src.signal_type import SignalType
from src.trade_executor_mt5 import TradeExecutorMT5
from tests.named_tuple_helper import MQLTradeResultNamedTuple, PositionNamedTuple

import pytest
import sys
import unittest

sys.modules['mt5'] = MagicMock()

class TradeExecutorMT5Tests(unittest.TestCase):

    ask = 1
    bid = 1
    deviation = 20
    price = 0.0
    signal = Signal(SignalType.BUY)
    symbol = "test symbol"
    trade_executor: TradeExecutorMT5

    @classmethod
    def setUpClass(self):
        mock_account = AccountMT5()
        mock_account.get_account_info = MagicMock('get_account_info')
        mock_account.get_account_info.return_value = {
            "balance": 0
        }
        self.trade_executor = TradeExecutorMT5(mock_account)

    @patch('src.trade_executor_mt5.mt5.last_error')
    @patch('src.trade_executor_mt5.mt5.order_send')
    @patch('src.trade_executor_mt5.calc_lot_size')
    def test_place_order_none_response(self, calc_lot_size, order_send_request, last_error_query):
        calc_lot_size.return_value = 1
        order_send_request.return_value = None
        last_error_query.return_value = None
        with pytest.raises(RuntimeError):
            self.trade_executor.place_order(self.symbol, self.signal, self.price, self.deviation)

    @patch('src.trade_executor_mt5.mt5.order_send')
    @patch('src.trade_executor_mt5.calc_lot_size')
    def test_place_order_error_response(self, calc_lot_size, order_send_request):
        calc_lot_size.return_value = 1
        order_send_request.return_value = MQLTradeResultNamedTuple(retcode = 10014)
        assert not self.trade_executor.place_order(self.symbol, self.signal, self.price, self.deviation)
        
    @patch('src.trade_executor_mt5.mt5.order_send')
    @patch('src.trade_executor_mt5.calc_lot_size')
    def test_place_order_executed_response(self, calc_lot_size, order_send_request):
        calc_lot_size.return_value = 1
        order_send_request.return_value = MQLTradeResultNamedTuple(retcode = 10009)
        assert self.trade_executor.place_order(self.symbol, self.signal, self.price, self.deviation)
    
    @patch('src.trade_executor_mt5.mt5.last_error')
    @patch('src.trade_executor_mt5.mt5.order_send')
    @patch('src.trade_executor_mt5.calc_lot_size')
    def test_close_position_none_response(self, calc_lot_size, order_send_request, last_error_query):
        calc_lot_size.return_value = 1
        order_send_request.return_value = None
        last_error_query.return_value = None
        with pytest.raises(RuntimeError):
            self.trade_executor.close_position(PositionNamedTuple(), self.bid, self.ask, self.deviation)

    @patch('src.trade_executor_mt5.mt5.order_send')
    @patch('src.trade_executor_mt5.calc_lot_size')
    def test_close_position_error_response(self, calc_lot_size, order_send_request):
        calc_lot_size.return_value = 1
        order_send_request.return_value = MQLTradeResultNamedTuple(retcode = 10014)
        assert not self.trade_executor.close_position(PositionNamedTuple(), self.bid, self.ask, self.deviation)
        
    @patch('src.trade_executor_mt5.mt5.order_send')
    @patch('src.trade_executor_mt5.calc_lot_size')
    def test_close_position_executed_response(self, calc_lot_size, order_send_request):
        calc_lot_size.return_value = 1
        order_send_request.return_value = MQLTradeResultNamedTuple(retcode = 10009)
        assert self.trade_executor.close_position(PositionNamedTuple(), self.bid, self.ask, self.deviation) 
        
