import json
import unittest

import pytest

from mock import patch
from src.metatrader.context_mt5 import ContextMT5


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
        self.context = ContextMT5()

    @patch('src.metatrader.context_mt5.mt5.login')
    @patch('src.metatrader.context_mt5.mt5.initialize')
    @patch('src.json_reader.JsonReader.get_json_data')
    def test_connect_init_and_login_successful(self, mock_get_json_data, mock_init, mock_login):
        mock_get_json_data.return_value = self.credentials
        mock_init.return_value = True
        mock_login.return_value = True
        assert self.context.connect()

    @patch('src.metatrader.context_mt5.mt5.initialize')
    @patch('src.json_reader.JsonReader.get_json_data')
    def test_connect_initialization_errors(self, mock_get_json_data, mock_init):
        mock_get_json_data.return_value = self.credentials
        mock_init.return_value = False
        with pytest.raises(ConnectionError):
            self.context.connect()
  
    @patch('src.metatrader.context_mt5.mt5.login')
    @patch('src.metatrader.context_mt5.mt5.initialize')
    @patch('src.json_reader.JsonReader.get_json_data')
    def test_connect_login_errors(self, mock_get_json_data, mock_init, mock_login):
        mock_get_json_data.return_value = self.credentials
        mock_init.return_value = True
        mock_login.return_value = False
        with pytest.raises(PermissionError):
            self.context.connect()
    
    @patch('src.json_reader.JsonReader.get_json_data')
    def test_connect_credential_value_missing(self, mock_get_json_data):
        mock_get_json_data.return_value = {}
        with pytest.raises(KeyError):
            self.context.connect()
    