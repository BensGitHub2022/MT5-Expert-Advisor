from collections import namedtuple
from mock import patch
from src.account_mt5 import AccountMT5

import pytest
import unittest

class AccountMT5Tests(unittest.TestCase):
    
    account: AccountMT5

    account_info_response: namedtuple
    balance = 100000.0
    profit = 0.0

    @classmethod
    def setUpClass(self):
        AccountResponse = namedtuple("AccountResponse", ["balance", "profit"])
        self.account_info_response = AccountResponse(self.balance, self.profit)
        self.account = AccountMT5()

    @patch('src.account_mt5.mt5.account_info')
    def test_get_account_balance(self, account_info_query):
        account_info_query.return_value = self.account_info_response
        assert self.account.get_account_balance() == self.balance
        assert True
    
    @patch('src.account_mt5.mt5.account_info')
    def test_get_account_profit(self, account_info_query):
        account_info_query.return_value = self.account_info_response
        assert self.account.get_account_profit() == self.profit
    
    @patch('src.account_mt5.mt5.last_error')
    @patch('src.account_mt5.mt5.account_info')
    def test_get_account_info_none_response(self, account_info_query, last_error_query):
        account_info_query.return_value = None
        last_error_query.return_value = None
        with pytest.raises(RuntimeError):
            self.account.get_account_info()
            
    @patch('src.account_mt5.mt5.last_error')
    @patch('src.account_mt5.mt5.positions_get')
    def test_get_positions_none_response(self, positions_query, last_error_query):
        positions_query.return_value = None
        last_error_query.return_value = None
        with pytest.raises(RuntimeError):
            self.account.get_positions()