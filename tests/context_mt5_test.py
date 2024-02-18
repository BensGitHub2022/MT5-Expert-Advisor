import json
import unittest

import pytest

from mock import patch
from src.context_mt5 import ContextMT5


class ContextMT5Tests(unittest.TestCase):
    
    context_with_complete_creds: ContextMT5
    
    credentials = json.loads("""{
        "mt5": {
            "server": "MetaQuotes-Demo",
            "login": 1,
            "password": "abc123",
            "terminal_pathway": "terminal64.exe",
            "server": "server",
            "timeout" : 100
        }
    }""")
    
    @classmethod
    def setUpClass(self):
        self.context_with_complete_creds = ContextMT5(self.credentials)

    @patch('src.context_mt5.mt5.login')
    @patch('src.context_mt5.mt5.initialize')
    def test_connect_init_and_login_successful(self, mock_init, mock_login):
        mock_init.return_value = True
        mock_login.return_value = True
        assert self.context_with_complete_creds.connect()

    @patch('src.context_mt5.mt5.initialize')
    def test_connect_initialization_errors(self, mock_init):
        mock_init.return_value = False
        with pytest.raises(ConnectionError):
            self.context_with_complete_creds.connect()
  
    @patch('src.context_mt5.mt5.login')
    @patch('src.context_mt5.mt5.initialize')
    def test_connect_login_errors(self, mock_init, mock_login):
        mock_init.return_value = True
        mock_login.return_value = False
        with pytest.raises(PermissionError):
            self.context_with_complete_creds.connect()
    
    # I think this is what you mean
    def test_connect_credential_value_missing(self):
        context_with_no_credentials = ContextMT5({})
        with pytest.raises(KeyError):
            context_with_no_credentials.connect()
    