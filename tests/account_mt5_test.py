from collections import namedtuple
from mock import MagicMock, patch
from src.account_mt5 import AccountMT5

import pytest
import sys
import unittest

sys.modules['mt5'] = MagicMock()

class AccountMT5Tests(unittest.TestCase):
    
    account: AccountMT5

    account_info_response: namedtuple
    balance = 100000.0
    profit = 0.0

    @classmethod
    def setUpClass(self):
        AccountMock = namedtuple("Account", ["balance", "profit"])
        self.account_info_response = AccountMock(self.balance, self.profit)
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